import getpass
import google.generativeai as genai
import os
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.pgvector import PGVector
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("AIzaSyCL6P36tSFVLCcEN5q_U-psAkiTmQODHJs")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

loader = PyPDFLoader("civil-code.pdf")
pages = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=1000)

chunks = text_splitter.split_documents(pages)

# vector_embeddings = embeddings.embed_query(chunks)
print(chunks
      )
#
# llm = ChatGoogleGenerativeAI(model="gemini-pro", client=genai,
#                              temperature="0.7")
