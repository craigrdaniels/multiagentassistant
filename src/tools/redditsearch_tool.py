from langchain_core.tools import tool


@tool
async def redditsearch(query: str, subreddit: str = "all"):
    """
    Search Reddit for a given query.
    Args:
        query (str): The search query.
        subreddit (str): The subreddit to search in (optional).
    """

    from src.core.__init__ import core

    search_results = await core.run_agent("redditsearch", query, subreddit)
    return search_results
