# Media Editor

An MCP (Model Context Protocol) server that provides tools for editing media files. Use it with Claude or other MCP-compatible AI assistants to automate video and audio processing tasks.

## Features

- **Video Trimming** - Cut video files to specific time ranges
- **Audio Transcription** - Convert speech to text using NVIDIA NeMo
- **Themed Thumbnails** - Generate and prepend title cards to videos with customizable themes

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- FFmpeg (must be installed and available in PATH)
- NVIDIA GPU with CUDA support (for transcription)

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/wmeints/media-editor.git
cd media-editor

# Install dependencies
uv sync
```

### Running the MCP Server

```bash
uv run media-editor
```

### Connecting to Claude Desktop

Add the following to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "media-editor": {
      "command": "uv",
      "args": ["run", "media-editor"],
      "cwd": "/path/to/media-editor"
    }
  }
}
```

## Development

```bash
# Run tests
uv run pytest

# Type checking
uv run mypy src/

# Linting
uv run ruff check src/
uv run ruff format src/
```

## License

MIT
