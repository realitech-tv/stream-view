"""
Tests for API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint"""

    def test_health_check_returns_200(self):
        """Health endpoint should return 200 OK"""
        response = client.get("/api/health")
        assert response.status_code == 200

    def test_health_check_returns_status(self):
        """Health endpoint should return status in response"""
        response = client.get("/api/health")
        assert "status" in response.json()
        assert response.json()["status"] == "healthy"


class TestAnalyzeEndpoint:
    """Tests for analyze endpoint"""

    def test_analyze_endpoint_exists(self):
        """Analyze endpoint should exist"""
        # Test that POST to /api/analyze doesn't return 404
        response = client.post("/api/analyze", json={"url": "invalid"})
        assert response.status_code != 404

    def test_analyze_rejects_invalid_url(self):
        """Should reject URLs without proper format"""
        response = client.post("/api/analyze", json={"url": "not-a-url"})
        assert response.status_code in [400, 422]

    def test_analyze_rejects_non_manifest_url(self):
        """Should reject URLs that don't end with .m3u8 or .mpd"""
        response = client.post("/api/analyze", json={"url": "https://example.com/video.mp4"})
        assert response.status_code in [400, 422]

    def test_analyze_accepts_m3u8_url(self):
        """Should accept valid .m3u8 URL format"""
        # This will likely fail to fetch, but should pass validation
        response = client.post("/api/analyze", json={"url": "https://example.com/stream.m3u8"})
        # Should not be a validation error (400/422)
        # May be 500 or other error due to network/parsing
        assert response.status_code not in [422]

    def test_analyze_accepts_mpd_url(self):
        """Should accept valid .mpd URL format"""
        response = client.post("/api/analyze", json={"url": "https://example.com/stream.mpd"})
        # Should not be a validation error
        assert response.status_code not in [422]

    @pytest.mark.parametrize("url_data", [
        {"url": ""},
        {"url": None},
        {},
        {"invalid_key": "value"}
    ])
    def test_analyze_validates_request_body(self, url_data):
        """Should validate request body structure"""
        response = client.post("/api/analyze", json=url_data)
        assert response.status_code == 422


class TestCORS:
    """Tests for CORS configuration"""

    def test_cors_headers_present(self):
        """CORS headers should be present in responses"""
        response = client.get("/api/health")
        # Check for common CORS headers
        assert "access-control-allow-origin" in [h.lower() for h in response.headers.keys()]

    def test_options_request_handled(self):
        """OPTIONS requests should be handled for CORS preflight"""
        response = client.options("/api/health")
        assert response.status_code in [200, 204]


class TestErrorHandling:
    """Tests for error handling"""

    def test_404_for_unknown_endpoint(self):
        """Unknown endpoints should return 404"""
        response = client.get("/api/unknown")
        assert response.status_code == 404

    def test_error_response_has_detail(self):
        """Error responses should include detail field"""
        response = client.post("/api/analyze", json={"url": "invalid"})
        if response.status_code >= 400:
            assert "detail" in response.json()
