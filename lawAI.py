from langchain.prompts import PromptTemplate
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
import getpass
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain

# api_key = getpass()
#
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("AIzaSyCL6P36tSFVLCcEN5q_U-psAkiTmQODHJs")

#
#
# question = "Tell me a short poem about snow?"
#

# # load pdf
loader = PyPDFLoader("civil-code.pdf")
pages = loader.load_and_split()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
context = "\n\n".join(str(p.page_content) for p in pages)
texts = text_splitter.split_text(context)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature="0.5",convert_system_message_to_human=True)
vector_index = Chroma.from_texts(texts, embeddings).as_retriever()

# template
prompt_template = """
 You are an AI assistant for answering questions about the act of Nepal. You are given the
a long document and a question. Provide answer in a simple terms, try to explain each
difficult terms in as simple as possible. If you don't know the answer, just say "Hmm, I'm not sure." Don't try to
make up an answer. If the question is not about the acts of nepal, politely inform them that you are tuned to
only answer questions about acts of nepal. Lastly, answer the question as if you were expert of nepal
act and include all the possible answers with act name, chapter, section and list all subsection for act if possible,
  Context:\n {context}?\n
  Question: \n{question}\n

  Answer:
"""
prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])

question = 'loss or damage related laws in nepal ?'

docs = vector_index.get_relevant_documents(question)
chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)

response = chain(
    {"input_documents":docs, "question": question}
    , return_only_outputs=True)
print(response)

