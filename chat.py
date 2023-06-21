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
from cachetools import TTLCache

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
CACHE_SIZE, CACHE_TIME = int(os.getenv("CACHE_SIZE")), int(os.getenv("CACHE_TIME"))


cache = TTLCache(maxsize=CACHE_SIZE, ttl=CACHE_TIME)



def load_instruction(filename):
    f = open(filename)
    return f.read()

def load_chat(address, is_new_chat):
    if is_new_chat:
        if address in cache:
            cache.pop(address)
        cache[address] = load_new_chat()
        return cache[address]
    
    if address not in cache:
        raise Exception("Chat not found try again")
    
    return cache[address]

def load_new_chat():
    chat = ChatOpenAI(temperature=0)

    instructions = load_instruction('./CHATBOT_INSTRUCTIONS.txt')
    system_message_prompt = SystemMessagePromptTemplate.from_template(instructions)

    system_message_prompt.format_messages()
    human_template = """
    You are a medical API that is trying to help a patient with their medical needs. as such your output should have JSON format.
    Your JSON response format should have the following keys:
    message "any and all messages including explanations and apologies",
    specialization "the specialization"

    message should contain any and all outputs you have including explanations and apologies.
    specialization is where you write the specialization as a string, if you don't have any specialization narrowed down leave it as an empty string

    Please remember to include any explanations or apologies within the 'message' field of the JSON response.
    If the input doesn't fit the provided context, provide your output in the JSON response format with an empty specialization field.
    Your output should always just be JSON Response with the message field and specialization field.

    for example: for the cases where the user is giving you inputs which are out of context, instead of just outputing this "My apologies, but I am a medical assistant chatbot API and I am not able to answer that question. Can I assist you with any medical concerns or symptoms you may be experiencing?"
    you should instead output it as 
    message: "My apologies, but I am a medical assistant chatbot API and I am not able to answer that question. Can I assist you with any medical concerns or symptoms you may be experiencing?", and leave the specialization empty


    for the cases where the patient is giving you valid inputs
    Your JSON response format should have the following keys:
    message
    specialization

    message is where you put any and all messages including explanations and apologies as a string.
    specialization is where you write the specialization as a string, if you don't have any specialization narrowed down leave it as an empty string
    you will then output this JSON Object.

    if the user provides no input, you should prompt them to provide an input.
    
    input = {input}
    """
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([
        system_message_prompt,
        MessagesPlaceholder(variable_name="history"),
        human_message_prompt
    ])

    memory = ConversationBufferMemory(input_key = "input", output_key="response", return_messages=True)
    conversation = ConversationChain(memory=memory, prompt=chat_prompt, llm=chat)
    return conversation