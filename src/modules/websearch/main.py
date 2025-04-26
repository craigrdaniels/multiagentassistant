from langchain_community.tools import DuckDuckGoSearchResults

search = DuckDuckGoSearchResults()


class Agent:
    """
    Agent to provide web search functionality.
    """

    async def run(self, query: str):
        try:
            return search.invoke(query)
        except Exception as e:
            return f"Error: {str(e)}"
