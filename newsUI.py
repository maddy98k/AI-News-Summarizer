import os
import streamlit as st
from dotenv import load_dotenv

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
# Load API Keys
# -----------------------------

load_dotenv()

os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]


# -----------------------------
# Custom CSS
# -----------------------------

st.markdown(
    """
    <style>
    .main {
        padding-top: 2rem;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .summary-box {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #444;
        margin-top: 20px;
    }

    .footer {
        text-align: center;
        margin-top: 40px;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Header
# -----------------------------

st.markdown(
    '<div class="title">📰 AI News Summarizer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Search the web and get short, simple AI-powered summaries.'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Initialize Session State
# -----------------------------

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "query" not in st.session_state:
    st.session_state.query = ""


# -----------------------------
# Gemini Model
# -----------------------------

@st.cache_resource
def load_model():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        max_output_tokens=300
    )


model = load_model()


# -----------------------------
# Tavily Search
# -----------------------------

@st.cache_resource
def load_search_tool():
    return TavilySearchResults(max_results=5)


search_tool = load_search_tool()


# -----------------------------
# Prompt
# -----------------------------

prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful news summarization assistant.

    Summarize the following news into:
    - 4 to 6 clear bullet points
    - Simple and easy English
    - Important facts only
    - Avoid unnecessary details

    Mention if the information is unclear or incomplete.

    News:
    {news}
    """
)


# -----------------------------
# LangChain Chain
# -----------------------------

chain = prompt | model | StrOutputParser()


# -----------------------------
# Example Queries
# -----------------------------

st.subheader("💡 Try an Example")

example_queries = [
    "Latest AI news",
    "Technology news today",
    "Latest space discoveries",
    "Global business news"
]

selected_example = st.selectbox(
    "Choose a topic",
    ["Select an example"] + example_queries
)

if selected_example != "Select an example":
    st.session_state.query = selected_example


# -----------------------------
# User Input
# -----------------------------

user_input = st.text_input(
    "🔍 Enter your news topic",
    value=st.session_state.query,
    placeholder="Example: Latest developments in artificial intelligence"
)


# -----------------------------
# Buttons
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    search_clicked = st.button(
        "🔎 Search & Summarize",
        use_container_width=True
    )

with col2:
    clear_clicked = st.button(
        "🧹 Clear",
        use_container_width=True
    )


# -----------------------------
# Clear Button
# -----------------------------

if clear_clicked:
    st.session_state.summary = ""
    st.session_state.query = ""

    st.rerun()


# -----------------------------
# Search and Summarize
# -----------------------------

if search_clicked:

    if not user_input.strip():
        st.warning("⚠️ Please enter a news topic.")

    else:
        try:
            with st.spinner("🔍 Searching the web..."):

                news_result = search_tool.invoke(user_input)

            with st.spinner("🤖 Generating AI summary..."):

                result = chain.invoke(
                    {
                        "news": news_result
                    }
                )

            st.session_state.summary = result

        except Exception as error:
            st.error(
                "❌ Something went wrong. "
                "Please check your API keys and try again."
            )

            st.caption(f"Error details: {error}")


# -----------------------------
# Display Summary
# -----------------------------

if st.session_state.summary:

    st.markdown("---")

    st.subheader("📰 AI-Generated Summary")

    st.markdown(
        f"""
        <div class="summary-box">
        {st.session_state.summary}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.download_button(
        label="📥 Download Summary",
        data=st.session_state.summary,
        file_name="news_summary.txt",
        mime="text/plain",
        use_container_width=True
    )


# -----------------------------
# Footer
# -----------------------------

st.markdown(
    '<div class="footer">'
    '🤖 Powered by Gemini, Tavily & LangChain'
    '</div>',
    unsafe_allow_html=True
)
