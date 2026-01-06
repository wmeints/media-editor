from pathlib import Path

import pytest

from media_editor.tools.video import get_video_duration, parse_timestamp, trim_video

TEST_DATA_DIR = Path(__file__).parent / "data"
TEST_VIDEO = TEST_DATA_DIR / "test-video.mp4"


class TestParseTimestamp:
    """Tests for parse_timestamp function."""

    def test_parse_int(self) -> None:
        assert parse_timestamp(30) == 30.0

    def test_parse_float(self) -> None:
        assert parse_timestamp(30.5) == 30.5

    def test_parse_timestamp_string(self) -> None:
        assert parse_timestamp("1:30") == 90.0

    def test_parse_timestamp_string_zero_minutes(self) -> None:
        assert parse_timestamp("0:45") == 45.0

    def test_parse_timestamp_string_large_minutes(self) -> None:
        assert parse_timestamp("10:05") == 605.0

    def test_parse_invalid_format_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid timestamp format"):
            parse_timestamp("invalid")

    def test_parse_invalid_seconds_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid seconds value"):
            parse_timestamp("1:60")


class TestGetVideoDuration:
    """Tests for get_video_duration function."""

    def test_returns_duration(self) -> None:
        duration = get_video_duration(TEST_VIDEO)
        assert duration > 0


class TestTrimVideo:
    """Tests for trim_video function."""

    def test_trim_with_start_offset(self, tmp_path: Path) -> None:
        output_path = tmp_path / "output.mp4"

        result = trim_video(str(TEST_VIDEO), str(output_path), start_offset=1)

        assert result == str(output_path)
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_trim_with_end_offset(self, tmp_path: Path) -> None:
        output_path = tmp_path / "output.mp4"

        result = trim_video(str(TEST_VIDEO), str(output_path), end_offset=1)

        assert result == str(output_path)
        assert output_path.exists()

    def test_trim_with_both_offsets(self, tmp_path: Path) -> None:
        output_path = tmp_path / "output.mp4"

        result = trim_video(
            str(TEST_VIDEO), str(output_path), start_offset=1, end_offset=1
        )

        assert result == str(output_path)
        assert output_path.exists()

    def test_trim_with_timestamp_string(self, tmp_path: Path) -> None:
        output_path = tmp_path / "output.mp4"

        result = trim_video(str(TEST_VIDEO), str(output_path), start_offset="0:01")

        assert result == str(output_path)
        assert output_path.exists()

    def test_raises_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError, match="Video file not found"):
            trim_video("/nonexistent/video.mp4", "/tmp/output.mp4", start_offset=1)

    def test_raises_when_no_offset_provided(self, tmp_path: Path) -> None:
        output_path = tmp_path / "output.mp4"

        with pytest.raises(ValueError, match="At least one of"):
            trim_video(str(TEST_VIDEO), str(output_path))
