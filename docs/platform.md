# Platform and Technology Stack

## Executive Summary

The stream-view application will be built using a **Python backend** with **FastAPI** and a **React frontend** with **Vite**, deployed via **Docker** containers. This stack was selected based on the technical requirements for **HLS and MPEG-DASH** manifest parsing, FFmpeg integration, and SCTE-35 marker analysis.

## Technology Stack

### Backend

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Runtime | Python | 3.11+ | Core backend language |
| Web Framework | FastAPI | Latest | Modern async web framework with auto-documentation |
| ASGI Server | Uvicorn | Latest | High-performance async server |
| FFmpeg Bindings | PyAV | Latest | Native FFmpeg library bindings (supports HLS & DASH) |
| SCTE-35 Parsing | threefive | Latest | SCTE-35 marker parsing and analysis |
| HLS Parsing | m3u8 | Latest | HLS manifest (.m3u8) parsing |
| DASH Parsing | mpegdash | Latest | MPEG-DASH manifest (.mpd) parsing |
| HTTP Client | httpx | Latest | Async HTTP client for fetching manifests |

### Frontend

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Framework | React | 18+ | UI component library |
| Build Tool | Vite | Latest | Fast build tooling and dev server |
| Language | TypeScript | 5+ | Type-safe JavaScript |
| Styling | Tailwind CSS | Latest | Modern utility-first CSS framework |
| HTTP Client | Axios | Latest | API communication |

### Infrastructure

| Component | Technology | Purpose |
|-----------|------------|---------|
| Containerization | Docker | Consistent deployment with FFmpeg dependencies |
| Orchestration | Docker Compose | Multi-container application management |
| FFmpeg | FFmpeg 6+ | Media analysis and stream probing |

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────┐
│                   Browser                        │
│  ┌───────────────────────────────────────────┐  │
│  │     React Frontend (TypeScript)           │  │
│  │  - Single Page Application                │  │
│  │  - Modern UI with Tailwind CSS            │  │
│  │  - Stream information display             │  │
│  └───────────────┬───────────────────────────┘  │
└─────────────────┼───────────────────────────────┘
                  │ HTTP/REST API
                  │
┌─────────────────▼───────────────────────────────┐
│            FastAPI Backend (Python)              │
│  ┌───────────────────────────────────────────┐  │
│  │  API Endpoints                            │  │
│  │  - /api/analyze (POST)                    │  │
│  │  - /api/health (GET)                      │  │
│  └───────────────┬───────────────────────────┘  │
│                  │                               │
│  ┌───────────────▼───────────────────────────┐  │
│  │  Stream Analysis Service                  │  │
│  │  - HLS manifest parsing (m3u8)            │  │
│  │  - DASH manifest parsing (mpegdash)       │  │
│  │  - SCTE-35 marker extraction (threefive)  │  │
│  │  - FFmpeg stream probing (PyAV)           │  │
│  │  - Metadata extraction                    │  │
│  └───────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

### Deployment Architecture

```
┌──────────────────────────────────────────────────┐
│              Docker Compose                       │
│                                                   │
│  ┌────────────────────┐  ┌───────────────────┐  │
│  │  Frontend Container │  │ Backend Container │  │
│  │  - Nginx           │  │ - Python 3.11     │  │
│  │  - React build     │  │ - FastAPI         │  │
│  │  - Port: 80        │  │ - PyAV            │  │
│  │                    │  │ - FFmpeg          │  │
│  │                    │  │ - Port: 8000      │  │
│  └────────────────────┘  └───────────────────┘  │
│                                                   │
└──────────────────────────────────────────────────┘
```

## Rationale

### Why Python for Backend?

1. **FFmpeg Integration**
   - PyAV provides native FFmpeg bindings (not just CLI wrappers)
   - Direct access to FFmpeg's powerful media analysis capabilities
   - Can probe streams, extract metadata, analyze codecs programmatically

2. **Dual Format Support (HLS & MPEG-DASH)**
   - `m3u8` library for HLS manifest (.m3u8) parsing
   - `mpegdash` library for MPEG-DASH manifest (.mpd) parsing
   - FFmpeg natively supports both streaming protocols
   - Unified analysis workflow for both formats

3. **SCTE-35 Parsing**
   - `threefive` library offers comprehensive SCTE-35 parsing
   - Works with both HLS and DASH streams
   - Supports extraction of ad markers, program boundaries, and splice points
   - Essential for professional streaming analysis

4. **Media Processing Ecosystem**
   - Python is the de facto standard for media processing and analysis
   - Rich ecosystem of video/streaming tools and libraries
   - Extensive documentation and community support

5. **Modern Web Framework**
   - FastAPI provides async/await support for high performance
   - Automatic OpenAPI documentation generation
   - Built-in data validation with Pydantic
   - Excellent developer experience

