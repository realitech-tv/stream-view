# Stream-View Implementation Plan

## Overview

This document outlines the detailed implementation plan for building the stream-view application - a web-based video stream analyzer that supports both HLS (.m3u8) and MPEG-DASH (.mpd) manifests.

## Technology Stack

**Backend:**
- Python 3.11+
- FastAPI (async web framework)
- Uvicorn (ASGI server)
- PyAV (FFmpeg native bindings)
- threefive (SCTE-35 parsing)
- m3u8 (HLS manifest parsing)
- mpegdash (DASH manifest parsing)
- httpx (async HTTP client)

**Frontend:**
- React 18+
- Vite (build tool)
- TypeScript 5+
- Tailwind CSS (styling)
- Axios (HTTP client)

**Infrastructure:**
- Docker & Docker Compose
- FFmpeg 6+

## Implementation Phases

### Phase 1: Project Foundation (Days 1-2)

#### 1.1 Project Structure Setup
**Goal:** Establish the basic project structure and directory layout

**Tasks:**
- Create `backend/` directory with Python FastAPI structure
  - `backend/main.py` - FastAPI application entry point
  - `backend/api/` - API route handlers
  - `backend/services/` - Business logic (parsers, analyzers)
  - `backend/models/` - Pydantic models for requests/responses
  - `backend/tests/` - Test suite
- Create `frontend/` directory with React + Vite + TypeScript
  - `frontend/src/components/` - React components
  - `frontend/src/services/` - API client
  - `frontend/src/types/` - TypeScript type definitions
  - `frontend/src/styles/` - CSS/Tailwind configurations
- Set up `.gitignore` for Python, Node.js, and Docker artifacts
- Create initial `README.md` with quick start guide

**Acceptance Criteria:**
- Directory structure matches planned architecture
- `.gitignore` prevents committing build artifacts, virtual environments, node_modules
- README contains basic project description and setup instructions

#### 1.2 Backend Initialization
**Goal:** Set up Python backend with all required dependencies

**Tasks:**
- Initialize Python project with `requirements.txt`
- Add core dependencies:
  ```
  fastapi>=0.104.0
  uvicorn[standard]>=0.24.0
  av>=11.0.0
  threefive>=2.4.0
  m3u8>=4.0.0
  mpegdash>=0.3.0
  httpx>=0.25.0
  pytest>=7.4.0
  pytest-asyncio>=0.21.0
  pydantic>=2.5.0
  ```
- Create basic FastAPI app structure:
  ```python
  from fastapi import FastAPI
  from fastapi.middleware.cors import CORSMiddleware

  app = FastAPI(title="Stream-View API")

  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],  # Configure for production
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )

  @app.get("/api/health")
  async def health_check():
      return {"status": "healthy"}
  ```
- Set up CORS middleware for frontend communication
- Create `pytest.ini` and test configuration

**Acceptance Criteria:**
- `pip install -r requirements.txt` succeeds
- `uvicorn main:app --reload` starts server successfully
- Health check endpoint `/api/health` returns 200 OK
- CORS headers present in responses

#### 1.3 Frontend Initialization
**Goal:** Set up React frontend with TypeScript and Tailwind CSS

**Tasks:**
- Initialize React + Vite project: `npm create vite@latest frontend -- --template react-ts`
- Install dependencies:
  ```bash
  npm install axios
  npm install -D tailwindcss postcss autoprefixer
  npx tailwindcss init -p
  ```
- Configure Tailwind CSS in `tailwind.config.js`:
  ```javascript
  export default {
    content: [
      "./index.html",
      "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
      extend: {},
    },
    plugins: [],
  }
  ```
- Create basic component structure:
  - `src/components/Header.tsx` - Logo and title
  - `src/components/StreamAnalyzer.tsx` - Main analysis component
  - `src/components/ResultsDisplay.tsx` - Results table display
  - `src/services/api.ts` - API client service
- Add Realitech logo asset

**Acceptance Criteria:**
- `npm run dev` starts development server
- TypeScript compilation succeeds with strict mode
- Tailwind CSS styles are applied
- Basic layout renders in browser

