"""
Pydantic models for Stream-View API requests and responses.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, HttpUrl, Field


class AnalyzeRequest(BaseModel):
    """Request model for stream analysis."""
    url: HttpUrl = Field(..., description="URL of the HLS (.m3u8) or DASH (.mpd) manifest")


class BitrateInfo(BaseModel):
    """Information about a specific bitrate level."""
    level: int = Field(..., description="Bitrate level index")
    bitrate: int = Field(..., description="Bitrate in bits per second")
    resolution: Optional[str] = Field(None, description="Resolution (e.g., 1920x1080)")
    codec: Optional[str] = Field(None, description="Video codec (e.g., H.264, H.265)")
    frame_rate: Optional[float] = Field(None, description="Frame rate in fps")
    audio_codec: Optional[str] = Field(None, description="Audio codec")


class AudioTrack(BaseModel):
    """Information about an audio track."""
    language: str = Field(..., description="Language code (e.g., en, es)")
    name: Optional[str] = Field(None, description="Track name")
    codec: Optional[str] = Field(None, description="Audio codec (e.g., AAC, AC3)")
    channels: Optional[int] = Field(None, description="Number of audio channels")
    bitrate: Optional[int] = Field(None, description="Audio bitrate in bits per second")


class SubtitleTrack(BaseModel):
    """Information about a subtitle track."""
    language: str = Field(..., description="Language code (e.g., en, es)")
    name: Optional[str] = Field(None, description="Track name")
    format: Optional[str] = Field(None, description="Subtitle format (e.g., WebVTT, TTML)")
    forced: bool = Field(False, description="Whether this is a forced subtitle track")


class ThumbnailTrack(BaseModel):
    """Information about a thumbnail/image track."""
    resolution: Optional[str] = Field(None, description="Thumbnail resolution")
    url: Optional[str] = Field(None, description="Thumbnail track URL")
    format: Optional[str] = Field(None, description="Image format (e.g., JPEG, PNG)")


class DRMInfo(BaseModel):
    """Information about DRM protection."""
    system: str = Field(..., description="DRM system (e.g., Widevine, PlayReady, FairPlay)")
    key_id: Optional[str] = Field(None, description="Key ID if available")
    license_url: Optional[str] = Field(None, description="License server URL")
    pssh: Optional[str] = Field(None, description="Protection System Specific Header (base64)")


class SCTE35Marker(BaseModel):
    """SCTE-35 marker information."""
    event_id: Optional[int] = Field(None, description="Event ID")
    pts: Optional[int] = Field(None, description="Presentation Time Stamp")
    command_type: str = Field(..., description="Splice command type (e.g., splice_insert, time_signal)")
    duration: Optional[float] = Field(None, description="Duration in seconds")
    upid: Optional[str] = Field(None, description="Unique Program ID")
    segmentation_type: Optional[str] = Field(None, description="Segmentation descriptor type")
    out_of_network: bool = Field(False, description="Out-of-network indicator")
    auto_return: bool = Field(False, description="Auto-return indicator")
    pre_roll: Optional[int] = Field(None, description="Pre-roll time in milliseconds")


class VideoMetadata(BaseModel):
    """Detailed video metadata from FFmpeg analysis."""
    level: int = Field(..., description="Bitrate level this metadata corresponds to")
    container_format: Optional[str] = Field(None, description="Container format (e.g., MPEG-TS, MP4)")
    video_codec: Optional[str] = Field(None, description="Video codec")
    codec_profile: Optional[str] = Field(None, description="Codec profile (e.g., High@L4.0)")
    resolution: Optional[str] = Field(None, description="Video resolution")
    frame_rate: Optional[float] = Field(None, description="Frame rate in fps")
    bitrate: Optional[int] = Field(None, description="Video bitrate in bits per second")
    color_space: Optional[str] = Field(None, description="Color space (e.g., yuv420p, bt709)")
    fragment_duration: Optional[float] = Field(None, description="Fragment/segment duration in seconds")
    file_size: Optional[int] = Field(None, description="Fragment file size in bytes")


class AnalyzeResponse(BaseModel):
    """Response model for stream analysis."""
    manifest_type: Literal["hls", "dash"] = Field(..., description="Type of manifest analyzed")
    manifest_url: str = Field(..., description="Original manifest URL")
    bitrates: List[BitrateInfo] = Field(default_factory=list, description="Available bitrate levels")
    audio_tracks: List[AudioTrack] = Field(default_factory=list, description="Available audio tracks")
    subtitle_tracks: List[SubtitleTrack] = Field(default_factory=list, description="Available subtitle tracks")
    thumbnail_tracks: List[ThumbnailTrack] = Field(default_factory=list, description="Available thumbnail tracks")
    drm_info: Optional[DRMInfo] = Field(None, description="DRM information if present")
    scte35_markers: List[SCTE35Marker] = Field(default_factory=list, description="SCTE-35 markers found")
    video_metadata: List[VideoMetadata] = Field(default_factory=list, description="Detailed video metadata")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[str] = Field(None, description="Additional error details")
