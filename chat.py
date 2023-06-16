import os
from dotenv import load_dotenv
import openai
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import json


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_instruction(filename):
    f = open(filename)
    return f.read()

def load_chat():
    chat = ChatOpenAI(temperature=0)

    instructions = load_instruction('./CHATBOT_INSTRUCTIONS.txt')
    system_message_prompt = SystemMessagePromptTemplate.from_template(instructions)

    system_message_prompt.format_messages()
    human_template = """
    when conversing your output should be formatted as JSON with the following keys:
    message
    specializations

    message is where you put your normal messages
    specializations is where you write the specializations as a list of strings, if you don't have any specializations narrowed down leave the list empty
    to repeat you are a medical assistant api, so you should strictly follow the output format

    input = {input}
    """
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([
        system_message_prompt,
        MessagesPlaceholder(variable_name="history"),
        human_message_prompt
    ])

    memory = ConversationBufferMemory(input_key = "input", output_key="response", return_messages=True)
    conversation = ConversationChain(memory=memory, prompt=chat_prompt, llm=chat, verbose=True)

    return conversation