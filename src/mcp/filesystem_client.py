"""Filesystem MCP Client implementation for MeetingMind AI.

This module provides the FilesystemMCPClient class, which connects to a
Model Context Protocol (MCP) server to read transcripts and save results,
avoiding direct filesystem access from the application layer.
"""

import json
import logging
from typing import Any, Dict, Optional, Union

# Bypassing pythonpath shadowing to import third-party `mcp` package
import sys
import importlib.util
import os

def _import_real_mcp():
    # Find all path entries and find the one that points to the third-party package
    # We want to exclude paths inside the current workspace/src
    for path in sys.path:
        if not path:
            continue
        try:
            # check if there is an mcp package in this path that is NOT our src folder
            if "MeetingMind-AI" in path and ("src" in path or "tests" in path):
                continue
            # Look for a directory named mcp or mcp.py in the path
            potential_dir = os.path.join(path, "mcp")
            if os.path.isdir(potential_dir) and os.path.exists(os.path.join(potential_dir, "__init__.py")):
                spec = importlib.util.spec_from_file_location("real_mcp", os.path.join(potential_dir, "__init__.py"))
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules["real_mcp"] = module
                    spec.loader.exec_module(module)
                    return module
        except Exception:
            pass
    # Fallback to standard import if not shadowed
    import mcp
    return mcp

real_mcp = _import_real_mcp()
ClientSession = getattr(real_mcp, "ClientSession", None)
if ClientSession is None:
    # If not at top-level, try client.session
    try:
        import real_mcp.client.session as client_session
        ClientSession = client_session.ClientSession
    except ImportError:
        try:
            import mcp.client.session as client_session
            ClientSession = client_session.ClientSession
        except ImportError:
            ClientSession = Any

logger = logging.getLogger("meetingmind.mcp_client")


class FilesystemMCPClient:
    """A client for interacting with the Filesystem MCP Server.

    This client encapsulates MCP tool calls (e.g., 'read_file', 'write_file')
    to prevent the application layer from performing direct filesystem operations.
    """

    def __init__(self, session: ClientSession) -> None:
        """Initializes the FilesystemMCPClient with an active MCP ClientSession.

        Args:
            session: An active mcp.ClientSession instance connected to the MCP server.
        """
        self.session = session
        logger.info("FilesystemMCPClient initialized with session.")

    def read_transcript(self, file_path: str) -> str:
        """Reads a meeting transcript file using the MCP server's read_file tool.

        Args:
            file_path: The absolute or relative path to the transcript file.

        Returns:
            str: The text content of the transcript file.

        Raises:
            RuntimeError: If the tool call fails or returns an unexpected result.
        """
        logger.info("Calling read_file tool via MCP for path: %s", file_path)
        try:
            # Google MCP Python SDK: session.call_tool(name, arguments)
            response = self.session.call_tool("read_file", {"path": file_path})
            if not response or not response.content:
                raise RuntimeError(f"MCP read_file returned an empty or invalid response for: {file_path}")

            # Usually the response.content is a list of content blocks.
            # We assume text content block.
            content_text = ""
            for block in response.content:
                if hasattr(block, "text") and block.text:
                    content_text += block.text
                elif isinstance(block, dict) and block.get("text"):
                    content_text += block["text"]

            if not content_text:
                raise RuntimeError(f"No text content found in MCP read_file response for: {file_path}")

            return content_text
        except Exception as e:
            logger.error("Failed to read transcript via MCP from %s: %s", file_path, e)
            raise RuntimeError(f"Failed to read file via MCP: {e}") from e

    def save_results(self, results: Union[str, Dict[str, Any]], output_path: str) -> bool:
        """Saves meeting processing results using the MCP server's write_file tool.

        Args:
            results: The results to save. Can be a string or a JSON-serializable dictionary.
            output_path: The destination file path.

        Returns:
            bool: True if the save operation was successful.

        Raises:
            RuntimeError: If the tool call fails.
        """
        logger.info("Calling write_file tool via MCP for path: %s", output_path)
        try:
            if isinstance(results, dict):
                content = json.dumps(results, indent=2)
            else:
                content = str(results)

            # Call the write_file tool exposed by the filesystem MCP server.
            # The arguments for write_file typically accept path and content.
            response = self.session.call_tool("write_file", {"path": output_path, "content": content})
            logger.info("Results successfully saved via MCP to %s", output_path)
            return True
        except Exception as e:
            logger.error("Failed to save results via MCP to %s: %s", output_path, e)
            raise RuntimeError(f"Failed to write file via MCP: {e}") from e
