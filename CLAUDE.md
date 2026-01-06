# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Media Editor is an MCP (Model Context Protocol) server that provides tools for editing media files. It exposes tools for:

- Trimming video files
- Transcribing audio from audio or video files
- Adding themed thumbnails to the start of videos with title and subtitle text

## Tech Stack

- **MCP Interface**: FastMCP
- **CLI Framework**: Typer
- **Video/Audio Processing**: FFmpeg (external dependency)
- **Speech-to-Text**: NVIDIA NeMo
- **Package Manager**: uv

## Development Commands

```bash
# Install dependencies
uv sync

# Run the MCP server
uv run media-editor

# Run tests
uv run pytest

# Run a single test
uv run pytest tests/test_file.py::test_function -v

# Type checking
uv run mypy src/

# Linting
uv run ruff check src/
uv run ruff format src/
```

## Architecture

```
src/media_editor/
├── __init__.py       # Entry point with main() function
├── server.py         # FastMCP server setup and tool registration
├── tools/
│   ├── trim.py       # Video trimming using FFmpeg
│   ├── transcribe.py # Audio transcription using NeMo
│   └── thumbnail.py  # Themed thumbnail generation and video prepending
├── themes/           # Thumbnail theme definitions (colors, fonts, layouts)
└── cli.py            # Typer CLI application
```

The MCP server runs as a command-line application via Typer. FastMCP handles the MCP protocol communication while tools delegate to FFmpeg and NeMo for actual media processing.

## Thumbnail Theming

Thumbnails support selectable themes that define visual styling (colors, fonts, layouts). Themes are reusable across different video types. The thumbnail tool accepts a title, subtitle, and theme name, generates the thumbnail image, and prepends it as a video segment.

## Code Style

- **Docstrings**: Use NumPy style docstrings for all functions and classes
- **Type hints**: Use Python 3.12+ type hints (e.g., `float | str` instead of `Union[float, str]`)
- **Linting/Formatting**: Use ruff for linting (`uv run ruff check src/`) and formatting (`uv run ruff format src/`)

## External Dependencies

- **FFmpeg**: Must be installed on the system and available in PATH
- **NVIDIA NeMo**: Requires appropriate NVIDIA drivers and CUDA for GPU acceleration
