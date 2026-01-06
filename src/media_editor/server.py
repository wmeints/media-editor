from fastmcp import FastMCP

from media_editor.tools.trim import trim_video

mcp = FastMCP("media-editor")

mcp.tool("trim_video")(trim_video)
