from langchain_core.tools import tool


@tool
async def redditsearch(
    query: str,
    sort: str = "new",
    time_filter: str = "all",
    subreddit: str = "all",
    limit: int = 20,
):
    """
    Search Reddit for a given query.
    Args:
        query (str): The search query.
        sort (str): The sorting method (e.g., "relevance", "new", "hot", "top", "comments").
        time_filter (str): shoudl be time period to filter by (eg. "all", "day", "hour", "month", "week", "year").
        subreddit (str): The subreddit to search in (optional).
        limit (int): The maximum number of results to return (default is 20).
    """

    from src.core.__init__ import core

    search_results = await core.run_agent(
        "redditsearch", query, subreddit, sort, time_filter, limit
    )
    return search_results
