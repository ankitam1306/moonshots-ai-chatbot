# 🚀 Moonshots

A collection of innovative projects and experiments.

## Launchbot

Launchbot is an intelligent chatbot that provides instant answers to LaunchDarkly documentation questions using RAG (Retrieval-Augmented Generation) technology.

### Architecture

The project consists of two main components:

- **launchbot/** - Python FastAPI backend with RAG implementation
- **launchbot-ui/** - React TypeScript frontend with real-time streaming UI

### Features

- 🤖 **AI-Powered Answers**: Uses OpenAI GPT-4 to generate accurate, context-aware responses
- 📚 **Documentation Search**: Semantic search over LaunchDarkly documentation using Pinecone vector database
- ⚡ **Real-time Streaming**: Streams responses token-by-token for instant feedback
- 🔗 **Source Citations**: Provides source links for all answers
- 🎨 **Syntax Highlighting**: Code snippets are beautifully formatted with PrismJS
- 🕷️ **Auto-Indexing**: Web crawler to automatically scrape and index LaunchDarkly docs

---

## Backend (launchbot/)

### Tech Stack

- **FastAPI** - Modern, high-performance web framework
- **LangChain** - Framework for building LLM applications
- **Pinecone** - Vector database for semantic search
- **OpenAI GPT-4** - Large language model for generating responses
- **BeautifulSoup4** - Web scraping library

### Project Structure

```
launchbot/
├── main.py                          # FastAPI server entry point
├── bot.py                           # RAG retrieval logic with streaming
├── crawler.py                       # Web crawler for LaunchDarkly docs
├── index_documents_in_pinecone.py   # Script to index documents
├── config.py                        # Configuration and initialization
├── model.py                         # Pydantic models
└── requirements.txt                 # Python dependencies
```

### Setup

1. **Create a virtual environment**:

   ```bash
   cd launchbot
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the `launchbot/` directory:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_INDEX_NAME=your_index_name
   PINECONE_ENVIRONMENT=your_environment
   ```

4. **Index the documentation** (first time only):

   ```bash
   python index_documents_in_pinecone.py
   ```

   This will crawl LaunchDarkly documentation and store embeddings in Pinecone.

5. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`

### API Endpoints

#### `POST /ask`

Ask a question and receive a streaming response.

**Request Body**:

```json
{
  "question": "How do you install ldcli on macOS using Homebrew?"
}
```

**Response**: Server-Sent Events (SSE) stream with:

- Streamed answer tokens
- Source documents at the end

---

## Frontend (launchbot-ui/)

### Tech Stack

- **React 19** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first CSS framework
- **PrismJS** - Syntax highlighting
- **React Icons** - Icon library

### Project Structure

```
launchbot-ui/
├── src/
│   ├── Launchbot.tsx                # Main chat component
│   ├── components/
│   │   ├── ChatInput.tsx            # Message input component
│   │   ├── MessageBubble.tsx        # Chat message display
│   │   └── TypingLoader/            # Typing animation
│   ├── hooks/
│   │   └── useLaunchbotQuery.ts     # Custom hook for API calls
│   ├── utils/
│   │   └── highlightContent.ts      # Markdown & code highlighting
│   └── stylesheets/
│       └── Launchbot.css            # Main styles
├── package.json
└── vite.config.ts
```

### Setup

1. **Install dependencies**:

   ```bash
   cd launchbot-ui
   npm install
   ```

2. **Start the development server**:

   ```bash
   npm run dev
   ```

   The UI will be available at `http://localhost:5173`

3. **Build for production**:
   ```bash
   npm run build
   ```

### Features

- **Real-time Streaming**: Messages stream in character-by-character
- **Markdown Support**: Renders formatted responses with headers, lists, and code blocks
- **Syntax Highlighting**: Automatically highlights code snippets
- **Source Links**: Displays documentation sources for each answer
- **Responsive Design**: Works on desktop and mobile devices

---

## Development Workflow

### Running Locally

1. **Terminal 1** - Start the backend:

   ```bash
   cd launchbot
   source venv/bin/activate
   uvicorn main:app --reload
   ```

2. **Terminal 2** - Start the frontend:

   ```bash
   cd launchbot-ui
   npm run dev
   ```

3. Open `http://localhost:5173` in your browser

### Re-indexing Documentation

If LaunchDarkly documentation is updated, re-index:

```bash
cd launchbot
python index_documents_in_pinecone.py
```

---

## How It Works

1. **Indexing Phase** (one-time):

   - Crawler scrapes LaunchDarkly documentation
   - Documents are split into chunks
   - Chunks are embedded using OpenAI embeddings
   - Embeddings are stored in Pinecone vector database

2. **Query Phase** (real-time):
   - User asks a question in the UI
   - Frontend sends question to backend API
   - Backend retrieves relevant document chunks from Pinecone
   - LangChain constructs a prompt with context
   - GPT-4 generates an answer based on context
   - Answer streams back to the frontend in real-time
   - Sources are displayed with the answer

---

## 💬 Sample Questions & Answers

Here are some example questions you can ask Launchbot and the type of responses you'll receive:

### Example 1: Installation Instructions

**Question**: _"How do you install ldcli on macOS using Homebrew?"_

**Answer**:

> **Installing ldcli on macOS using Homebrew**
>
> To install the LaunchDarkly CLI (ldcli) on macOS using Homebrew, follow these steps:
>
> 1. **Add the LaunchDarkly tap**:
>
>    ```bash
>    brew tap launchdarkly/tap
>    ```
>
> 2. **Install ldcli**:
>
>    ```bash
>    brew install ldcli
>    ```
>
> 3. **Verify the installation**:
>    ```bash
>    ldcli version
>    ```
>
> This will install the latest version of ldcli on your system.
>
> **Sources**:
>
> - https://launchdarkly.com/docs/cli/installation
> - https://launchdarkly.com/docs/cli/getting-started

---

### Example 2: Authentication

**Question**: _"Which environment variable is used to authenticate ldcli with LaunchDarkly?"_

**Answer**:

> **Authentication Environment Variable**
>
> The environment variable used to authenticate ldcli with LaunchDarkly is **`LD_ACCESS_TOKEN`**.
>
> You can set it in your terminal:
>
> ```bash
> export LD_ACCESS_TOKEN=your_access_token_here
> ```
>
> Alternatively, you can pass the access token directly using the `--access-token` flag with any ldcli command:
>
> ```bash
> ldcli --access-token YOUR_TOKEN command
> ```
>
> **Note**: Access tokens can be created in the LaunchDarkly dashboard under Account Settings → Authorization.
>
> **Sources**:
>
> - https://launchdarkly.com/docs/cli/authentication

---

### Example 3: Feature Flag Concepts

**Question**: _"What is a guarded rollout and how can I use that?"_

**Answer**:

> **Guarded Rollouts in LaunchDarkly**
>
> A **guarded rollout** is a feature release strategy that allows you to gradually roll out a feature to your users while monitoring key metrics and automatically halting the rollout if issues are detected.
>
> **How it works:**
>
> 1. **Set up metrics**: Define success metrics and guardrail metrics in LaunchDarkly
> 2. **Configure the rollout**: Specify the percentage increase over time (e.g., 10% every hour)
> 3. **Enable guardrails**: The system monitors your metrics in real-time
> 4. **Automatic protection**: If guardrail metrics exceed thresholds, the rollout automatically pauses
>
> **Example use case:**
>
> ```
> Rolling out a new checkout flow:
> - Start with 5% of users
> - Increase by 10% every 2 hours
> - Monitor: conversion rate, error rate, page load time
> - Auto-pause if error rate > 2% or conversion drops > 5%
> ```
>
> **Benefits:**
>
> - Reduces risk of widespread issues
> - Provides automated safeguards
> - Allows data-driven rollout decisions
> - Easy rollback if problems occur
>
> **Sources**:
>
> - https://launchdarkly.com/docs/home/releases/guarded-rollouts
> - https://launchdarkly.com/docs/home/experimentation

---

### Example 4: Quick Reference

**Question**: _"How to create an access token?"_

**Answer**:

> **Creating an Access Token in LaunchDarkly**
>
> To create an access token:
>
> 1. Navigate to **Account Settings** → **Authorization**
> 2. Click **Create token**
> 3. Enter a **name** for your token
> 4. Select a **role** (Reader, Writer, Admin, or custom role)
> 5. Optionally set an **expiration date**
> 6. Click **Save token**
> 7. **Copy the token immediately** - it won't be shown again!
>
> **Token Types:**
>
> - **Personal access tokens**: Tied to your user account
> - **Service tokens**: For automated systems and integrations
>
> **Best Practices:**
>
> - Use least-privilege roles
> - Set expiration dates for security
> - Rotate tokens regularly
> - Never commit tokens to version control
>
> **Sources**:
>
> - https://launchdarkly.com/docs/home/account-security/api-access-tokens

---

### Example 5: Managing Feature Flags

**Question**: _"How do I archive or delete old feature flags?"_

**Answer**:

> **Archiving and Deleting Feature Flags**
>
> LaunchDarkly allows you to archive or delete feature flags that are no longer needed. Here's how:
>
> **Archiving Flags (Recommended)**
>
> Archiving is the safer option as it preserves flag data and history:
>
> 1. Navigate to your **Feature Flags** list
> 2. Click on the flag you want to archive
> 3. Click the **Settings** tab
> 4. Scroll to the bottom and click **Archive flag**
> 5. Confirm the action
>
> **What happens when you archive:**
>
> - Flag becomes read-only across all environments
> - Flag disappears from the main flags list (accessible via "Archived" filter)
> - Historical data is preserved
> - Can be restored later if needed
>
> **Deleting Flags (Permanent)**
>
> ⚠️ **Warning**: Deletion is permanent and cannot be undone.
>
> 1. First, the flag must be **archived**
> 2. Go to the archived flags list
> 3. Open the archived flag
> 4. In Settings, click **Delete flag**
> 5. Type the flag key to confirm
> 6. Click **Delete permanently**
>
> **Best Practices:**
>
> - ✅ **Archive instead of delete** to maintain audit trails
> - ✅ Remove flag references from code before archiving
> - ✅ Use the Code References feature to find all flag usages
> - ✅ Communicate with your team before archiving flags
> - ✅ Test in lower environments first
> - ❌ Don't delete flags that might be referenced in production code
>
> **Using the CLI:**
>
> ```bash
> # Archive a flag
> ldcli flags archive --flag-key my-flag-key --project my-project
>
> # Delete a flag (must be archived first)
> ldcli flags delete --flag-key my-flag-key --project my-project
> ```
>
> **Tip**: Enable the "Code References" integration to automatically detect where flags are used in your codebase before archiving them.
>
> **Sources**:
>
> - https://launchdarkly.com/docs/home/flags/archive-delete
> - https://launchdarkly.com/docs/home/code/flag-archive
> - https://launchdarkly.com/docs/cli/flags

---

### More Questions You Can Try

- "What are feature flag targeting rules?"
- "How do I set up environments in LaunchDarkly?"
- "What is the difference between client-side and server-side SDKs?"
- "How do I use flag variations and fallback values?"
- "What are segments and how do I create them?"
- "How to integrate LaunchDarkly with React?"
- "What is the relay proxy and when should I use it?"
- "What metrics can I track with LaunchDarkly?"
- "How does flag evaluation work?"
- "How to check usage information?"

---

## Environment Variables

### Backend (.env in launchbot/)

| Variable               | Description                             |
| ---------------------- | --------------------------------------- |
| `OPENAI_API_KEY`       | OpenAI API key for GPT-4 and embeddings |
| `PINECONE_API_KEY`     | Pinecone API key                        |
| `PINECONE_INDEX_NAME`  | Name of your Pinecone index             |
| `PINECONE_ENVIRONMENT` | Pinecone environment region             |

---

## Future Enhancements

- [ ] Add conversation history/memory
- [ ] Support multi-turn conversations
- [ ] Add authentication
- [ ] Deploy to production
- [ ] Add more documentation sources
- [ ] Implement caching for common queries
- [ ] Add analytics and usage tracking
- [ ] Voice input support
- [ ] Export conversation history

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## License

MIT License
