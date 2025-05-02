from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_async_playwright_browser

from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import RunnableConfig
from langgraph.graph.message import MessagesState
from langgraph.graph import StateGraph, START

import nest_asyncio

nest_asyncio.apply()


class Agent:
    """
    Agent to provide web search functionality.
    """

    def __init__(self):

        async_browser = create_async_playwright_browser()
        toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
        tools = toolkit.get_tools()

        # Create the agent
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

        self.agent = create_react_agent(
            model=self.model,
            name="PlaywrightAgent",
            prompt="""You are a helpful assistant that can help with web automation tasks using Playwright. You can navigate to web pages, click buttons, fill forms, and extract information from web pages. You can also take screenshots and perform other browser actions.""",
            tools=tools,
        )

    async def call_model(self, state: MessagesState):
        config = RunnableConfig(configurable={"thread_id": "1"})
        response = await self.agent.ainvoke(state, config=config)
        return response

    async def run(self, *args, **kwargs):
        """
        Run the agent with the given arguments and keyword arguments.
        """
        graph = (
            StateGraph(MessagesState)
            .add_node(self.call_model)
            .add_edge(START, "call_model")
            .compile()
        )

        print("Run Playwright")

        if args:
            user_text = args[0]
        else:
            user_text = kwargs.get("input", "")

        result = await graph.ainvoke(
            {"messages": [("user", user_text)]},
        )

        messages = result.get("messages", [])
        if not messages:
            return "No response from the agent."

        last = messages[-1]
        if isinstance(last, tuple) and len(last) == 2:
            return last[1]

        return getattr(last, "content", str(last))
