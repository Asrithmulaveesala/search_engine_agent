
from langchain.chat_models import init_chat_model
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import (
    create_tool_calling_agent,
    AgentExecutor,
)


def create_search_agent(groq_api_key: str, pdf_path: str = None):

    if not groq_api_key or not groq_api_key.strip():
        raise ValueError("Please provide a Groq API key.")

    llm = init_chat_model(
        "groq:openai/gpt-oss-120b",
        api_key=groq_api_key.strip()
    )

    # Arxiv tool
    arxiv_wrapper = ArxivAPIWrapper(
        top_k_results=1,
        doc_content_chars_max=500
    )
    arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

    # Wikipedia tool
    wiki_wrapper = WikipediaAPIWrapper(
        top_k_results=1,
        doc_content_chars_max=500,
        lang="en"
    )
    wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)

    # Always available
    tools = [arxiv, wiki]

    # Add PDF RAG only if a PDF was uploaded
    if pdf_path:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        if not documents:
            raise ValueError("The uploaded PDF contains no readable pages.")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = splitter.split_documents(documents)

        embeddings = OllamaEmbeddings(
            model="nomic-embed-text:latest"
        )

        vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=embeddings
        )

        retriever = vector_store.as_retriever(
            search_kwargs={"k": 3}
        )

        @tool
        def pdf_rag(question: str) -> str:
            """Answer questions using the PDF uploaded by the user."""

            retrieved_docs = retriever.invoke(question)

            if not retrieved_docs:
                return "No relevant information was found in the PDF."

            context = "\n\n".join(
                doc.page_content for doc in retrieved_docs
            )

            prompt_text = f"""
            Answer using only the PDF context below.
            If the answer is unavailable, say so clearly.

            Context:
            {context}

            Question:
            {question}
            """

            return llm.invoke(prompt_text).content

        tools.append(pdf_rag)

    # Agent prompt
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an intelligent AI Search Engine Assistant.

            Automatically decide which available tool to use.

            - Use Arxiv for academic papers and scientific research.
            - Use Wikipedia for general knowledge and factual questions.
            - Use PDF RAG for questions about an uploaded PDF,
              but only when that tool is available.
            - Answer directly when no tool is necessary.
            - Never ask the user to select a tool.
            - Never claim to have used a tool unless you did."""
        ),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        handle_parsing_errors=True
    )

