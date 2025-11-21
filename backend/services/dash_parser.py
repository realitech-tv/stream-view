"""
DASH manifest parser service.

Parses MPEG-DASH (.mpd) manifests and extracts stream information including
bitrates, audio tracks, subtitles, and DRM information.
"""

import httpx
from typing import Dict, List, Optional
from xml.etree import ElementTree as ET
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


def get_namespace(root: ET.Element) -> Dict[str, str]:
    """
    Extract XML namespaces from MPD root element.

    Args:
        root: MPD root element

    Returns:
        Dictionary of namespace prefixes to URIs
    """
    namespaces = {}
    # Default DASH namespace
    if root.tag.startswith('{'):
        default_ns = root.tag[1:root.tag.index('}')]
        namespaces['mpd'] = default_ns
    else:
        namespaces['mpd'] = 'urn:mpeg:dash:schema:mpd:2011'

    # Extract all namespaces from root attributes
    for key, value in root.attrib.items():
        if key.startswith('{http://www.w3.org/2000/xmlns/}'):
            prefix = key.split('}')[1]
            namespaces[prefix] = value

    return namespaces


def parse_drm_info(root: ET.Element, namespaces: Dict[str, str]) -> Optional[DRMInfo]:
    """
    Extract DRM information from DASH manifest.

    Args:
        root: MPD root element
        namespaces: XML namespaces

    Returns:
        DRMInfo if DRM is detected, None otherwise
    """
    # Look for ContentProtection elements (try both with and without namespace)
    content_protections = root.findall('.//mpd:ContentProtection', namespaces)
    if not content_protections:
        # Try without namespace prefix (some manifests don't use namespaces)
        content_protections = root.findall('.//ContentProtection')

    # First pass: collect key_id from any ContentProtection element
    common_key_id = None
    for cp in content_protections:
        kid = (
            cp.get('default_KID') or
            cp.get('kid') or
            cp.get('{urn:mpeg:cenc:2013}default_KID')
        )
        if kid:
            common_key_id = kid
            break

    # Second pass: find specific DRM system
    for cp in content_protections:
        scheme_id_uri = cp.get('schemeIdUri', '')

        # Determine DRM system
        drm_system = None
        scheme_id_lower = scheme_id_uri.lower()

        # Check for Widevine (both by name and UUID)
        if 'widevine' in scheme_id_lower or 'edef8ba9-79d6-4ace-a3c8-27dcd51d21ed' in scheme_id_lower:
            drm_system = 'Widevine'
        # Check for PlayReady (both by name and UUID)
        elif 'playready' in scheme_id_lower or '9a04f079-9840-4286-ab92-e65be0885f95' in scheme_id_lower:
            drm_system = 'PlayReady'
        elif 'fairplay' in scheme_id_lower:
            drm_system = 'FairPlay'
        elif 'clearkey' in scheme_id_lower:
            drm_system = 'ClearKey'

        # If we found a specific DRM system (not generic CENC), extract info and return
        if drm_system:
            # Extract key ID (check current element, or use common key_id)
            key_id = (
                cp.get('default_KID') or
                cp.get('kid') or
                cp.get('{urn:mpeg:cenc:2013}default_KID') or
                common_key_id
            )

            # Look for PSSH box (try multiple approaches)
            pssh = None
            # Try with cenc namespace if available
            if 'cenc' in namespaces:
                pssh_elem = cp.find('.//cenc:pssh', namespaces)
                if pssh_elem is not None and pssh_elem.text:
                    pssh = pssh_elem.text.strip()

            # Try without namespace
            if not pssh:
                pssh_elem = cp.find('.//{urn:mpeg:cenc:2013}pssh')
                if pssh_elem is not None and pssh_elem.text:
                    pssh = pssh_elem.text.strip()

            # Look for license URL (mspr namespace for PlayReady)
            license_url = None
            if 'playready' in scheme_id_uri.lower():
                laurl = cp.find('.//mspr:laurl', namespaces)
                if laurl is not None:
                    license_url = laurl.text

            return DRMInfo(
                system=drm_system,
                key_id=key_id,
                license_url=license_url,
                pssh=pssh
            )

    return None


