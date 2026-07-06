"""Unit tests for FilesystemMCPClient.

Verifies reading transcripts and saving results using mocked Model Context Protocol (MCP) tool calls.
"""

import sys
import pytest
from unittest.mock import MagicMock, patch

# Remove local 'src/mcp' directory or 'src' from sys.path temporarily to import real mcp
import importlib
try:
    from mcp import ClientSession
except ImportError:
    # Try importing from the filesystem_client module which resolved real_mcp
    from mcp.filesystem_client import ClientSession

# We mock mcp types blocks since they are returned by call_tool
class MockContentBlock:
    """Mock for content block returned by call_tool."""
    def __init__(self, text: str) -> None:
        self.text = text


# To import from src, we import absolute mcp package's filesystem_client
from mcp.filesystem_client import FilesystemMCPClient


def test_read_transcript_success() -> None:
    """Tests reading transcript successfully via MCP read_file tool."""
    mock_session = MagicMock()
    # The call_tool returns a response containing content blocks
    mock_response = MagicMock()
    mock_response.content = [MockContentBlock("This is the transcript content.")]
    mock_session.call_tool.return_value = mock_response

    client = FilesystemMCPClient(mock_session)
    content = client.read_transcript("C:/dummy/transcript.txt")

    assert content == "This is the transcript content."
    mock_session.call_tool.assert_called_once_with(
        "read_file", {"path": "C:/dummy/transcript.txt"}
    )


def test_read_transcript_missing_file() -> None:
    """Tests that read_transcript raises RuntimeError when the file is missing/error occurs."""
    mock_session = MagicMock()
    mock_session.call_tool.side_effect = Exception("File not found")

    client = FilesystemMCPClient(mock_session)

    with pytest.raises(RuntimeError) as exc_info:
        client.read_transcript("C:/dummy/missing.txt")

    assert "Failed to read file via MCP" in str(exc_info.value)
    mock_session.call_tool.assert_called_once_with(
        "read_file", {"path": "C:/dummy/missing.txt"}
    )


def test_save_results_success() -> None:
    """Tests saving results successfully via MCP write_file tool."""
    mock_session = MagicMock()
    mock_session.call_tool.return_value = MagicMock()

    client = FilesystemMCPClient(mock_session)
    results = {"meeting_title": "Test Title", "summary": "Great summary."}
    success = client.save_results(results, "C:/dummy/output.json")

    assert success is True
    # The JSON should be dumped with indent=2
    import json
    expected_content = json.dumps(results, indent=2)
    mock_session.call_tool.assert_called_once_with(
        "write_file", {"path": "C:/dummy/output.json", "content": expected_content}
    )


def test_save_results_invalid_path() -> None:
    """Tests that save_results raises RuntimeError when path is invalid or write fails."""
    mock_session = MagicMock()
    mock_session.call_tool.side_effect = Exception("Permission denied")

    client = FilesystemMCPClient(mock_session)

    with pytest.raises(RuntimeError) as exc_info:
        client.save_results("some data", "invalid_dir/output.txt")

    assert "Failed to write file via MCP" in str(exc_info.value)
    mock_session.call_tool.assert_called_once_with(
        "write_file", {"path": "invalid_dir/output.txt", "content": "some data"}
    )
