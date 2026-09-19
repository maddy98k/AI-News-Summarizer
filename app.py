import gradio as gr
from dotenv import load_dotenv

load_dotenv()

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ============================================================
# AI MODEL
# ============================================================

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0.2,
    max_output_tokens=300
)


# ============================================================
# TAVILY SEARCH
# ============================================================

search_tool = TavilySearchResults(max_results=5)


# ============================================================
# PROMPT
# ============================================================

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful assistant.

Summarize the following news into clear bullet points
in short and simple language.

{news}
"""
)


# ============================================================
# LANGCHAIN CHAIN
# ============================================================

chain = prompt | model | StrOutputParser()


# ============================================================
# SEARCH FUNCTION
# ============================================================

def search_news(user_input):

    if not user_input.strip():
        return "⚠️ Please enter a search query."

    try:
        # Tavily search
        news_result = search_tool.invoke(user_input)

        # Gemini response
        result = chain.invoke({
            "news": news_result
        })

        return result

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ============================================================
# CUSTOM CSS
# ============================================================

css = """

/* Main background */
.gradio-container {
    max-width: 1100px !important;
    margin: auto !important;
    background: #0b0f19 !important;
    color: white !important;
}

/* Header */
.header {
    text-align: center;
    padding: 35px 20px 20px 20px;
}

.header h1 {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 8px;
}

.header p {
    color: #9ca3af;
    font-size: 16px;
}

/* Search box */
.search-box textarea {
    background: #111827 !important;
    border: 1px solid #263244 !important;
    border-radius: 14px !important;
    color: white !important;
    font-size: 16px !important;
}

/* Buttons */
.search-btn {
    background: #6366f1 !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

.search-btn:hover {
    background: #4f46e5 !important;
}

.clear-btn {
    background: #1f2937 !important;
    color: white !important;
    border: 1px solid #374151 !important;
    border-radius: 12px !important;
}

.clear-btn:hover {
    background: #374151 !important;
}

/* Result */
.result-box {
    background: #111827 !important;
    border: 1px solid #263244 !important;
    border-radius: 16px !important;
    padding: 10px !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #6b7280;
    font-size: 13px;
    padding: 25px;
}

"""


# ============================================================
# GRADIO UI
# ============================================================

with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="indigo",
        neutral_hue="slate"
    ),
    css=css,
    title="AI News Summarizer"
) as demo:

    # Header
    gr.HTML(
        """
        <div class="header">
            <h1>📰 AI News Summarizer</h1>
            <p>
                Search the web and get concise AI-powered news summaries.
            </p>
        </div>
        """
    )

    # Search input
    query = gr.Textbox(
        label="Search",
        placeholder="Example: Latest AI news in 2026...",
        lines=2,
        elem_classes="search-box"
    )

    # Buttons
    with gr.Row():

        search_button = gr.Button(
            "🔍 Search",
            variant="primary",
            elem_classes="search-btn"
        )

        clear_button = gr.Button(
            "🗑 Clear",
            elem_classes="clear-btn"
        )

    # Result
    output = gr.Markdown(
        value="### AI Summary\n\nYour search results will appear here.",
        elem_classes="result-box"
    )

    # Footer
    gr.HTML(
        """
        <div class="footer">
            Powered by Gemini + Tavily + LangChain
        </div>
        """
    )


    # Search event
    search_button.click(
        fn=search_news,
        inputs=query,
        outputs=output
    )


    # Enter key
    query.submit(
        fn=search_news,
        inputs=query,
        outputs=output
    )


    # Clear button
    clear_button.click(
        fn=lambda: ("", "### AI Summary\n\nYour search results will appear here."),
        inputs=None,
        outputs=[query, output]
    )


# ============================================================
# LAUNCH
# ============================================================

demo.launch()