def parse_codec_string(codecs: str, mime_type: str) -> str:
    """
    Parse codec string to human-readable format.

    Args:
        codecs: Codec string from manifest
        mime_type: MIME type of the representation

    Returns:
        Human-readable codec name
    """
    if not codecs:
        return None

    codecs_lower = codecs.lower()

    if codecs_lower.startswith('avc'):
        return 'H.264'
    elif codecs_lower.startswith('hvc') or codecs_lower.startswith('hev'):
        return 'H.265'
    elif codecs_lower.startswith('vp09') or codecs_lower.startswith('vp9'):
        return 'VP9'
    elif codecs_lower.startswith('av01'):
        return 'AV1'
    elif codecs_lower.startswith('mp4a'):
        return 'AAC'
    elif codecs_lower.startswith('ac-3'):
        return 'AC3'
    elif codecs_lower.startswith('ec-3'):
        return 'EAC3'
    elif 'opus' in codecs_lower:
        return 'Opus'

    return codecs


def parse_bitrates(root: ET.Element, namespaces: Dict[str, str]) -> List[BitrateInfo]:
    """
    Extract bitrate information from DASH manifest.

    Args:
        root: MPD root element
        namespaces: XML namespaces

    Returns:
        List of BitrateInfo objects
    """
    bitrates = []
    level = 0

    # Find all video adaptation sets
    for period in root.findall('.//mpd:Period', namespaces):
        for adaptation_set in period.findall('.//mpd:AdaptationSet', namespaces):
            # Check if this is a video adaptation set
            content_type = adaptation_set.get('contentType', '')
            mime_type = adaptation_set.get('mimeType', '')

            is_video = 'video' in content_type or 'video' in mime_type

            # Also check representations
            if not is_video:
                for rep in adaptation_set.findall('.//mpd:Representation', namespaces):
                    rep_mime = rep.get('mimeType', mime_type)
                    if 'video' in rep_mime:
                        is_video = True
                        break

            if not is_video:
                continue

            # Extract video representations
            for representation in adaptation_set.findall('.//mpd:Representation', namespaces):
                bandwidth = representation.get('bandwidth')
                width = representation.get('width')
                height = representation.get('height')
                codecs = representation.get('codecs') or adaptation_set.get('codecs')
                frame_rate = representation.get('frameRate') or adaptation_set.get('frameRate')

                # Parse resolution
                resolution = None
                if width and height:
                    resolution = f"{width}x{height}"

                # Parse codec
                rep_mime = representation.get('mimeType') or mime_type
                codec = parse_codec_string(codecs, rep_mime) if codecs else None

                # Parse frame rate
                fps = None
                if frame_rate:
                    try:
                        if '/' in str(frame_rate):
                            num, den = frame_rate.split('/')
                            fps = float(num) / float(den)
                        else:
                            fps = float(frame_rate)
                    except:
                        pass

                bitrates.append(BitrateInfo(
                    level=level,
                    bitrate=int(bandwidth) if bandwidth else 0,
                    resolution=resolution,
                    codec=codec,
                    frame_rate=fps,
                    audio_codec=None
                ))
                level += 1

    return bitrates


def parse_audio_tracks(root: ET.Element, namespaces: Dict[str, str]) -> List[AudioTrack]:
    """
    Extract audio track information from DASH manifest.

    Args:
        root: MPD root element
        namespaces: XML namespaces

    Returns:
        List of AudioTrack objects
    """
    audio_tracks = []

    # Find all audio adaptation sets
    for period in root.findall('.//mpd:Period', namespaces):
        for adaptation_set in period.findall('.//mpd:AdaptationSet', namespaces):
            # Check if this is an audio adaptation set
            content_type = adaptation_set.get('contentType', '')
            mime_type = adaptation_set.get('mimeType', '')

            is_audio = 'audio' in content_type or 'audio' in mime_type

            # Also check representations
            if not is_audio:
                for rep in adaptation_set.findall('.//mpd:Representation', namespaces):
                    rep_mime = rep.get('mimeType', mime_type)
                    if 'audio' in rep_mime:
                        is_audio = True
                        break

            if not is_audio:
                continue

            # Extract language
            language = adaptation_set.get('lang', 'und')

            # Extract codec from first representation
            codec = None
            channels = None
            bitrate = None

            representation = adaptation_set.find('.//mpd:Representation', namespaces)
            if representation is not None:
                codecs = representation.get('codecs') or adaptation_set.get('codecs')
                rep_mime = representation.get('mimeType') or mime_type
                codec = parse_codec_string(codecs, rep_mime) if codecs else None

                # Get audio configuration
                audio_config = representation.find('.//mpd:AudioChannelConfiguration', namespaces)
                if audio_config is not None:
                    value = audio_config.get('value')
                    if value:
                        try:
                            channels = int(value)
                        except:
                            pass

                bandwidth = representation.get('bandwidth')
                if bandwidth:
                    bitrate = int(bandwidth)

            # Get track name from Label or other attributes
            name = None
            label = adaptation_set.find('.//mpd:Label', namespaces)
            if label is not None and label.text:
                name = label.text.strip()

            audio_tracks.append(AudioTrack(
                language=language,
                name=name,
                codec=codec,
                channels=channels,
                bitrate=bitrate
            ))

    return audio_tracks


