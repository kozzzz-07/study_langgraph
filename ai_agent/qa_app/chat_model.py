from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import ConfigurableField

from dotenv import load_dotenv


load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite-preview-06-17", temperature=0)
# llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0)

llm.configurable_fields(max_output_tokens=ConfigurableField(id="max_output_tokens"))