---

### Phase 2: Backend Core Development (Days 3-5)

#### 2.1 API Structure
**Goal:** Create the main analysis API endpoint with proper validation and error handling

**Tasks:**
- Create `/api/analyze` POST endpoint accepting manifest URL
- Implement Pydantic models:
  ```python
  class AnalyzeRequest(BaseModel):
      url: HttpUrl

  class AnalyzeResponse(BaseModel):
      manifest_type: Literal["hls", "dash"]
      bitrates: List[BitrateInfo]
      audio_tracks: List[AudioTrack]
      subtitle_tracks: List[SubtitleTrack]
      thumbnail_tracks: List[ThumbnailTrack]
      drm_info: Optional[DRMInfo]
      scte35_markers: List[SCTE35Marker]
      video_metadata: List[VideoMetadata]
  ```
- Add URL validation (must end with `.m3u8` or `.mpd`)
- Implement timeout protection (30s default)
- Add manifest size limits (10MB max)
- Create error response models with helpful messages

**Acceptance Criteria:**
- POST to `/api/analyze` with valid URL returns 200
- Invalid URLs return 400 with clear error message
- Requests timeout after configured duration
- Large manifests are rejected with appropriate error
- API documentation available at `/docs` (FastAPI auto-generated)

#### 2.2 HLS Parsing (US-002)
**Goal:** Parse HLS manifests and extract all required information

**Tasks:**
- Create `services/hls_parser.py`:
  - Function to fetch manifest with httpx (async)
  - Parse manifest using m3u8 library
  - Extract variant streams (bitrates, resolutions, codecs)
  - Parse audio tracks from `EXT-X-MEDIA` tags (TYPE=AUDIO)
  - Parse subtitle tracks from `EXT-X-MEDIA` tags (TYPE=SUBTITLES)
  - Parse thumbnail tracks from `EXT-X-I-FRAMES-ONLY` or `EXT-X-IMAGE-STREAM-INF`
  - Detect DRM from `EXT-X-KEY` tags (METHOD=SAMPLE-AES, etc.)
- Handle edge cases:
  - Master vs. media playlists
  - Missing optional fields
  - Malformed manifests
- Add comprehensive error handling with specific error messages

**Acceptance Criteria:**
- Successfully parses BBC News HLS manifest (test data)
- Extracts all bitrate levels with resolution and codec info
- Identifies audio tracks with language and name
- Detects subtitle tracks
- Identifies DRM encryption when present
- Returns structured data matching response model
- Gracefully handles parsing errors

#### 2.3 DASH Parsing (US-003)
**Goal:** Parse DASH manifests and extract all required information

**Tasks:**
- Create `services/dash_parser.py`:
  - Function to fetch manifest with httpx (async)
  - Parse MPD XML using mpegdash library
  - Extract AdaptationSets and Representations
  - Identify video representations (bitrates, resolutions, codecs)
  - Parse audio AdaptationSets (languages, codecs)
  - Parse subtitle AdaptationSets (languages, formats)
  - Parse thumbnail/image AdaptationSets
  - Detect DRM from `ContentProtection` elements (Widevine, PlayReady, etc.)
- Handle edge cases:
  - Live vs. VOD presentations
  - SegmentTemplate vs. SegmentList vs. SegmentBase
  - Multiple periods
- Add comprehensive error handling

**Acceptance Criteria:**
- Successfully parses BBC Two DASH manifest (test data)
- Extracts all video representations with bitrate/resolution/codec
- Identifies audio adaptations with language information
- Detects subtitles
- Identifies DRM schemes (Widevine, PlayReady, etc.)
- Returns structured data matching response model
- Gracefully handles parsing errors

#### 2.4 SCTE-35 Extraction (US-004)
**Goal:** Extract and parse SCTE-35 markers from both HLS and DASH streams

