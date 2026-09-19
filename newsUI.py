import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI News Summarizer",
    page_icon="📰",
    layout="centered"
)


# -----------------------------
# Title
# -----------------------------

st.title("📰 AI News Summarizer")
st.write("Search the web and get a short, simple summary.")


# -----------------------------
# Gemini Model
# -----------------------------

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0.2,
    max_output_tokens=300
)


# -----------------------------
# Tavily Search
# -----------------------------

search_tool = TavilySearchResults(max=5)


# -----------------------------
# Prompt
# -----------------------------

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful assistant.

Summarize the following news into clear bullet points
in short and simple language.

{news}
"""
)


# -----------------------------
# LangChain Chain
# -----------------------------

chain = prompt | model | StrOutputParser()


# -----------------------------
# User Input
# -----------------------------

user_input = st.text_input(
    "Enter your query",
    placeholder="Example: Latest AI news"
)


# -----------------------------
# Search Button
# -----------------------------

if st.button("Search"):

    if user_input:

        with st.spinner("Searching and summarizing..."):

            # Web search
            news_result = search_tool.invoke(user_input)

            # LLM response
            result = chain.invoke({
                "news": news_result
            })

        st.subheader("AI Summary")
        st.write(result)

    else:
        st.warning("Please enter a query.")


# -----------------------------
# Clear Button
# -----------------------------

if st.button("Clear"):
    st.rerun()
