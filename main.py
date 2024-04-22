from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv

from tools.sql import run_query_tool

#load environment variables
load_dotenv()

#create chat model
chat = ChatOpenAI()

#create chat prompt template
prompt = ChatPromptTemplate(
    messages = [
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
)


tools = [run_query_tool]

#create agent (~ a chain that knows how to use tools)
agent = OpenAIFunctionsAgent(
    llm = chat,
    prompt = prompt,
    tools = tools
)

#create agent executor (~ while loop)
agent_executor = AgentExecutor(
    agent = agent,
    verbose = True,
    tools = tools
)


#run agent executor
agent_executor("How many users are in the database")