**Tasks:**
- Create `services/scte35_parser.py`:
  - For HLS: Parse `EXT-X-DATERANGE` tags with SCTE35 data
  - For DASH: Parse `EventStream` elements with SCTE35 scheme
  - Use threefive library to decode SCTE-35 binary data
  - Extract required fields:
    - Splice commands (splice_insert, splice_null, time_signal)
    - PTS (Presentation Time Stamp)
    - Pre-roll time (duration before splice point)
    - Out-of-network indicator
    - Return indicator (auto_return)
    - UPID (Unique Program ID)
    - Segmentation descriptors (segment type, duration)
    - Event ID
    - Break duration
- Handle missing or malformed SCTE-35 data
- Support multiple SCTE-35 markers per manifest

**Acceptance Criteria:**
- Successfully extracts SCTE-35 from HLS manifests with `EXT-X-DATERANGE`
- Successfully extracts SCTE-35 from DASH manifests with `EventStream`
- Decodes all required SCTE-35 fields
- Handles manifests without SCTE-35 (returns empty list)
- Handles malformed SCTE-35 data gracefully
- Returns structured list of SCTE-35 markers

#### 2.5 FFmpeg Integration (US-005)
**Goal:** Use FFmpeg to analyze video fragments and extract detailed metadata

**Tasks:**
- Create `services/ffmpeg_analyzer.py`:
  - Use PyAV (av library) to probe video streams
  - Download 1-10 video segments/fragments from stream
  - For HLS: Download .ts segments
  - For DASH: Download initialization segment + media segments
  - Extract metadata:
    - Container format (MPEG-TS, MP4, etc.)
    - Fragment/segment duration
    - Average bitrate (from fragment size / duration)
    - File size
    - Video codec (H.264, H.265, VP9, AV1)
    - Codec profile and level (High@L4.0, Main10@L5.1, etc.)
    - Resolution (width x height)
    - Frame rate (fps)
    - Bit rate (video stream bitrate)
    - Color space (yuv420p, bt709, etc.)
  - Handle DRM-encrypted fragments:
    - Can analyze init segments (not encrypted)
    - Extract what's possible from manifest
    - Gracefully skip encrypted media segments
- Implement caching to avoid re-downloading same fragments
- Add timeout protection for downloads

**Acceptance Criteria:**
- Successfully downloads and analyzes fragments from HLS streams
- Successfully downloads and analyzes fragments from DASH streams
- Extracts all required metadata fields
- Handles DRM-encrypted streams (extracts available info)
- Respects timeout limits
- Returns structured metadata for each bitrate level
- Works with both live and VOD streams

---

### Phase 3: Frontend Development (Days 6-8)

#### 3.1 UI Layout (US-001)
**Goal:** Create the main single-page layout with modern design

**Tasks:**
- Create `components/Header.tsx`:
  - Realitech logo in top-left corner
  - App title "Stream-View"
  - Clean, professional styling with Tailwind
- Create `components/StreamAnalyzer.tsx`:
  - URL input field (full width, modern styling)
  - "View" button (primary call-to-action styling)
  - Form validation (client-side)
  - Loading state indicator
- Create main layout in `App.tsx`:
  - Header at top
  - Main content area with StreamAnalyzer
  - Results display area below
- Implement responsive design:
  - Desktop-first (primary use case)
  - Tablet-friendly
  - Clean spacing and typography
- Add modern UI elements:
  - Rounded corners, shadows, gradients
  - Smooth transitions and hover effects
  - Professional color scheme

**Acceptance Criteria:**
- Realitech logo displayed in top-left
- Single-page layout (no routing required)
- Modern, clean design using Tailwind CSS
- URL input and "View" button clearly visible
- Responsive on desktop and tablet
- Professional appearance suitable for streaming engineers

#### 3.2 Stream Analysis Display
**Goal:** Display analysis results in structured, readable format

**Tasks:**
- Create `components/BitrateTable.tsx`:
  - Multi-column table component
  - Three-column format: Level | Property | Value
  - Display for each bitrate level:
    - Resolution
    - Codec
    - Bitrate
    - Frame rate
  - Responsive table layout
- Create `components/TrackInfo.tsx`:
  - Display audio tracks (language, codec, channels)
  - Display subtitle tracks (language, format)
  - Display thumbnail tracks if present
