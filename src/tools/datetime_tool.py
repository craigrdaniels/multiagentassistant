from langchain_core.tools import tool
import asyncio


@tool
async def get_datetime(timezone: str = None, fmt: str = None):
    """
    Get the current date and time in a human-readable format.
    Args:
      • a dict: {"timezone": "Australia/Brisbane", "fmt": "%I:%M %p"}
      • or omitted entirely
    """

    from src.core.__init__ import core

    time = await core.run_agent("datetime", timezone, fmt)
    # result = asyncio.run(coro)
    return time
