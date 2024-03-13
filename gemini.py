import fitz
import getpass
import json
import os
from dotenv import load_dotenv

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_google_genai import GoogleGenerativeAI

load_dotenv()


class Document(BaseModel):
    question: str = Field(description="Question")
    option_a: str = Field(description="Option 1")
    option_b: str = Field(description="Option 2")
    option_c: str = Field(description="Option 3")
    option_d: str = Field(description="Option 4")
    correct_answer: str = Field(description="Correct answer")
    remark: str = Field(description="Remark")


def load_pdf():
    doc = fitz.open('quiz.pdf')
    pages = ""
    for page in doc:
        pages += page.get_text()
    return pages


def initialize_gemini_model():
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = getpass.getpass("AIzaSyCL6P36tSFVLCcEN5q_U-psAkiTmQODHJs")

    pages = load_pdf()
    parser = JsonOutputParser(pydantic_object=Document)
    prompt = PromptTemplate(
        template="Extract the information as specified but it will be an array of object return all data from pages and donot repeat if question already exists.{format_instructions}\n{context}\n",
        input_variables=["context"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    llm = GoogleGenerativeAI(model="gemini-pro", temperature="0", convert_system_message_to_human=True)

    chain = prompt | llm | parser
    response = chain.invoke({
        "context": pages
    })
    converted_response = json.dumps(response)
    return converted_response


def main_function():
    response = initialize_gemini_model()
    print(response)


if __name__ == "__main__":
    main_function()
