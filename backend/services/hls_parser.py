"""
HLS manifest parser service.

Parses HLS (.m3u8) manifests and extracts stream information including
bitrates, audio tracks, subtitles, and DRM information.
"""

import m3u8
import httpx
from typing import Dict, List, Optional
from fastapi import HTTPException

from models.schemas import (
    BitrateInfo, AudioTrack, SubtitleTrack,
    ThumbnailTrack, DRMInfo
)


# Timeout for manifest downloads (30 seconds)
MANIFEST_TIMEOUT = 30.0
# Maximum manifest size (10MB)
MAX_MANIFEST_SIZE = 10 * 1024 * 1024


async def fetch_manifest(url: str) -> str:
    """
    Fetch manifest content from URL with timeout and size limits.

    Args:
        url: Manifest URL to fetch

    Returns:
        Manifest content as string

    Raises:
        HTTPException: If fetch fails or exceeds limits
    """
    try:
        async with httpx.AsyncClient(timeout=MANIFEST_TIMEOUT) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()

            # Check content size
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > MAX_MANIFEST_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"Manifest size exceeds maximum of {MAX_MANIFEST_SIZE} bytes"
                )

            content = response.text
            if len(content) > MAX_MANIFEST_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"Manifest size exceeds maximum of {MAX_MANIFEST_SIZE} bytes"
                )

            return content

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail=f"Timeout fetching manifest (max {MANIFEST_TIMEOUT}s)"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"HTTP error fetching manifest: {e.response.status_code}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching manifest: {str(e)}"
        )


def parse_drm_info(playlist: m3u8.M3U8) -> Optional[DRMInfo]:
    """
    Extract DRM information from HLS manifest.

    Args:
        playlist: Parsed M3U8 playlist

    Returns:
        DRMInfo if DRM is detected, None otherwise
    """
    # Check for encryption in keys
    if playlist.keys:
        for key in playlist.keys:
            if key and key.method and key.method != 'NONE':
                system = key.method
                if 'AES' in system:
                    system = 'AES-128'
                elif 'SAMPLE-AES' in system:
                    system = 'SAMPLE-AES'

                return DRMInfo(
                    system=system,
                    key_id=key.iv if hasattr(key, 'iv') else None,
                    license_url=key.uri if key.uri else None,
                    pssh=None  # HLS doesn't typically use PSSH boxes
                )

    # Check segments for encryption
    if playlist.segments:
        for segment in playlist.segments:
            if segment.key and segment.key.method and segment.key.method != 'NONE':
                return DRMInfo(
                    system=segment.key.method,
                    license_url=segment.key.uri if segment.key.uri else None,
                    key_id=segment.key.iv if hasattr(segment.key, 'iv') else None,
                    pssh=None
                )

    return None


def parse_bitrates(playlist: m3u8.M3U8) -> List[BitrateInfo]:
    """
    Extract bitrate information from HLS manifest.

    Args:
        playlist: Parsed M3U8 playlist

    Returns:
        List of BitrateInfo objects
    """
    bitrates = []

    if not playlist.playlists:
        return bitrates

    for idx, variant in enumerate(playlist.playlists):
        stream_info = variant.stream_info

        # Extract resolution
        resolution = None
        if stream_info.resolution:
            width, height = stream_info.resolution
            resolution = f"{width}x{height}"

        # Extract codec
        codec = None
        if stream_info.codecs:
            # Parse video codec from codecs string
            codecs_list = stream_info.codecs.split(',')
            for c in codecs_list:
                c = c.strip()
                if c.startswith('avc') or c.startswith('hvc') or c.startswith('vp'):
                    if c.startswith('avc'):
                        codec = 'H.264'
                    elif c.startswith('hvc') or c.startswith('hev'):
                        codec = 'H.265'
                    elif c.startswith('vp09'):
                        codec = 'VP9'
                    elif c.startswith('av01'):
                        codec = 'AV1'
                    break

        # Extract audio codec
        audio_codec = None
        if stream_info.codecs:
            codecs_list = stream_info.codecs.split(',')
            for c in codecs_list:
                c = c.strip()
                if c.startswith('mp4a'):
                    audio_codec = 'AAC'
                elif c.startswith('ac-3'):
                    audio_codec = 'AC3'
                elif c.startswith('ec-3'):
                    audio_codec = 'EAC3'

        bitrates.append(BitrateInfo(
            level=idx,
            bitrate=stream_info.bandwidth if stream_info.bandwidth else 0,
            resolution=resolution,
            codec=codec,
            frame_rate=stream_info.frame_rate if hasattr(stream_info, 'frame_rate') else None,
            audio_codec=audio_codec
        ))

    return bitrates


