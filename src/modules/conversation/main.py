from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, AIMessageChunk
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
from typing import Dict, List

from langgraph.graph.message import MessagesState

# from src.helpers.voice.main import speak, listen

from src.helpers.cli.main import speak, listen
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from src.tools.datetime_tool import get_datetime
from src.tools.websearch_tool import websearch
from src.tools.redditsearch_tool import redditsearch
from src.tools.gmail_tool import gmail_tool

import datetime as dt

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

memory = MemorySaver()

chat_agent = create_react_agent(
    model=model,
    name="VoiceAgent",
    prompt=f"""Today is {dt.date.today()},You are a voice assistant. Respond to the user's queries in a friendly and helpful, but slightly playful manner. Don't use emojis. Respond in a manner that is best for a text-to-speech agent
    you can call get_datetime({{timezone=timezone}}) or get_datetime({{timezone, fmt}}).
    you can search the web using websearch({{query}}).
    you can search reddit - preference this over websearch if searching reddit using redditsearch({{query, sort, time_filter, subreddit, limit}}) or redditsearch({{query}}).
    you can also use gmail_tool({{query}}) to parse the query to another agent to send, read, and delete emails.
    """,
    tools=[
        get_datetime,
        websearch,
        redditsearch,
        gmail_tool,
    ],
)


class Agent:

    async def call_model(self, state: MessagesState):
        config = RunnableConfig(configurable={"thread_id": "1"})
        response = await chat_agent.ainvoke(state, config=config)
        return response

    async def run(self, *args, **kwargs):
        graph = (
            StateGraph(MessagesState)
            .add_node(self.call_model)
            .add_edge(START, "call_model")
            .compile(checkpointer=memory)
        )

        speak("Hello! How can I help you today?")

        while True:
            user_input = listen(timeout=10)

            if not user_input:
                speak("I didn't catch that. Could you repeat?")
                continue

            if "stop" in user_input:
                speak("Okay, ending the conversation. Have a great day!")
                break

            # Fallback to LLM chat
            else:

                text_buffer = ""

                config = RunnableConfig(configurable={"thread_id": "1"})
                async for node_result, metadata in graph.astream(
                    {"messages": [HumanMessage(content=user_input)]},
                    config=config,
                    stream_mode="messages",
                ):

                    msg = getattr(node_result, "content", None)

                    if isinstance(node_result, AIMessageChunk):
                        print(msg, end="", flush=True)

                        if not msg:
                            continue

                        text_buffer += msg

                        if (
                            text_buffer.endswith(("\n", ".", "!", "?"))
                            or len(text_buffer) > 256
                        ):
                            speak(text_buffer)
                            text_buffer = ""

                if text_buffer:
                    speak(text_buffer)
