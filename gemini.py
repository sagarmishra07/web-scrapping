import fitz
import getpass
import json
import os
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_google_genai import GoogleGenerativeAI


class Document(BaseModel):
    question: str = Field(description="Question")
    option_a: str = Field(description="Option 1")
    option_b: str = Field(description="Option 2")
    option_c: str = Field(description="Option 3")
    option_d: str = Field(description="Option 4")
    correct_answer: str = Field(description="Correct answer")
    remark: str = Field(description="Remark")


# api_key = getpass()
#
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("AIzaSyCL6P36tSFVLCcEN5q_U-psAkiTmQODHJs")

# # load pdf

pdf_file = 'quiz.pdf'

loader = PyPDFLoader(pdf_file)

pages = loader.load()

parser = JsonOutputParser(pydantic_object=Document)
prompt = PromptTemplate(
    template="Extract the information as specified but it will be and array of object and object is seperated after 7 line in pdf return all data from pages.\n{format_instructions}\n{context}\n",
    input_variables=["context"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
llm = GoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)

chain = prompt | llm | parser
response = chain.invoke({
    "context": pages
})
with open("gemini_output.json", "w") as write_file:
    converted_response = json.loads(response)
    json.dump(converted_response, write_file)
