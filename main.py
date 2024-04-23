from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables, describe_tables_tool
from tools.report import write_report_tool
from handlers.chat_model_start_handler import ChatModelStartHandler


#load environment variables
load_dotenv()

#create handler
handler = ChatModelStartHandler()

#create chat model
chat = ChatOpenAI(
    callbacks = [handler] #passing handler to chat model
)

#get all table names
tables = list_tables()

#create chat prompt template
prompt = ChatPromptTemplate(
    messages = [
        SystemMessage(content=(
            "You are an AI that has access to an SQLite databse.\n"
            f"The database has tables of: {tables}\n"
            "Do not make any assumptions about what tables exist "
            "or what columns exist. Instead, use the 'describe_tables' function"
        )),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)


#creating conversation memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

#list of tools
tools = [run_query_tool, describe_tables_tool, write_report_tool]

#create agent (~ a chain that knows how to use tools)
agent = OpenAIFunctionsAgent(
    llm = chat,
    prompt = prompt,
    tools = tools
)

#create agent executor (~ while loop)
agent_executor = AgentExecutor(
    agent = agent,
    # verbose = True,
    tools = tools,
    memory = memory
)


#run agent executor
# agent_executor("How many users are in the database")
agent_executor("How many orders are there? Write the result to an html report.")

agent_executor("Repeat the exact same process for users.")
