"""
API endpoints for stream analysis.
"""

import re
from typing import Union
from urllib.parse import urlparse, parse_qs
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from models.schemas import AnalyzeRequest, AnalyzeResponse, ErrorResponse
from services.hls_parser import parse_hls_manifest
from services.dash_parser import parse_dash_manifest
from services.scte35_parser import extract_scte35_markers
from services.ffmpeg_analyzer import analyze_video_fragments

router = APIRouter(prefix="/api", tags=["analysis"])


def validate_manifest_url(url: str) -> tuple[bool, str, str]:
    """
    Validate manifest URL format and determine type.
    Supports URLs with query parameters per TR-004.

    Args:
        url: The manifest URL to validate

    Returns:
        Tuple of (is_valid, manifest_type, error_message)
    """
    url_str = str(url)

    # Parse URL to get path component (before query parameters)
    try:
        parsed_url = urlparse(url_str)
        path = parsed_url.path
    except Exception as e:
        return False, '', f'Invalid URL format: {str(e)}'

    # Check for valid extension on the path only (TR-004)
    if path.endswith('.m3u8'):
        manifest_type = 'hls'
    elif path.endswith('.mpd'):
        manifest_type = 'dash'
    else:
        return False, '', 'URL path must end with .m3u8 (HLS) or .mpd (DASH)'

    # Validate query parameters are well-formed (TR-004)
    if parsed_url.query:
        try:
            # Parse query string to ensure it's well-formed
            parse_qs(parsed_url.query, strict_parsing=True)
        except ValueError as e:
            return False, '', f'Malformed query parameters: {str(e)}'

    # Security check: Prevent SSRF attacks
    # Only check the hostname/netloc for private IPs, not query parameters
    # This prevents false positives when query params contain encoded data
    hostname = parsed_url.netloc.lower()

    blocked_patterns = [
        r'localhost',
        r'127\.0\.0\.',
        r'0\.0\.0\.0',
        r'169\.254\.',  # Link-local
        r'10\.',        # Private network
        r'172\.(1[6-9]|2[0-9]|3[0-1])\.',  # Private network
        r'192\.168\.',  # Private network
        r'\[::1\]',     # IPv6 loopback
        r'\[::ffff:127\.0\.0\.1\]',  # IPv4-mapped IPv6 loopback
    ]

    for pattern in blocked_patterns:
        if re.search(pattern, hostname, re.IGNORECASE):
            return False, '', 'Access to private/internal URLs is not allowed'

    return True, manifest_type, ''


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_stream(request: AnalyzeRequest) -> Union[AnalyzeResponse, JSONResponse]:
    """
    Analyze a streaming manifest (HLS or DASH).

    This endpoint accepts a manifest URL, downloads and parses it,
    extracts SCTE-35 markers, and analyzes video fragments using FFmpeg.

    Args:
        request: AnalyzeRequest containing the manifest URL

    Returns:
        AnalyzeResponse with complete stream analysis

    Raises:
        HTTPException: For validation errors, network errors, or parsing failures
    """
    # Validate URL format and type
    is_valid, manifest_type, error_msg = validate_manifest_url(request.url)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    try:
        # Parse manifest based on type
        if manifest_type == 'hls':
            result = await parse_hls_manifest(str(request.url))
        else:  # dash
            result = await parse_dash_manifest(str(request.url))

        # Extract SCTE-35 markers
        scte35_markers = await extract_scte35_markers(
            str(request.url),
            manifest_type,
            result
        )

        # Analyze video fragments with FFmpeg
        video_metadata = await analyze_video_fragments(
            result,
            manifest_type
        )

        # Build response
        response = AnalyzeResponse(
            manifest_type=manifest_type,
            manifest_url=str(request.url),
            bitrates=result.get('bitrates', []),
            audio_tracks=result.get('audio_tracks', []),
            subtitle_tracks=result.get('subtitle_tracks', []),
            thumbnail_tracks=result.get('thumbnail_tracks', []),
            drm_info=result.get('drm_info'),
            scte35_markers=scte35_markers,
            video_metadata=video_metadata
        )

        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log error and return generic error response
        error_response = ErrorResponse(
            error="parsing_error",
            message="Failed to parse manifest",
            details=str(e)
        )
        return JSONResponse(
            status_code=500,
            content=error_response.model_dump()
        )
