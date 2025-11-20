"""
Pytest configuration and shared fixtures for backend tests.
"""
import json
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def test_data():
    """Load test data from test_data.json"""
    test_data_path = Path(__file__).parent.parent / "test_data.json"
    with open(test_data_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def hls_streams(test_data):
    """Get HLS test streams"""
    return test_data['hls_streams']


@pytest.fixture
def dash_streams(test_data):
    """Get DASH test streams"""
    return test_data['dash_streams']


@pytest.fixture
def sample_hls_manifest():
    """Sample HLS manifest content for testing"""
    return """#EXTM3U
#EXT-X-VERSION:6
#EXT-X-INDEPENDENT-SEGMENTS
#EXT-X-STREAM-INF:BANDWIDTH=2000000,RESOLUTION=1280x720,CODECS="avc1.64001f,mp4a.40.2"
https://example.com/720p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080,CODECS="avc1.640028,mp4a.40.2"
https://example.com/1080p.m3u8
#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio",LANGUAGE="en",NAME="English",DEFAULT=YES,URI="https://example.com/audio_en.m3u8"
#EXT-X-MEDIA:TYPE=SUBTITLES,GROUP-ID="subs",LANGUAGE="en",NAME="English",URI="https://example.com/subs_en.m3u8"
"""


@pytest.fixture
def sample_dash_manifest():
    """Sample DASH manifest content for testing"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<MPD xmlns="urn:mpeg:dash:schema:mpd:2011">
  <Period>
    <AdaptationSet mimeType="video/mp4">
      <Representation id="1" bandwidth="2000000" width="1280" height="720" codecs="avc1.64001f">
        <SegmentTemplate />
      </Representation>
      <Representation id="2" bandwidth="5000000" width="1920" height="1080" codecs="avc1.640028">
        <SegmentTemplate />
      </Representation>
    </AdaptationSet>
    <AdaptationSet mimeType="audio/mp4" lang="en">
      <Representation id="audio1" bandwidth="128000" codecs="mp4a.40.2">
        <SegmentTemplate />
      </Representation>
    </AdaptationSet>
  </Period>
</MPD>
"""


@pytest.fixture
def mock_httpx_client():
    """Mock httpx async client"""
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = ""
    mock_client.get.return_value = mock_response
    return mock_client


@pytest.fixture
def mock_av_container():
    """Mock PyAV container for FFmpeg tests"""
    mock_container = MagicMock()
    mock_video_stream = MagicMock()
    mock_video_stream.codec_context.name = "h264"
    mock_video_stream.codec_context.profile = "High"
    mock_video_stream.codec_context.width = 1920
    mock_video_stream.codec_context.height = 1080
    mock_video_stream.codec_context.framerate = 30
    mock_video_stream.codec_context.pix_fmt = "yuv420p"
    mock_video_stream.codec_context.bit_rate = 5000000
    mock_container.streams.video = [mock_video_stream]
    mock_container.format.name = "mpegts"
    mock_container.duration = 10000000  # microseconds
    return mock_container