def parse_subtitle_tracks(root: ET.Element, namespaces: Dict[str, str]) -> List[SubtitleTrack]:
    """
    Extract subtitle track information from DASH manifest.

    Args:
        root: MPD root element
        namespaces: XML namespaces

    Returns:
        List of SubtitleTrack objects
    """
    subtitle_tracks = []

    # Find all text/subtitle adaptation sets
    for period in root.findall('.//mpd:Period', namespaces):
        for adaptation_set in period.findall('.//mpd:AdaptationSet', namespaces):
            # Check if this is a text/subtitle adaptation set
            content_type = adaptation_set.get('contentType', '')
            mime_type = adaptation_set.get('mimeType', '')

            is_subtitle = 'text' in content_type or 'application' in mime_type

            if not is_subtitle:
                continue

            # Extract language
            language = adaptation_set.get('lang', 'und')

            # Determine format from MIME type
            format_type = None
            if 'wvtt' in mime_type or 'vtt' in mime_type:
                format_type = 'WebVTT'
            elif 'ttml' in mime_type:
                format_type = 'TTML'
            elif 'stpp' in mime_type:
                format_type = 'TTML'

            # Get track name
            name = None
            label = adaptation_set.find('.//mpd:Label', namespaces)
            if label is not None and label.text:
                name = label.text.strip()

            subtitle_tracks.append(SubtitleTrack(
                language=language,
                name=name,
                format=format_type,
                forced=False  # DASH doesn't typically indicate forced subs
            ))

    return subtitle_tracks


def parse_thumbnail_tracks(root: ET.Element, namespaces: Dict[str, str]) -> List[ThumbnailTrack]:
    """
    Extract thumbnail track information from DASH manifest.

    Args:
        root: MPD root element
        namespaces: XML namespaces

    Returns:
        List of ThumbnailTrack objects
    """
    thumbnail_tracks = []

    # Look for image adaptation sets
    for period in root.findall('.//mpd:Period', namespaces):
        for adaptation_set in period.findall('.//mpd:AdaptationSet', namespaces):
            # Check if this is an image adaptation set
            content_type = adaptation_set.get('contentType', '')
            mime_type = adaptation_set.get('mimeType', '')

            is_image = 'image' in content_type or 'image' in mime_type

            if not is_image:
                continue

            # Get first representation
            representation = adaptation_set.find('.//mpd:Representation', namespaces)
            if representation is not None:
                width = representation.get('width')
                height = representation.get('height')

                resolution = None
                if width and height:
                    resolution = f"{width}x{height}"

                rep_mime = representation.get('mimeType') or mime_type
                format_type = 'JPEG'
                if 'png' in rep_mime.lower():
                    format_type = 'PNG'

                thumbnail_tracks.append(ThumbnailTrack(
                    resolution=resolution,
                    url=None,  # URL would be in BaseURL or SegmentTemplate
                    format=format_type
                ))

    return thumbnail_tracks


async def parse_dash_manifest(url: str) -> Dict:
    """
    Parse DASH manifest and extract all information.

    Args:
        url: URL of the DASH manifest

    Returns:
        Dictionary containing parsed information

    Raises:
        HTTPException: If parsing fails
    """
    try:
        # Fetch manifest content
        content = await fetch_manifest(url)

        # Parse XML
        root = ET.fromstring(content)
        namespaces = get_namespace(root)

        # Extract all information
        bitrates = parse_bitrates(root, namespaces)
        audio_tracks = parse_audio_tracks(root, namespaces)
        subtitle_tracks = parse_subtitle_tracks(root, namespaces)
        thumbnail_tracks = parse_thumbnail_tracks(root, namespaces)
        drm_info = parse_drm_info(root, namespaces)

        return {
            'bitrates': bitrates,
            'audio_tracks': audio_tracks,
            'subtitle_tracks': subtitle_tracks,
            'thumbnail_tracks': thumbnail_tracks,
            'drm_info': drm_info,
            'raw_xml': root,  # Include for SCTE-35 parsing
            'namespaces': namespaces
        }

    except HTTPException:
        raise
    except ET.ParseError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid XML in DASH manifest: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing DASH manifest: {str(e)}"
        )
