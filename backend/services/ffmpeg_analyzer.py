"""
FFmpeg video analyzer service.

Uses PyAV (FFmpeg bindings) to analyze video fragments and extract
detailed metadata about streams.
"""

import av
import httpx
import tempfile
import os
from typing import List, Dict, Optional
from pathlib import Path
from urllib.parse import urljoin

from models.schemas import VideoMetadata


# Timeout for fragment downloads
FRAGMENT_TIMEOUT = 10.0
# Maximum fragment size to download (50MB)
MAX_FRAGMENT_SIZE = 50 * 1024 * 1024
# Number of fragments to analyze per bitrate level
FRAGMENTS_TO_ANALYZE = 2


async def download_fragment(url: str, timeout: float = FRAGMENT_TIMEOUT) -> Optional[bytes]:
    """
    Download a video fragment from URL.

    Args:
        url: Fragment URL
        timeout: Download timeout in seconds

    Returns:
        Fragment bytes or None if download fails
    """
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()

            # Check size
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > MAX_FRAGMENT_SIZE:
                print(f"Fragment too large: {content_length} bytes")
                return None

            content = response.content
            if len(content) > MAX_FRAGMENT_SIZE:
                print(f"Fragment too large: {len(content)} bytes")
                return None

            return content

    except Exception as e:
        print(f"Error downloading fragment from {url}: {e}")
        return None


def analyze_fragment_with_pyav(fragment_data: bytes) -> Dict:
    """
    Analyze video fragment using PyAV (FFmpeg).

    Also detects DRM/encryption by attempting to decode the fragment.

    Args:
        fragment_data: Fragment binary data

    Returns:
        Dictionary containing video metadata and encryption status
    """
    # Write fragment to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        tmp_file.write(fragment_data)
        tmp_path = tmp_file.name

    try:
        # Open with PyAV
        container = av.open(tmp_path)

        metadata = {
            'container_format': container.format.name,
            'duration': container.duration / av.time_base if container.duration else None,
            'file_size': len(fragment_data),
            'is_encrypted': False,
            'drm_detected': None
        }

        # Find video stream
        video_stream = None
        for stream in container.streams.video:
            video_stream = stream
            break

        if video_stream:
            # Extract video metadata
            metadata['video_codec'] = video_stream.codec_context.name
            metadata['codec_profile'] = video_stream.codec_context.profile if video_stream.codec_context.profile else None

            # Resolution
            if video_stream.codec_context.width and video_stream.codec_context.height:
                metadata['resolution'] = f"{video_stream.codec_context.width}x{video_stream.codec_context.height}"

            # Frame rate
            if video_stream.average_rate:
                try:
                    metadata['frame_rate'] = float(video_stream.average_rate)
                except:
                    pass

            # Bitrate
            if video_stream.codec_context.bit_rate:
                metadata['bitrate'] = video_stream.codec_context.bit_rate

            # Color space
            pix_fmt = video_stream.codec_context.pix_fmt
            if pix_fmt:
                metadata['color_space'] = pix_fmt

            # Calculate fragment duration
            if container.duration:
                metadata['fragment_duration'] = container.duration / av.time_base

            # Check for encryption by trying to decode a frame
            try:
                # Attempt to decode one frame
                packet_count = 0
                decoded_frame = False

                for packet in container.demux(video_stream):
                    packet_count += 1
                    try:
                        for frame in packet.decode():
                            # Successfully decoded a frame
                            decoded_frame = True
                            break
                    except Exception as decode_error:
                        # Decode error might indicate encryption
                        error_str = str(decode_error).lower()
                        if any(term in error_str for term in ['decrypt', 'encrypted', 'drm', 'protection']):
                            metadata['is_encrypted'] = True
                            metadata['drm_detected'] = 'Unknown (encrypted)'
                        break

                    if decoded_frame or packet_count >= 5:
                        break

                # If we read packets but couldn't decode any frames, likely encrypted
                if packet_count > 0 and not decoded_frame:
                    metadata['is_encrypted'] = True
                    metadata['drm_detected'] = 'Unknown (encrypted)'

            except Exception as e:
                # If we can't even read packets, check if it's encryption-related
                error_str = str(e).lower()
                if any(term in error_str for term in ['decrypt', 'encrypted', 'drm', 'protection', 'cenc']):
                    metadata['is_encrypted'] = True
                    metadata['drm_detected'] = 'Unknown (encrypted)'

        # Find audio stream
        audio_stream = None
        for stream in container.streams.audio:
            audio_stream = stream
            break

        if audio_stream:
            metadata['audio_codec'] = audio_stream.codec_context.name
            metadata['audio_channels'] = audio_stream.codec_context.channels
            metadata['audio_sample_rate'] = audio_stream.codec_context.sample_rate

        container.close()

        return metadata

    except Exception as e:
        error_str = str(e).lower()
        print(f"Error analyzing fragment with PyAV: {e}")

        # Check if error indicates encryption
        if any(term in error_str for term in ['decrypt', 'encrypted', 'drm', 'protection', 'cenc']):
            return {
                'is_encrypted': True,
                'drm_detected': 'Unknown (encrypted)',
                'file_size': len(fragment_data),
                'error': str(e)
            }

        return {}
    finally:
        # Clean up temp file
        try:
            os.unlink(tmp_path)
        except:
            pass


