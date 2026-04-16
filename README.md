# SupportLens

A RAG-powered customer support bot that answers questions from a company's own knowledge base — 24 hours a day, 7 days a week. When it doesn't know the answer, it escalates to a human agent instead of guessing.

**Live Demo:** https://supportlens-h8qqiopqkjeqcfzt3dsdmf.streamlit.app

---

## The Problem It Solves

Most small businesses can only offer customer support during working hours. But customers have questions at midnight, on weekends, and during public holidays. Every unanswered question is a potential lost sale or a frustrated customer.

Generic chatbots make this worse — they answer from the internet, not from your specific business documents. So customers get plausible-sounding but incorrect answers about your policies, pricing, and products.

SupportLens fixes both problems. It runs 24/7 and answers only from documents you provide.

---

## How It Works

1. Company documents (FAQs, product guides, policies) are loaded from a `docs` folder
2. Documents are split into chunks and converted into embeddings using OpenAI
3. Embeddings are stored in a local ChromaDB vector database
4. When a customer asks a question, the 3 most relevant chunks are retrieved
5. GPT-4o-mini reads only those chunks to generate a grounded answer
6. If the answer is not in the knowledge base, the bot escalates to a human agent

This pattern is called **RAG (Retrieval-Augmented Generation)**.

---

## Key Features

- **Grounded answers** — responds only from your documents, never the internet
- **Graceful escalation** — tells customers to contact a human agent when it doesn't know
- **Zero-upload interface** — knowledge base loads automatically on startup
- **Cached vector store** — database is built once, not on every question
- **Easy to customise** — swap the docs folder contents to deploy for any business

---

## Tech Stack

| Layer | Tool |
|---|---|
| UI | Streamlit |
| LLM | GPT-4o-mini (OpenAI) |
| Embeddings | OpenAI text-embedding-ada-002 |
| Vector Store | ChromaDB |
| Orchestration | LangChain (LCEL) |
| Document Loading | DirectoryLoader + TextLoader |
| Environment | python-dotenv |

---

## Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/DataBuster204/supportlens.git
cd supportlens
```

**2. Create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your OpenAI API key**

Create a `.env` file in the root folder:
```
OPENAI_API_KEY=your-key-here
```

**5. Add your knowledge base**

Place your company documents as `.txt` files inside the `docs/` folder. The app will automatically load everything in that folder on startup.

**6. Run the app**
```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## Customising for a Client

To deploy SupportLens for a specific business:

1. Replace the contents of the `docs/` folder with the client's documents
2. Update the company name and contact details in `app.py`
3. Push to GitHub and redeploy on Streamlit Cloud
4. Provide the client with the live URL or embed it on their website using an iframe

The entire RAG pipeline requires no changes — only the documents and branding need updating.

---

## Project Structure

```
supportlens/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── docs/               # Company knowledge base (txt files)
│   └── faq.txt         # Sample FAQ document
├── .env                # API key (not committed to GitHub)
├── .gitignore          # Excludes .env, venv, ChromaDB files
└── .chroma/            # Local vector store (auto-created on first run)
```

---

## Use Cases

- **Healthcare** — patients make enquiries ahead of appointments
- **Legal firms** — clients ask about services, fees, and procedures
- **E-commerce** — customers ask about orders, returns, and shipping
- **SaaS platforms** — users get instant answers about features and billing
- **Schools** — parents and students query admissions and policies

---

## Built By

**Olumide Daramola** — NVIDIA-certified Generative AI Developer
[Portfolio](https://olumidedaramola.dev) · [GitHub](https://github.com/DataBuster204)
