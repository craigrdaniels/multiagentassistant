from langchain_openai import ChatOpenAI
from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import RunnableConfig
from langgraph.graph.message import MessagesState
from langgraph.graph import StateGraph, START

# TODO: Stop the agent from streaming - just return the final result


class Agent:
    """
    Agent to provide Gmail functionality.
    """

    def __init__(self):
        self.credentials = get_gmail_credentials(
            token_file="token.json",
            scopes=["https://mail.google.com/"],
            client_secrets_file="src/modules/gmail/credentials.json",
        )

        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

        toolkit = GmailToolkit()
        self.tools = toolkit.get_tools()

        self.agent = create_react_agent(
            model=self.model,
            name="GmailAgent",
            prompt="""You are a helpful assistant that can help with Gmail tasks. You can read, send, and delete emails. You can also search for emails based on various criteria.""",
            tools=self.tools,
        )

    async def call_model(self, state):
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

        if args:
            user_text = args[0]
        else:
            user_text = kwargs.get("input", "")

        result = await graph.ainvoke(
            {"messages": [("user", user_text)]},
        )

        # return "No response from the agent." # debugging
        messages = result.get("messages", [])
        if not messages:
            return "No response from the agent."

        last = messages[-1]
        if isinstance(last, tuple) and len(last) == 2:
            return last[1]

        return getattr(last, "content", str(last))
