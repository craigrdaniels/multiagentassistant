import os
from langchain_community.tools.reddit_search.tool import RedditSearchSchema
from langchain_community.tools.reddit_search.tool import RedditSearchRun
from langchain_community.utilities.reddit_search import RedditSearchAPIWrapper


class Agent:
    """
    Agent to provide reddit search functionality.
    """

    async def run(
        self,
        query: str,
        subreddit: str,
        sort: str = "new",
        time_filter: str = "all",
        limit: int = 20,
    ):
        try:
            search_params = RedditSearchSchema(
                query=query,
                subreddit=subreddit,
                sort=sort,
                time_filter=time_filter,
                limit=str(limit),
            )

            search = RedditSearchRun(
                api_wrapper=RedditSearchAPIWrapper(
                    reddit_client="Agents",
                    reddit_client_id=os.getenv("REDDIT_APP_ID"),
                    reddit_client_secret=os.getenv("REDDIT_APP_SECRET"),
                    reddit_user_agent="MyUserAgent-v1.0",
                )
            )

            result = search.run(tool_input=search_params.dict())
            return result

        except Exception as e:
            return f"Error: {str(e)}"
