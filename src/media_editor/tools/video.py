import re
import subprocess
from pathlib import Path


def parse_timestamp(value: float | str) -> float:
    """
    Parse a timestamp value to seconds.

    Parameters
    ----------
    value : float or str
        Either a number of seconds (float/int) or a timestamp string in 'mm:ss' format.

    Returns
    -------
    float
        The timestamp in seconds.

    Raises
    ------
    ValueError
        If the string format is invalid.
    """
    if isinstance(value, (int, float)):
        return float(value)

    match = re.match(r"^(\d+):(\d{2})$", value)
    if not match:
        raise ValueError(
            f"Invalid timestamp format: '{value}'. Expected 'mm:ss' (e.g., '1:30' or '10:05')"
        )

    minutes, seconds = int(match.group(1)), int(match.group(2))
    if seconds >= 60:
        raise ValueError(f"Invalid seconds value: {seconds}. Must be less than 60.")

    return minutes * 60 + seconds


def get_video_duration(video_path: Path) -> float:
    """
    Get the duration of a video file in seconds using ffprobe.

    Parameters
    ----------
    video_path : Path
        Path to the video file.

    Returns
    -------
    float
        Duration of the video in seconds.
    """
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def trim_video(
    video_path: str,
    output_path: str,
    start_offset: float | str | None = None,
    end_offset: float | str | None = None,
) -> str:
    """
    Trim a video file by removing content from the start and/or end.

    This tool uses FFmpeg to trim video files. You can remove a portion from
    the beginning of the video, from the end, or from both sides.

    Parameters
    ----------
    video_path : str
        Absolute path to the input video file to trim.
    output_path : str
        Absolute path where the trimmed video will be saved.
        The output format is determined by the file extension.
    start_offset : float or str, optional
        Amount to remove from the beginning of the video.
        Can be specified as seconds (e.g., 30 or 30.5) or as a timestamp
        string in 'mm:ss' format (e.g., '1:30' for 1 minute 30 seconds).
        If provided, the video will start at this offset.
    end_offset : float or str, optional
        Amount to remove from the end of the video.
        Can be specified as seconds (e.g., 10) or as a timestamp string
        in 'mm:ss' format (e.g., '0:10' for 10 seconds).
        If provided, the video will end this amount before its original end.

    Returns
    -------
    str
        The absolute path to the trimmed output video file.

    Raises
    ------
    ValueError
        If neither start_offset nor end_offset is provided,
        or if timestamp format is invalid.
    subprocess.CalledProcessError
        If FFmpeg fails to process the video.
    FileNotFoundError
        If the input video file does not exist.

    Examples
    --------
    Remove the first 30 seconds from a video:

    >>> trim_video("/path/to/video.mp4", "/path/to/output.mp4", start_offset=30)

    Remove the first 1 minute 30 seconds using timestamp format:

    >>> trim_video("/path/to/video.mp4", "/path/to/output.mp4", start_offset="1:30")

    Remove the last 10 seconds from a video:

    >>> trim_video("/path/to/video.mp4", "/path/to/output.mp4", end_offset=10)

    Keep only the middle portion (remove 1:30 from start, 0:45 from end):

    >>> trim_video("/path/to/video.mp4", "/path/to/output.mp4", start_offset="1:30", end_offset="0:45")
    """
    input_path = Path(video_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if start_offset is None and end_offset is None:
        raise ValueError("At least one of start_offset or end_offset must be provided")

    start_seconds = parse_timestamp(start_offset) if start_offset is not None else None
    end_seconds = parse_timestamp(end_offset) if end_offset is not None else None

    ffmpeg_args = ["ffmpeg", "-y", "-i", str(input_path)]

    if start_seconds is not None:
        ffmpeg_args.extend(["-ss", str(start_seconds)])

    if end_seconds is not None:
        duration = get_video_duration(input_path)
        end_time = duration - end_seconds
        if start_seconds is not None:
            end_time -= start_seconds
        ffmpeg_args.extend(["-t", str(end_time)])

    ffmpeg_args.extend(["-c", "copy", output_path])

    subprocess.run(ffmpeg_args, check=True, capture_output=True, text=True)

    return output_path