def get_hls_fragment_urls(parsed_data: Dict, manifest_url: str) -> Dict[int, List[str]]:
    """
    Extract fragment URLs from HLS parsed data.

    Args:
        parsed_data: Parsed HLS manifest data
        manifest_url: The manifest URL to resolve relative URLs

    Returns:
        Dictionary mapping bitrate level to list of fragment URLs
    """
    fragment_urls = {}
    playlist = parsed_data.get('raw_playlist')

    if not playlist or not playlist.playlists:
        return fragment_urls

    # For each bitrate level, get segment URLs
    for idx, variant in enumerate(playlist.playlists):
        if variant.uri:
            # This is a variant playlist - we'd need to fetch it to get actual segments
            # Convert relative URL to absolute URL
            absolute_url = urljoin(manifest_url, variant.uri)
            fragment_urls[idx] = [absolute_url]

    return fragment_urls


def get_dash_fragment_urls(parsed_data: Dict, manifest_url: str) -> Dict[int, List[str]]:
    """
    Extract fragment URLs from DASH parsed data.

    Args:
        parsed_data: Parsed DASH manifest data
        manifest_url: The manifest URL to resolve relative URLs

    Returns:
        Dictionary mapping bitrate level to list of fragment URLs
    """
    fragment_urls = {}
    root = parsed_data.get('raw_xml')
    namespaces = parsed_data.get('namespaces', {})

    if root is None:
        return fragment_urls

    level = 0

    # Find video representations and their segments
    for period in root.findall('.//mpd:Period', namespaces):
        for adaptation_set in period.findall('.//mpd:AdaptationSet', namespaces):
            # Check if video
            content_type = adaptation_set.get('contentType', '')
            mime_type = adaptation_set.get('mimeType', '')
            is_video = 'video' in content_type or 'video' in mime_type

            if not is_video:
                for rep in adaptation_set.findall('.//mpd:Representation', namespaces):
                    rep_mime = rep.get('mimeType', mime_type)
                    if 'video' in rep_mime:
                        is_video = True
                        break

            if not is_video:
                continue

            # Extract segment URLs from each representation
            for representation in adaptation_set.findall('.//mpd:Representation', namespaces):
                urls = []

                # Look for BaseURL
                base_url_elem = representation.find('.//mpd:BaseURL', namespaces)
                if base_url_elem is not None and base_url_elem.text:
                    relative_url = base_url_elem.text.strip()
                    # Convert relative URL to absolute URL
                    absolute_url = urljoin(manifest_url, relative_url)
                    urls.append(absolute_url)

                # Look for SegmentTemplate or SegmentList
                # This would require more complex URL construction
                # For now, just use BaseURL if available

                if urls:
                    fragment_urls[level] = urls[:FRAGMENTS_TO_ANALYZE]

                level += 1

    return fragment_urls


async def analyze_video_fragments(parsed_data: Dict, manifest_type: str, manifest_url: str = '') -> tuple[List[VideoMetadata], Optional[Dict]]:
    """
    Analyze video fragments using FFmpeg.

    Args:
        parsed_data: Parsed manifest data
        manifest_type: Type of manifest ('hls' or 'dash')
        manifest_url: The manifest URL to resolve relative URLs

    Returns:
        Tuple of (List of VideoMetadata objects, DRM info dict or None)
    """
    metadata_list = []
    drm_info = None

    try:
        # Get fragment URLs based on manifest type
        if manifest_type == 'hls':
            fragment_urls = get_hls_fragment_urls(parsed_data, manifest_url)
        else:
            fragment_urls = get_dash_fragment_urls(parsed_data, manifest_url)

        # Analyze fragments for each bitrate level
        for level, urls in fragment_urls.items():
            for url in urls[:FRAGMENTS_TO_ANALYZE]:
                # Download fragment
                fragment_data = await download_fragment(url)

                if fragment_data:
                    # Analyze with PyAV
                    analysis = analyze_fragment_with_pyav(fragment_data)

                    if analysis:
                        # Check if DRM was detected in fragment
                        if analysis.get('is_encrypted') and not drm_info:
                            drm_info = {
                                'system': analysis.get('drm_detected', 'Unknown'),
                                'detected_by': 'ffmpeg'
                            }

                        # Create VideoMetadata object
                        metadata = VideoMetadata(
                            level=level,
                            container_format=analysis.get('container_format'),
                            video_codec=analysis.get('video_codec'),
                            codec_profile=analysis.get('codec_profile'),
                            resolution=analysis.get('resolution'),
                            frame_rate=analysis.get('frame_rate'),
                            bitrate=analysis.get('bitrate'),
                            color_space=analysis.get('color_space'),
                            fragment_duration=analysis.get('fragment_duration'),
                            file_size=analysis.get('file_size')
                        )
                        metadata_list.append(metadata)

                        # Only analyze one fragment per level for now
                        break

    except Exception as e:
        print(f"Error analyzing video fragments: {e}")

    return metadata_list, drm_info
