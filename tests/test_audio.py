import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from media_editor.tools.audio import extract_audio

TEST_DATA_DIR = Path(__file__).parent / "data"
TEST_VIDEO = TEST_DATA_DIR / "test-video.mp4"


def test_extract_audio_creates_output_file(tmp_path: Path) -> None:
    """Test that extract_audio creates an audio file from a video."""
    output_path = tmp_path / "output.aac"

    result = extract_audio(str(TEST_VIDEO), str(output_path))

    assert result == str(output_path)
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_extract_audio_raises_file_not_found() -> None:
    """Test that extract_audio raises FileNotFoundError for missing input."""
    with pytest.raises(FileNotFoundError, match="Video file not found"):
        extract_audio("/nonexistent/video.mp4", "/tmp/output.aac")


def test_extract_audio_raises_on_ffmpeg_failure(tmp_path: Path) -> None:
    """Test that extract_audio raises CalledProcessError when FFmpeg fails."""
    output_path = tmp_path / "output.aac"

    with patch("media_editor.tools.audio.subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd=["ffmpeg"], stderr="FFmpeg error"
        )

        with pytest.raises(subprocess.CalledProcessError):
            extract_audio(str(TEST_VIDEO), str(output_path))