- Create `components/DRMInfo.tsx`:
  - Display DRM scheme (Widevine, PlayReady, FairPlay, etc.)
  - Show encryption method
  - Display key system information
- Create `components/SCTE35Display.tsx`:
  - Table format for SCTE-35 markers
  - Columns: Event ID | PTS | Command | Duration | UPID | Descriptors
  - Expandable rows for detailed segmentation info
- Create `components/VideoMetadata.tsx`:
  - Table showing video fragment analysis
  - Display: Container | Codec | Profile | Resolution | FPS | Color Space
  - Group by bitrate level
- Create `components/ResultsDisplay.tsx`:
  - Orchestrates all result components
  - Sections: Overview, Bitrates, Tracks, DRM, SCTE-35, Video Analysis
  - Collapsible sections for better organization
  - Clean spacing between sections

**Acceptance Criteria:**
- Results display in structured, readable tables
- All required information from US-002 through US-005 displayed
- Tables use modern styling (borders, alternating rows, etc.)
- Collapsible sections for better information organization
- Professional layout suitable for technical users
- Data formatted appropriately (bitrates in Mbps, durations in seconds, etc.)

#### 3.3 Error Handling & UX
**Goal:** Provide excellent user experience with clear feedback

**Tasks:**
- Create `components/ErrorMessage.tsx`:
  - Display error messages with clear styling (red border, icon)
  - Different message types: validation, network, parsing
  - Helpful suggestions (e.g., "Check URL format and try again")
- Implement form validation:
  - Real-time URL format validation
  - Check for .m3u8 or .mpd extension
  - Visual feedback (red border, error text)
- Add loading states:
  - Spinner during analysis
  - Progress indication ("Fetching manifest...", "Parsing...", "Analyzing...")
  - Disable button during processing
- Implement error boundaries:
  - Catch React errors gracefully
  - Display fallback UI
- Add success feedback:
  - Smooth transition to results
  - Clear indication that analysis is complete

**Acceptance Criteria:**
- Invalid URLs show clear error messages
- Loading states display during API calls
- Errors don't crash the application
- Users understand what went wrong and how to fix it
- Smooth transitions between states (idle, loading, success, error)

---

### Phase 4: Docker & Deployment (Days 9-10)

#### 4.1 Backend Dockerfile
**Goal:** Create production-ready Docker image for Python backend

**Tasks:**
- Create `backend/Dockerfile`:
  ```dockerfile
  FROM python:3.11-slim

  # Install FFmpeg
  RUN apt-get update && apt-get install -y \
      ffmpeg \
      && rm -rf /var/lib/apt/lists/*

  WORKDIR /app

  # Install Python dependencies
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt

  # Copy application code
  COPY . .

  EXPOSE 8000

  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```
- Configure Uvicorn for production:
  - Set appropriate worker count
  - Configure logging
  - Set timeouts
- Add health check endpoint for container health monitoring

**Acceptance Criteria:**
- Dockerfile builds successfully
- FFmpeg installed and accessible
- Python dependencies installed
- Container starts and serves API
- Health check endpoint responds

#### 4.2 Frontend Dockerfile
**Goal:** Create optimized production build with nginx

**Tasks:**
- Create `frontend/Dockerfile`:
  ```dockerfile
  # Build stage
  FROM node:20-alpine AS builder
  WORKDIR /app
  COPY package*.json ./
  RUN npm ci
  COPY . .
  RUN npm run build

  # Production stage
  FROM nginx:alpine
  COPY --from=builder /app/dist /usr/share/nginx/html
  COPY nginx.conf /etc/nginx/conf.d/default.conf
  EXPOSE 80
  CMD ["nginx", "-g", "daemon off;"]
  ```
- Create `nginx.conf`:
  - Configure SPA routing (try_files)
  - Proxy /api requests to backend
  - Enable gzip compression
  - Set cache headers for static assets
- Optimize production build (Vite handles this)

**Acceptance Criteria:**
- Multi-stage build produces small image
- Static assets served efficiently by nginx
- SPA routing works correctly
- API requests proxied to backend
- Production build optimized (minified, tree-shaken)

