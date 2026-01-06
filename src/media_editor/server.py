from fastmcp import FastMCP

from media_editor.tools.audio import extract_audio
from media_editor.tools.video import trim_video

mcp = FastMCP("media-editor")

mcp.tool("trim_video")(trim_video)
mcp.tool("extract_audio")(extract_audio)
