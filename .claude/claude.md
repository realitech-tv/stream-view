# Stream-View Project Context

## Project Overview

Stream-view is a web-based application for analyzing video streaming manifests. It provides streaming engineers with detailed information about HLS and MPEG-DASH streams, including metadata extraction, SCTE-35 marker analysis, and FFmpeg-based stream probing.

## Project Goals

- Create a single-page web application accessible via browser
- Support analysis of both HLS (.m3u8) and MPEG-DASH (.mpd) manifests
- Extract and display SCTE-35 markers for ad insertion and program boundaries
- Utilize FFmpeg for deep stream analysis and metadata extraction
- Provide a clean, modern UI without authentication requirements
- Enable easy deployment on local machines or cloud servers
- Build with zero-knowledge required (simple `docker-compose up`)

## Current Status

**Phase:** Initial Planning & Architecture Definition

**Completed:**
- Repository created in realitech-tv organization
- Project documentation structure established
- Platform architecture defined (Python + FastAPI + React)
- Technology stack decisions documented
- Requirements and user stories defined

**Next Steps:**
- Set up project structure (frontend/backend directories)
- Initialize Python backend with FastAPI
- Initialize React frontend with Vite
- Create Docker configuration
- Implement HLS manifest parsing
- Implement DASH manifest parsing
- Add SCTE-35 marker extraction
- Integrate FFmpeg probing capabilities

## Technology Stack

### Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI (async web framework)
- **Server:** Uvicorn (ASGI server)
- **HLS Parsing:** m3u8 library
- **DASH Parsing:** mpegdash library
- **FFmpeg:** PyAV (native bindings)
- **SCTE-35:** threefive library
- **HTTP Client:** httpx (async)

### Frontend
- **Framework:** React 18+
- **Build Tool:** Vite
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios

### Infrastructure
- **Containerization:** Docker
- **Orchestration:** Docker Compose
- **Dependencies:** FFmpeg 6+

## Architecture Decisions

### Why Python for Backend?
1. Native FFmpeg bindings via PyAV (not just CLI wrappers)
2. Excellent libraries for both HLS (m3u8) and DASH (mpegdash) parsing
3. Comprehensive SCTE-35 support with threefive library
4. Rich media processing ecosystem
5. FastAPI provides modern async/await patterns
6. Easy containerization with all dependencies

### Why React for Frontend?
1. Component-based architecture for maintainable code
2. Natural fit for single-page application requirement
3. Vite provides fast development experience
4. TypeScript ensures type safety for complex stream data
5. Large ecosystem of UI components

### Why Docker?
1. Zero-knowledge builds (`docker-compose up`)
2. Bundles FFmpeg and all dependencies
3. Consistent environment across development and production
4. Easy deployment to any server (local or cloud)

## Key Constraints & Requirements

### Functional Requirements
- Single-page web application
- Support HLS (.m3u8) manifest analysis
- Support MPEG-DASH (.mpd) manifest analysis
- Parse and display SCTE-35 markers
- Use FFmpeg for stream probing
- Display stream metadata (codecs, bitrates, variants, etc.)
- Validate manifest format before processing

### Non-Functional Requirements
- Clean, modern UI design
- No authentication required
- Realitech logotype in top left corner
- Easy to build without code knowledge
- Can run on local machine or cloud server
- Fast response times (< 1s for complete analysis)
- Support 100+ concurrent requests

### Security Considerations
- Validate URL format before fetching
- Implement timeout protection for manifest fetching
- Enforce size limits on downloaded manifests
- Follow OWASP guidelines (prevent XSS, injection attacks)

## Project Structure

```
stream-view/
├── .claude/                 # Claude Code configuration
│   ├── guidelines.md       # Development standards
│   ├── prompts.md          # Development prompt log
│   └── claude.md           # This context file
├── docs/                    # Project documentation
│   ├── overview.md         # Project overview
│   ├── requirements.md     # User stories and requirements
│   └── platform.md         # Platform architecture
├── backend/                 # Python FastAPI backend (TBD)
│   ├── main.py
│   ├── requirements.txt
│   └── ...
├── frontend/                # React frontend (TBD)
│   ├── src/
│   ├── package.json
│   └── ...
├── docker-compose.yml       # Multi-container orchestration (TBD)
└── README.md               # Main project README (TBD)
```

## Important Files & Documentation

- `docs/platform.md` - Comprehensive platform architecture and technology decisions
- `docs/requirements.md` - User stories and acceptance criteria
- `docs/overview.md` - High-level project overview
- `.claude/guidelines.md` - Development standards and best practices
- `.claude/prompts.md` - Log of development prompts

## Domain Knowledge

### HLS (HTTP Live Streaming)
- Manifest format: .m3u8 (text-based, M3U playlist format)
- Adaptive bitrate streaming protocol developed by Apple
- Variants contain different quality levels
- Can include SCTE-35 markers in EXT-X-DATERANGE tags

### MPEG-DASH (Dynamic Adaptive Streaming over HTTP)
- Manifest format: .mpd (XML-based Media Presentation Description)
- Industry standard adaptive streaming protocol
- Similar concept to HLS but different manifest format
- Can include SCTE-35 markers in EventStream elements

### SCTE-35
- Standard for insertion of alternate content (typically ads)
- Defines splice points and program boundaries
- Embedded in both HLS and DASH streams
- Critical for professional broadcast workflows

### FFmpeg
- Comprehensive multimedia framework
- Can probe streams to extract detailed metadata
- Supports both HLS and DASH protocols natively
- Provides codec information, bitrates, resolution, etc.

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use TypeScript strict mode for frontend
- Write self-documenting code with clear names
- Keep functions small and focused
- Add comments for complex logic

### Testing
- Write tests for all stream parsing logic
- Mock external stream fetches in unit tests
- Test both valid and invalid manifests
- Ensure SCTE-35 parsing edge cases are covered

### Git Workflow
- Write clear, descriptive commit messages
- Use conventional commit format
- Never commit secrets or credentials
- Keep commits atomic and focused

### Security
- Never commit API keys or secrets
- Validate all user inputs (URLs)
- Implement timeout protection
- Follow OWASP guidelines for web security

## Performance Expectations

- HLS Manifest Parsing: < 100ms
- DASH Manifest Parsing: < 150ms (XML parsing overhead)
- SCTE-35 Extraction: < 50ms
- FFmpeg Probe: < 500ms
- Total API Response: < 1s

## Future Considerations

- Redis caching for manifest analysis results
- PostgreSQL for storing analysis history
- WebSocket support for live stream monitoring
- Scheduled analysis jobs
- Alert notifications for stream issues
- OAuth2 authentication (if needed)
- API key management for programmatic access

## Helpful Commands

### Development
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

### Production
```bash
docker-compose up --build
```

### Testing
```bash
# Backend
pytest

# Frontend
npm test
```

## Contact & Resources

- **Organization:** realitech-tv
- **Repository:** https://github.com/realitech-tv/stream-view
- **Visibility:** Public (read-only for public, write access restricted)

## Notes for Claude

- This is a greenfield project - no existing codebase yet
- Focus on clean, maintainable code with good documentation
- Prioritize security (input validation, timeout protection)
- Follow the architecture decisions in `docs/platform.md`
- Refer to `docs/requirements.md` for user stories and acceptance criteria
- Follow development standards in `.claude/guidelines.md`
- The application must be easy to build and deploy (Docker is key)
- Performance is important but not at the cost of code clarity
- This is a professional tool for streaming engineers - accuracy is critical