#### 4.3 Docker Compose
**Goal:** Enable one-command deployment of entire application

**Tasks:**
- Create `docker-compose.yml`:
  ```yaml
  version: '3.8'

  services:
    backend:
      build: ./backend
      ports:
        - "8000:8000"
      environment:
        - ENVIRONMENT=production
      volumes:
        - ./backend:/app
      restart: unless-stopped

    frontend:
      build: ./frontend
      ports:
        - "80:80"
      depends_on:
        - backend
      restart: unless-stopped
  ```
- Configure networking between services
- Set environment variables
- Add volume mounts for development
- Configure restart policies

**Acceptance Criteria:**
- `docker-compose up` builds and starts both containers
- Frontend accessible at http://localhost
- Backend accessible at http://localhost:8000
- Services can communicate
- Logs visible with `docker-compose logs`
- `docker-compose down` stops all services cleanly

---

### Phase 5: Testing (Days 11-12)

#### 5.1 Backend Testing
**Goal:** Comprehensive test coverage for backend services

**Tasks:**
- Create `tests/test_hls_parser.py`:
  - Test HLS manifest parsing with real test data
  - Test bitrate extraction
  - Test audio/subtitle track parsing
  - Test DRM detection
  - Test error handling (malformed manifests, network errors)
  - Mock httpx requests for unit tests
- Create `tests/test_dash_parser.py`:
  - Test DASH manifest parsing
  - Test adaptation set extraction
  - Test DRM detection (ContentProtection)
  - Test error handling
- Create `tests/test_scte35_parser.py`:
  - Test SCTE-35 extraction from HLS
  - Test SCTE-35 extraction from DASH
  - Test parsing of all required fields
  - Test handling of missing SCTE-35 data
- Create `tests/test_ffmpeg_analyzer.py`:
  - Test fragment download and analysis
  - Test metadata extraction
  - Test handling of DRM-encrypted content
  - Mock PyAV for faster tests
- Create `tests/test_api.py`:
  - Test `/api/analyze` endpoint
  - Test input validation
  - Test timeout handling
  - Test size limit enforcement
  - Integration tests with mocked services

**Acceptance Criteria:**
- All tests pass with `pytest`
- Test coverage > 80%
- Tests run quickly (< 30 seconds)
- Tests are independent and repeatable
- Both unit tests (mocked) and integration tests (real parsing)

#### 5.2 Test Data Management
**Goal:** Externalize test URLs for easy maintenance

**Tasks:**
- Create `backend/test_data.json`:
  ```json
  {
    "hls_streams": [
      {
        "name": "Freevee Euronews",
        "url": "https://...",
        "type": "live",
        "drm": true
      },
      ...
    ],
    "dash_streams": [
      {
        "name": "BBC Two",
        "url": "https://...",
        "type": "live",
        "drm": false
      },
      ...
    ]
  }
  ```
- Copy all test URLs from requirements.md
- Create test helper to load test data:
  ```python
  def load_test_data():
      with open('test_data.json') as f:
          return json.load(f)
  ```
- Use in parameterized tests:
  ```python
  @pytest.mark.parametrize("stream", load_test_data()['hls_streams'])
  def test_hls_stream(stream):
      result = parse_hls(stream['url'])
      assert result is not None
  ```

**Acceptance Criteria:**
- All test URLs from requirements stored in JSON
- Tests load data dynamically
- Easy to add new test URLs without code changes
- Tests cover both HLS and DASH
- Tests cover both live and VOD
- Tests cover both DRM and non-DRM

#### 5.3 Frontend Testing
**Goal:** Ensure UI meets modern design standards and functions correctly

**Tasks:**
- Set up Playwright:
  ```bash
  npm install -D @playwright/test
  npx playwright install
  ```
- Create `tests/e2e/ui.spec.ts`:
  - Test: Page loads with correct layout
  - Test: Realitech logo visible in top-left
  - Test: URL input and View button present
  - Test: URL validation works
  - Test: Error messages display correctly
  - Test: Loading states show during analysis
  - Test: Results display after successful analysis
  - Test: Tables render with correct structure
