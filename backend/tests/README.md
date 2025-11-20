# Backend Tests

This directory contains the test suite for the Stream-View backend.

## Running Tests

### All Tests
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
pytest
```

### Specific Test File
```bash
pytest tests/test_api.py
```

### With Coverage
```bash
pytest --cov=. --cov-report=html
```

### Verbose Output
```bash
pytest -v
```

## Test Structure

- `conftest.py` - Shared fixtures and test configuration
- `test_api.py` - API endpoint tests
- `test_hls_parser.py` - HLS manifest parsing tests (placeholder)
- `test_dash_parser.py` - DASH manifest parsing tests (placeholder)
- `test_scte35_parser.py` - SCTE-35 extraction tests (placeholder)
- `test_ffmpeg_analyzer.py` - FFmpeg analysis tests (placeholder)

## Test Data

Test URLs are stored in `backend/test_data.json` and can be updated without modifying test code.

## Fixtures

Common fixtures are defined in `conftest.py`:
- `test_data` - Loads test URLs from test_data.json
- `hls_streams` - HLS test stream data
- `dash_streams` - DASH test stream data
- `sample_hls_manifest` - Sample HLS manifest content
- `sample_dash_manifest` - Sample DASH manifest content
- `mock_httpx_client` - Mocked HTTP client
- `mock_av_container` - Mocked PyAV container

## Test Coverage Goals

Target: > 80% code coverage

Current coverage can be checked with:
```bash
pytest --cov=. --cov-report=term-missing
```

## Notes

- Some CORS tests may fail with TestClient (this is expected)
- Real network tests should be mocked for unit tests
- Integration tests can use real URLs from test_data.json
