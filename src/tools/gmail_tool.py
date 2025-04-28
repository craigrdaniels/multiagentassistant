from langchain_core.tools import tool


@tool
async def gmail_tool(query: str):
    """
    An agent to perform functions related to Gmail, such as searching for emails or sending messages.
    Args:
        query (str): The search query or command for the agent to perform.
    """
    from src.core.__init__ import core

    tool_results = await core.run_agent("gmail", query)

    return tool_results
