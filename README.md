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

This repository uses Git LFS to store test video files. Install Git LFS before cloning:

```bash
# Install Git LFS (macOS)
brew install git-lfs

# Initialize Git LFS
git lfs install
```

Then clone and install:

```bash
# Clone the repository (LFS files are fetched automatically)
git clone https://github.com/wmeints/media-editor.git
cd media-editor

# Install dependencies
uv sync
```

### Verifying Your Setup

Run the `doctor` command to check that all required dependencies are installed and available:

```bash
uv run media-editor doctor
```

If successful, you'll see the path to FFmpeg. If FFmpeg is missing, install it and ensure it's in your PATH.

### Running the MCP Server

```bash
uv run media-editor mcp
```

### Connecting to Claude Desktop

Add the following to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "media-editor": {
      "command": "uv",
      "args": ["run", "media-editor", "mcp"],
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
uv run pyright

# Linting
uv run ruff check src/
uv run ruff format src/
```

## License

MIT