- Create `tests/e2e/accessibility.spec.ts`:
  - Test: Proper heading hierarchy
  - Test: Form labels associated correctly
  - Test: Keyboard navigation works
  - Test: Color contrast meets standards
- Create visual regression tests:
  - Capture screenshots of key UI states
  - Compare against baseline

**Acceptance Criteria:**
- Playwright tests pass
- UI conforms to modern design standards
- Responsive layout verified
- Accessibility standards met
- Visual regression tests establish baseline
- Tests can run in CI/CD

---

### Phase 6: Documentation (Day 13)

#### 6.1 User Documentation (US-006)
**Goal:** Enable users to deploy and operate the application

**Tasks:**
- Update `README.md`:
  - Project description and features
  - Prerequisites (Docker, Docker Compose)
  - Quick start: `docker-compose up`
  - Access instructions (http://localhost)
  - How to stop: `docker-compose down`
  - Troubleshooting common issues
  - Example usage with test URLs
- Create `docs/deployment.md`:
  - Detailed deployment instructions
  - Environment variable configuration
  - Production deployment considerations
  - Cloud deployment options (AWS, GCP, Azure)
  - Updating the application
- Create `docs/user-guide.md`:
  - How to use the application
  - Understanding the results
  - Supported stream formats
  - Known limitations

**Acceptance Criteria:**
- Non-technical user can deploy with README alone
- All deployment scenarios documented
- Troubleshooting guide covers common issues
- Examples use actual test URLs from requirements

#### 6.2 Technical Documentation
**Goal:** Enable developers to understand and maintain the codebase

**Tasks:**
- Create `docs/architecture.md`:
  - System architecture diagram
  - Component descriptions
  - Data flow diagrams
  - Technology choices rationale
- Create `docs/api.md`:
  - API endpoint documentation
  - Request/response examples
  - Error codes and messages
  - Rate limiting and timeouts
- Update `docs/platform.md`:
  - Verify all implementation details match
  - Add actual performance measurements
- Document file structure:
  ```
  stream-view/
  ├── backend/
  │   ├── main.py           # FastAPI application
  │   ├── api/              # API endpoints
  │   ├── services/         # Parsers and analyzers
  │   ├── models/           # Pydantic models
  │   └── tests/            # Test suite
  ├── frontend/
  │   ├── src/
  │   │   ├── components/   # React components
  │   │   ├── services/     # API client
  │   │   └── types/        # TypeScript types
  │   └── tests/            # Playwright tests
  ├── docs/                 # Documentation
  └── docker-compose.yml    # Orchestration
  ```

**Acceptance Criteria:**
- Architecture clearly documented
- API fully documented with examples
- File structure documented
- Code comments explain complex logic
- Developer can onboard with documentation alone

#### 6.3 Development Documentation
**Goal:** Enable contributors to work on the codebase

**Tasks:**
- Create `docs/development.md`:
  - Local development setup
  - Running backend: `uvicorn main:app --reload`
  - Running frontend: `npm run dev`
  - Running tests: `pytest` and `npm test`
  - Code style guidelines (PEP 8, TypeScript)
  - Git workflow
- Create `CONTRIBUTING.md`:
  - How to contribute
  - Code review process
  - Testing requirements
  - Documentation requirements
- Add inline code documentation:
  - Docstrings for all functions/classes
  - Type hints throughout
  - Comments for complex logic

**Acceptance Criteria:**
- Developer can set up local environment using docs
- Contribution process clear
- All code has appropriate documentation
- Guidelines reference `.claude/guidelines.md`

---

### Phase 7: Polish & Security (Day 14)

#### 7.1 Security Hardening
**Goal:** Ensure application meets security best practices

**Tasks:**
- Input validation and sanitization:
  - Validate URL format rigorously
  - Prevent SSRF attacks (block localhost, internal IPs)
  - Sanitize all user inputs before logging
- Implement rate limiting:
  - Use slowapi or similar
  - Limit requests per IP
  - Prevent DoS attacks
- Set manifest size limits:
  - Max 10MB manifest size
  - Reject large files early
- Set request timeouts:
  - 30s default timeout
  - Prevent hanging requests
- Review OWASP Top 10:
  - SQL Injection: N/A (no database)
  - XSS: Sanitize any displayed URLs
  - CSRF: N/A (public API, no sessions)
  - Broken Authentication: N/A (no auth)
  - Security Misconfiguration: Review Docker configs
  - Sensitive Data Exposure: Don't log full URLs (may have tokens)
  - Insufficient Logging: Add structured logging
  - Insecure Deserialization: Validate JSON/XML
  - Using Components with Known Vulnerabilities: Run security audit
  - Insufficient Attack Protection: Add rate limiting
- Add security headers:
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - Content-Security-Policy
- Run security audit:
  ```bash
  # Python
  pip install safety
  safety check

  # Node.js
  npm audit
  ```

**Acceptance Criteria:**
- SSRF attacks blocked (can't access localhost, 127.0.0.1, 169.254.0.0/16, etc.)
- Rate limiting active
- Size limits enforced
- Timeouts prevent hanging
- Security audit passes (no high/critical vulnerabilities)
- Security headers present in responses
- OWASP Top 10 checklist reviewed

#### 7.2 Performance Optimization
**Goal:** Ensure application meets performance targets

**Tasks:**
- Measure baseline performance:
  - Time HLS manifest parsing
  - Time DASH manifest parsing
  - Time SCTE-35 extraction
  - Time FFmpeg analysis
  - Time total API response
- Optimize as needed:
  - Use async/await for all I/O
  - Parallel processing where possible
  - Efficient data structures
  - Avoid unnecessary parsing
- Frontend optimization:
  - Lazy load components
  - Optimize bundle size
  - Enable gzip compression
  - Add loading skeletons
- Add performance monitoring:
  - Log request durations
  - Track slow requests
  - Monitor memory usage

**Acceptance Criteria:**
- HLS parsing < 100ms (measured)
- DASH parsing < 150ms (measured)
- SCTE-35 extraction < 50ms (measured)
- FFmpeg analysis < 500ms (measured)
- Total API response < 1s (measured)
- Frontend bundle size reasonable (< 500KB gzipped)
- No performance regressions

#### 7.3 Final QA
**Goal:** Verify all requirements met with real-world testing

**Tasks:**
- Test with all provided test URLs:
  - [ ] BBC Two (DASH Live, No DRM)
  - [ ] BBC News (DASH Live, No DRM)
  - [ ] ITV1 (DASH Live, DRM)
  - [ ] ITV2 (DASH Live, DRM)
  - [ ] Freevee Blitz (DASH VOD, DRM)
  - [ ] Channel4 Hollyoaks (DASH VOD, DRM)
  - [ ] Freevee Euronews (HLS Live, DRM)
  - [ ] Amazon Prime Playdate (HLS VOD, DRM)
  - [ ] Channel4 4 (HLS Live, DRM)
  - [ ] Channel4 Hollyoaks (HLS VOD, DRM)
- Verify all user stories:
  - [ ] US-001: Web interface loads, logo present, no auth required
  - [ ] US-002: HLS analysis works (bitrates, tracks, DRM)
  - [ ] US-003: DASH analysis works (bitrates, tracks, DRM)
  - [ ] US-004: SCTE-35 markers extracted and displayed
  - [ ] US-005: Video metadata extracted and displayed
  - [ ] US-006: Documentation complete and accurate
- Final UI/UX review:
  - [ ] Modern design
  - [ ] Responsive layout
  - [ ] Clear error messages
  - [ ] Good loading states
  - [ ] Professional appearance
- Cross-browser testing:
  - [ ] Chrome
  - [ ] Firefox
  - [ ] Safari
  - [ ] Edge

**Acceptance Criteria:**
- All test URLs process successfully
- All user stories verified complete
- UI/UX meets standards
- Works in all major browsers
- No critical bugs

---

## Deliverables

✅ **Fully functional web application**
- Single-page web interface
- HLS and DASH support
- SCTE-35 extraction
- FFmpeg video analysis
- Modern, clean UI

✅ **Docker containers with one-command deployment**
- Backend Docker image
- Frontend Docker image
- Docker Compose orchestration
- `docker-compose up` works

✅ **Comprehensive test suite**
- Backend unit tests (pytest)
- Frontend E2E tests (Playwright)
- Test data externalized
- >80% code coverage

✅ **Complete documentation**
- User guide (deployment, usage)
- Technical documentation (architecture, API)
- Development guide (setup, contributing)
- Inline code documentation

✅ **Clean, maintainable code**
- Follows PEP 8 (Python)
- TypeScript strict mode (frontend)
- Clear function/variable names
- Small, focused functions
- Proper error handling

✅ **All user stories satisfied**
- US-001: ✅ Web interface
- US-002: ✅ HLS analysis
- US-003: ✅ DASH analysis
- US-004: ✅ SCTE-35 extraction
- US-005: ✅ Video metadata
- US-006: ✅ Documentation

---

## Success Criteria

The project is complete when:

- ✅ Application runs with `docker-compose up`
- ✅ Supports both HLS (.m3u8) and DASH (.mpd) manifests
- ✅ Extracts SCTE-35 markers from both formats
- ✅ Uses FFmpeg for video fragment analysis
- ✅ Works with DRM-encrypted streams
- ✅ Modern, clean UI with Realitech logo
- ✅ No authentication required
- ✅ Response time < 1 second
- ✅ All tests passing
- ✅ Documentation complete
- ✅ Security review passed
- ✅ All test URLs work

---

## Risk Management

### Potential Risks

1. **DRM-encrypted content analysis limitations**
   - **Risk:** Cannot fully analyze encrypted video fragments
   - **Mitigation:** Extract maximum info from manifest and init segments; document limitations

2. **Live stream availability**
   - **Risk:** Test URLs may become unavailable
   - **Mitigation:** Document URLs with timestamps; use mix of live and VOD; test data externalized

3. **FFmpeg complexity**
   - **Risk:** FFmpeg/PyAV integration may be challenging
   - **Mitigation:** Start with basic probing; incremental enhancement; thorough error handling

4. **Performance with large manifests**
   - **Risk:** Large manifests may exceed 1s response time target
   - **Mitigation:** Size limits; async processing; optimization pass in Phase 7

5. **SCTE-35 format variations**
   - **Risk:** SCTE-35 encoding may vary between providers
   - **Mitigation:** Use robust threefive library; test with multiple sources; graceful error handling

### Mitigation Strategy

- Start with simpler features, add complexity incrementally
- Extensive error handling throughout
- Comprehensive testing with real-world streams
- Performance monitoring from early phases
- Document known limitations clearly

---

## Timeline Summary

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| Phase 1: Foundation | Days 1-2 | Project structure, initialized backend/frontend |
| Phase 2: Backend | Days 3-5 | API, HLS/DASH/SCTE-35 parsers, FFmpeg integration |
| Phase 3: Frontend | Days 6-8 | UI components, results display, error handling |
| Phase 4: Docker | Days 9-10 | Dockerfiles, docker-compose, deployment |
| Phase 5: Testing | Days 11-12 | Backend tests, frontend tests, test data |
| Phase 6: Documentation | Day 13 | User docs, technical docs, dev docs |
| Phase 7: Polish | Day 14 | Security, performance, QA |

**Total: 14 days**

---

## Next Steps

After plan approval:

1. Begin Phase 1: Project Foundation
2. Set up project structure
3. Initialize backend with FastAPI
4. Initialize frontend with React + Vite
5. Create initial Docker configuration
6. Proceed through phases sequentially

## Notes

- This plan follows the architecture defined in `docs/platform.md`
- All requirements from `docs/requirements.md` are addressed
- Development follows guidelines in `.claude/guidelines.md`
- Plan assumes full-time development effort
- Phases can overlap slightly for efficiency
- Regular testing throughout (not just Phase 5)
- Security considerations integrated throughout
