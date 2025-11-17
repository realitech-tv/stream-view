# Stream-View

A web-based application for analyzing video streaming manifests. Stream-View provides streaming engineers with detailed information about HLS and MPEG-DASH streams, including metadata extraction, SCTE-35 marker analysis, and FFmpeg-based stream probing.

## Features

- **HLS Manifest Analysis** - Parse and analyze HTTP Live Streaming (.m3u8) manifests
- **DASH Manifest Analysis** - Parse and analyze MPEG-DASH (.mpd) manifests
- **SCTE-35 Extraction** - Extract and display ad insertion markers and program boundaries
- **Video Metadata** - Deep stream analysis using FFmpeg for codec, bitrate, and quality information
- **DRM Detection** - Identify encryption schemes (Widevine, PlayReady, FairPlay)
- **Modern UI** - Clean, responsive web interface with no authentication required

## Quick Start

### Prerequisites

- **Docker** and **Docker Compose** installed on your system
- No other dependencies required!

### Run the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/realitech-tv/stream-view.git
   cd stream-view
   ```

2. Start the application:
   ```bash
   docker-compose up
   ```

3. Open your browser and navigate to:
   ```
   http://localhost
   ```

4. Enter a manifest URL (.m3u8 or .mpd) and click "View" to analyze the stream.

### Stop the Application

```bash
docker-compose down
```

## Development Setup

### Backend (Python)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Technology Stack

**Backend:**
- Python 3.11+ with FastAPI
- FFmpeg (via PyAV) for stream analysis
- Libraries: m3u8, mpegdash, threefive, httpx

**Frontend:**
- React 18+ with TypeScript
- Vite for fast development and optimized builds
- Tailwind CSS for modern styling

**Infrastructure:**
- Docker & Docker Compose for containerized deployment

## Project Structure

```
stream-view/
├── backend/              # Python FastAPI backend
│   ├── main.py          # Application entry point
│   ├── api/             # API endpoints
│   ├── services/        # Business logic (parsers, analyzers)
│   ├── models/          # Pydantic data models
│   └── tests/           # Test suite
├── frontend/            # React TypeScript frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API client
│   │   ├── types/       # TypeScript definitions
│   │   └── styles/      # CSS and Tailwind config
│   └── public/          # Static assets
├── docs/                # Documentation
├── assets/              # Design assets (logos, etc.)
└── docker-compose.yml   # Multi-container orchestration
```

## Usage

1. **Enter Stream URL** - Paste a HLS (.m3u8) or DASH (.mpd) manifest URL
2. **Click View** - The application will analyze the stream
3. **Review Results** - See detailed information about:
   - Video bitrate levels and variants
   - Audio tracks and languages
   - Subtitle tracks
   - DRM encryption details
   - SCTE-35 ad markers
   - Video codec and metadata

## Supported Stream Formats

- **HLS** (HTTP Live Streaming) - `.m3u8` manifests
- **DASH** (Dynamic Adaptive Streaming over HTTP) - `.mpd` manifests

Both live streams and video-on-demand (VOD) are supported.

## Documentation

- [Platform Architecture](docs/platform.md) - Technology decisions and system design
- [Requirements](docs/requirements.md) - User stories and acceptance criteria
- [Implementation Plan](docs/plan.md) - Detailed development roadmap
- [Project Overview](docs/overview.md) - High-level project description

## Contributing

See [Development Guidelines](.claude/guidelines.md) for code style and contribution standards.

## License

Copyright © Realitech. All rights reserved.

## Support

For issues or questions, please open an issue on GitHub:
https://github.com/realitech-tv/stream-view/issues
