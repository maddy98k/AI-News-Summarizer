# 📰 AI News Summarizer

An AI-powered News Summarizer built using **Python, Gradio, Gemini, Tavily, and LangChain**.

This application allows users to search for the latest news and receive concise, easy-to-understand summaries using AI.

---

## 🚀 Features

- 🔍 Search for news using Tavily
- 🤖 AI-powered summaries using Google Gemini
- 📝 Short and simple bullet-point summaries
- 🎨 Modern dark-themed UI
- ⚡ Fast and user-friendly interface
- 🗑 Clear search and results
- ⌨️ Press Enter to search

---

## 🛠️ Technologies Used

- **Python** – Programming language
- **Gradio** – User interface
- **Google Gemini** – AI-powered summarization
- **Tavily** – Web search
- **LangChain** – AI workflow and prompt management
- **python-dotenv** – Environment variable management

---

## 📂 Project Structure

```text
AI-News-Summarizer/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
└── .gitignore
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

```bash
cd AI-News-Summarizer
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 API Key Configuration

Create a `.env` file in the project root directory.

Add your API keys:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### API Keys

- Google Gemini API:
  https://aistudio.google.com/

- Tavily API:
  https://tavily.com/

**Never share your API keys publicly.**

---

## ▶️ Run the Application

Start the application using:

```bash
python app.py
```

After running, Gradio will provide a local URL.

Open the URL in your browser to use the AI News Summarizer.

---

## 🔄 How It Works

```text
User enters a search query
          ↓
Tavily searches the web
          ↓
Search results are collected
          ↓
LangChain sends results to Gemini
          ↓
Gemini summarizes the news
          ↓
Summary displayed in Gradio UI
```

---

## 💡 Example Queries

```text
Latest AI news in 2026
```

```text
Latest technology news
```

```text
Current space exploration updates
```

```text
Latest developments in artificial intelligence
```

---

## 🧠 LangChain Workflow

The application uses a LangChain pipeline:

```python
chain = prompt | model | StrOutputParser()
```

### Workflow

1. **ChatPromptTemplate** – Creates the summarization prompt.
2. **ChatGoogleGenerativeAI** – Generates the AI response.
3. **StrOutputParser** – Converts the response into a string.

---

## 🔮 Future Improvements

- Add news categories
- Display news sources and links
- Add date-based filtering
- Support multiple languages
- Add voice-based search
- Improve summary accuracy
- Deploy the application online

---



---

## ⭐ Project Highlights

This project demonstrates:

- Generative AI integration
- API integration
- Prompt engineering
- LangChain pipelines
- Web search automation
- Gradio UI development
- Environment variable management