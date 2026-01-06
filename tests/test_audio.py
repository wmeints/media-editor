from pathlib import Path

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
