import subprocess
from pathlib import Path


def extract_audio(video_path: str, output_path: str) -> str:
    """
    Extract audio from a video file.

    This tool uses FFmpeg to extract the audio stream from a video file
    and save it to a separate audio file. The audio is copied without
    re-encoding for fast, lossless extraction.

    Parameters
    ----------
    video_path : str
        Absolute path to the input video file.
    output_path : str
        Absolute path where the extracted audio will be saved.
        The output format is determined by the file extension
        (e.g., .mp3, .aac, .wav, .flac).

    Returns
    -------
    str
        The absolute path to the extracted audio file.

    Raises
    ------
    FileNotFoundError
        If the input video file does not exist.
    subprocess.CalledProcessError
        If FFmpeg fails to extract the audio.

    Examples
    --------
    Extract audio from a video to an AAC file:

    >>> extract_audio("/path/to/video.mp4", "/path/to/audio.aac")

    Extract audio to MP3 format:

    >>> extract_audio("/path/to/video.mp4", "/path/to/audio.mp3")
    """
    input_path = Path(video_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    ffmpeg_args = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vn",
        "-acodec",
        "copy",
        output_path,
    ]

    subprocess.run(ffmpeg_args, check=True, capture_output=True, text=True)

    return output_path
