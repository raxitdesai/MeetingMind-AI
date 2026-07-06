"""Agent registry for MeetingMind AI.

This module provides the AgentRegistry class to manage and resolve registered agents.
"""

from typing import Dict, Any

class AgentRegistry:
    """Registry to keep track of and retrieve active agents in the system."""

    def __init__(self) -> None:
        """Initializes the agent registry."""
        self._agents: Dict[str, Any] = {}

    def register(self, name: str, agent: Any) -> None:
        """Registers a new agent under the given name.

        Args:
            name: The unique registration key for the agent.
            agent: The agent instance.
        """
        self._agents[name] = agent

    def get(self, name: str) -> Any:
        """Retrieves a registered agent by name.

        Args:
            name: The unique registration key of the agent.

        Returns:
            The agent instance.

        Raises:
            KeyError: If the agent is not registered.
        """
        if name not in self._agents:
            raise KeyError(f"Agent '{name}' is not registered.")
        return self._agents[name]

    def list_agents(self) -> list[str]:
        """Lists all registered agent names.

        Returns:
            A list of registered agent names.
        """
        return list(self._agents.keys())
