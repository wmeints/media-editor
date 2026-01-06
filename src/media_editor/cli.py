import shutil

import typer

from media_editor.server import mcp

app = typer.Typer()


@app.command("mcp")
def run_mcp() -> None:
    """Run the Media Editor MCP server."""
    mcp.run()


@app.command("doctor")
def doctor() -> None:
    """Check that required dependencies are available."""
    ffmpeg_path = shutil.which("ffmpeg")

    if ffmpeg_path:
        typer.echo(f"ffmpeg: {ffmpeg_path}")
    else:
        typer.echo(
            "ffmpeg: not found. Make sure ffmpeg is installed and available in your PATH.",
            err=True,
        )
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