6. **Easy Deployment**
   - Simple to containerize with all dependencies
   - FFmpeg installation in Docker is straightforward
   - Reproducible builds across environments

### Why React for Frontend?

1. **Modern UI Development**
   - Component-based architecture for maintainable code
   - Large ecosystem of UI libraries and components
   - Excellent developer tools and debugging

2. **Single Page Application**
   - Natural fit for the single-page requirement
   - Fast, responsive user experience
   - Client-side routing if needed later

3. **Build Tooling**
   - Vite provides extremely fast development server
   - Hot module replacement for instant feedback
   - Optimized production builds

4. **TypeScript Support**
   - Type safety for complex stream data structures
   - Better IDE support and autocomplete
   - Catch errors at compile time

### Why Docker?

1. **Zero-Knowledge Builds**
   - `docker-compose up` is all users need to know
   - All dependencies bundled in container
   - No need to install Python, FFmpeg, Node.js manually

2. **Consistent Environments**
   - Same environment on developer machine and cloud server
   - Eliminates "works on my machine" problems
   - Reproducible builds

3. **Easy FFmpeg Distribution**
   - FFmpeg compiled and ready in container
   - No manual installation or compilation needed
   - Same FFmpeg version everywhere

## Alternative Options Considered

### Node.js (Rejected)

**Pros:**
- Single language for frontend and backend
- Good HLS parsing libraries
- Some DASH parsing libraries available

**Cons:**
- ❌ `fluent-ffmpeg` is just a CLI wrapper, not true bindings
- ❌ Limited SCTE-35 parsing libraries
- ❌ Not ideal for deep media analysis
- ❌ Would spawn FFmpeg processes instead of using library directly
- ❌ Weaker DASH parsing ecosystem compared to Python

### Go (Strong Alternative)

**Pros:**
- Good FFmpeg bindings (gmf)
- Single binary deployment
- Fast performance
- SCTE-35 parsing available
- Has DASH libraries (go-mpd)

**Cons:**
- Smaller ecosystem for media tools compared to Python
- Less mature streaming analysis libraries for both HLS and DASH

**Verdict:** Solid choice, but Python's ecosystem is stronger for dual HLS/DASH support

### Static Frontend Only (Rejected)

**Pros:**
- Simplest deployment
- No backend needed

**Cons:**
- ❌ Cannot use FFmpeg (browser-only)
- ❌ Limited SCTE-35 parsing capability
- ❌ CORS issues with manifest fetching
- ❌ Cannot handle complex stream analysis

## Development Workflow

### Local Development

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Production Build

```bash
docker-compose up --build
```

Access application at `http://localhost`

## Performance Characteristics

| Metric | Expected Performance |
|--------|---------------------|
| HLS Manifest Parsing | < 100ms for typical .m3u8 manifest |
| DASH Manifest Parsing | < 150ms for typical .mpd manifest (XML parsing) |
| SCTE-35 Extraction | < 50ms per manifest (both HLS and DASH) |
| FFmpeg Probe | < 500ms for remote stream |
| API Response Time | < 1s for complete analysis |
| Concurrent Requests | 100+ (with async FastAPI) |

## Security Considerations

1. **Input Validation**
   - Validate URL format before fetching
   - Timeout protection for manifest fetching
   - Size limits on downloaded manifests

2. **Dependencies**
   - Regular updates via Dependabot
   - Security scanning in CI/CD pipeline
   - Minimal dependency footprint

3. **CORS Configuration**
   - Configured for frontend-backend communication
   - Restricted to necessary origins in production

## Scalability

The architecture supports horizontal scaling:

- **Stateless backend** - Multiple FastAPI instances behind load balancer
- **Containerized** - Easy to deploy multiple replicas
- **Async processing** - Handle many concurrent requests per instance
- **CDN-ready frontend** - Static assets can be CDN-distributed

## Future Considerations

1. **Caching Layer**
   - Redis for manifest caching
   - Reduce repeated analysis of same streams

2. **Database**
   - PostgreSQL for storing analysis history
   - User preferences and favorites

3. **Authentication**
   - OAuth2 integration if needed later
   - API key management for programmatic access

4. **Advanced Features**
   - WebSocket support for live stream monitoring
   - Scheduled analysis jobs
   - Alert notifications for stream issues

## Conclusion

The **Python + FastAPI + React** stack provides the optimal balance of:
- **Functionality** - Full support for both HLS and MPEG-DASH formats, FFmpeg integration, and SCTE-35 parsing
- **Developer Experience** - Modern frameworks with excellent tooling
- **Deployment** - Simple Docker-based distribution
- **Performance** - Async architecture for high throughput
- **Maintainability** - Strong typing and comprehensive ecosystems

This platform will enable rapid development while meeting all technical requirements for professional **HLS and MPEG-DASH** stream analysis.
