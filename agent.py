from crewai import Crew, Task, Agent
from crewai_tools import SerperDevTool
#from langchain_ibm import WatsongxLLM
import os
# Use a pipeline as a high-level helper
from transformers import pipeline

messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe = pipeline("text-generation", model="nvidia/Llama-3.1-Nemotron-70B-Instruct-HF")
pipe(messages)
#os.environ["WATSONX_APIKEY" = ""]
#os.environ["SERPER_API_KEY" = ""]

#Parameters
parameters = {"decoding_method":"greedy", "max_new_tokens":500}

#Create the first LLM
#llm = WatsongxLLM(model_id="meta")