def parse_audio_tracks(playlist: m3u8.M3U8) -> List[AudioTrack]:
    """
    Extract audio track information from HLS manifest.

    Args:
        playlist: Parsed M3U8 playlist

    Returns:
        List of AudioTrack objects
    """
    audio_tracks = []

    if not playlist.media:
        return audio_tracks

    for media in playlist.media:
        if media.type == 'AUDIO':
            # Parse codec from group_id or uri
            codec = None
            if media.group_id:
                if 'aac' in media.group_id.lower():
                    codec = 'AAC'
                elif 'ac3' in media.group_id.lower():
                    codec = 'AC3'
                elif 'ec3' in media.group_id.lower():
                    codec = 'EAC3'

            audio_tracks.append(AudioTrack(
                language=media.language if media.language else 'und',
                name=media.name if media.name else None,
                codec=codec,
                channels=None,  # Not typically in HLS manifest
                bitrate=None    # Not typically in HLS manifest
            ))

    return audio_tracks


def parse_subtitle_tracks(playlist: m3u8.M3U8) -> List[SubtitleTrack]:
    """
    Extract subtitle track information from HLS manifest.

    Args:
        playlist: Parsed M3U8 playlist

    Returns:
        List of SubtitleTrack objects
    """
    subtitle_tracks = []

    if not playlist.media:
        return subtitle_tracks

    for media in playlist.media:
        if media.type == 'SUBTITLES' or media.type == 'CLOSED-CAPTIONS':
            # Determine format
            format_type = 'WebVTT'  # Default for HLS
            if media.uri and '.vtt' in media.uri.lower():
                format_type = 'WebVTT'
            elif media.uri and '.ttml' in media.uri.lower():
                format_type = 'TTML'

            subtitle_tracks.append(SubtitleTrack(
                language=media.language if media.language else 'und',
                name=media.name if media.name else None,
                format=format_type,
                forced=media.forced == 'YES' if hasattr(media, 'forced') else False
            ))

    return subtitle_tracks


def parse_thumbnail_tracks(playlist: m3u8.M3U8) -> List[ThumbnailTrack]:
    """
    Extract thumbnail track information from HLS manifest.

    Args:
        playlist: Parsed M3U8 playlist

    Returns:
        List of ThumbnailTrack objects
    """
    thumbnail_tracks = []

    # Look for I-frame playlists
    if hasattr(playlist, 'iframe_playlists') and playlist.iframe_playlists:
        for iframe in playlist.iframe_playlists:
            resolution = None
            if hasattr(iframe, 'iframe_stream_info') and iframe.iframe_stream_info.resolution:
                width, height = iframe.iframe_stream_info.resolution
                resolution = f"{width}x{height}"

            thumbnail_tracks.append(ThumbnailTrack(
                resolution=resolution,
                url=iframe.uri if hasattr(iframe, 'uri') else None,
                format='JPEG'  # I-frames are typically JPEG
            ))

    return thumbnail_tracks


async def parse_hls_manifest(url: str) -> Dict:
    """
    Parse HLS manifest and extract all information.

    Args:
        url: URL of the HLS manifest

    Returns:
        Dictionary containing parsed information

    Raises:
        HTTPException: If parsing fails
    """
    try:
        # Fetch manifest content
        content = await fetch_manifest(url)

        # Parse with m3u8 library
        playlist = m3u8.loads(content)

        # Extract all information
        bitrates = parse_bitrates(playlist)
        audio_tracks = parse_audio_tracks(playlist)
        subtitle_tracks = parse_subtitle_tracks(playlist)
        thumbnail_tracks = parse_thumbnail_tracks(playlist)
        drm_info = parse_drm_info(playlist)

        return {
            'bitrates': bitrates,
            'audio_tracks': audio_tracks,
            'subtitle_tracks': subtitle_tracks,
            'thumbnail_tracks': thumbnail_tracks,
            'drm_info': drm_info,
            'raw_playlist': playlist  # Include for SCTE-35 parsing
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing HLS manifest: {str(e)}"
        )
