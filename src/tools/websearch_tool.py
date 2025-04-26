from langchain_core.tools import tool


@tool
async def websearch(query: str):
    """
    Search the web for a given query.
    Args:
        query (str): The search query.
    """

    from src.core.__init__ import core

    search_results = await core.run_agent("websearch", query)
    return search_results
