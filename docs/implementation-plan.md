# Phase-Wise Implementation Plan

> [!WARNING]
> **User Review Required: RAG Chatbot Integration**
> You requested to integrate a RAG (Retrieval-Augmented Generation) chatbot into the dashboard so the evaluator can "chat" with the 1,000+ user reviews. To build a *true* RAG system, the backend requires an active LLM API.
> 
> **Open Question:** Do you have an API key (e.g., OpenAI, Gemini, or Groq) that we can use for the backend Python server? 
> - **If YES:** I will build a real vector-database RAG pipeline using Python (LangChain/ChromaDB).
> - **If NO:** I can build a "Simulated RAG" for the prototype that uses keyword-matching to retrieve verbatim quotes from our dataset and outputs intelligent, pre-structured responses. This is perfectly acceptable for MVP demos and avoids paid APIs. Which route do you prefer?This document breaks down the end-to-end execution of the **Wishlist to Purchase Conversion** project into actionable phases and iterative sub-phases, bridging the requirements from `context.md` with the technical design in `architecture.md`.

---

## Phase 1: Environment Setup & Data Ingestion 
**Goal:** Build the foundation of the AI-Powered Discovery Engine by collecting raw user data from multiple sources.
**Corresponds to:** `architecture.md` (Ingestion & Storage Layers), `context.md` (Part 1)

### Sub-Phase 1.1: Workspace Initialization
- Set up a Python virtual environment.
- Install required dependencies: `praw` (Reddit), `google-play-scraper`, `app-store-scraper`, `pandas`.

### Sub-Phase 1.2: Raw HTML Scraping Script Development
- **Script 1 (App Reviews):** Continue using `google-play-scraper` (already complete for Play Store).
- **Script 2 (Reddit HTML Scraper):** Build a `requests` + `BeautifulSoup` scraper targeting `old.reddit.com/r/IndianFashionAddicts/search` to bypass the PRAW API requirement. We will parse the raw HTML structure to extract post titles and body text.
- **Script 3 (Quora & Forums HTML Scraper):** Build a scraper that uses custom headers (e.g., Googlebot User-Agent) to fetch raw HTML from Quora threads related to "AJIO wishlist" and parses the Q&A text blocks.
- **Script 4 (YouTube/Social Media):** Implement extraction for YouTube comments by simulating raw HTTP requests to internal AJAX endpoints, pulling comments from AJIO fashion haul videos without official API keys.

### Sub-Phase 1.3: Data Execution & Storage Validation
- Run all scripts to collect data.
- Consolidate scraped data into local `raw_data.csv` and `raw_data.json` files.
- Perform basic cleaning (removing duplicates, filtering out short/irrelevant entries).

**Deliverable:** A populated dataset containing real user conversations about fashion wishlists.

---

## Phase 2: Processing, Analytics & AI Discovery
**Goal:** Leverage Antigravity (LLM) to extract meaning, pain points, and themes from the raw data.
**Corresponds to:** `architecture.md` (Processing Layer), `context.md` (Part 1)

### Sub-Phase 2.1: Data Preprocessing Pipeline
- Write a script to clean formatting and chunk the raw data into manageable payloads for the LLM context window.

### Sub-Phase 2.2: Prompt Engineering & Testing
- Design system prompts to answer the core questions in `context.md` (*Why postpone? How do they compare? Size/Price impact?*).
- Run small tests on a subset of the data to validate that the LLM extracts meaningful and structured insights.

### Sub-Phase 2.3: Batch AI Analysis & Quantification
- Feed the entire dataset through the LLM.
- Generate structured JSON outputs categorizing primary friction points (e.g., Sizing Uncertainty, Price Tracking, Bookmarking).
- Write a small script to quantify the occurrence of each theme to rank the biggest bottlenecks.

### Sub-Phase 2.4: Discovery Engine Web Dashboard (Testable Link)
- **Backend:** Create a lightweight Python Flask server that wraps the theme analysis script (`analyze_themes.py`) into an API endpoint.
- **Frontend:** Build a premium, highly aesthetic web interface (Vanilla HTML/CSS/JS with glassmorphism, modern typography, and smooth micro-animations) where users can click a button to "Run AI Discovery Engine".
- **Visualization:** Display the extracted friction themes, keyword frequencies, and verbatim quotes dynamically using modern charting libraries (e.g., Chart.js).

### Sub-Phase 2.5: True RAG Integration (Groq API)
- **Backend Infrastructure:** Upgrade the static dashboard by building a Python Flask API (`app.py`) to handle frontend requests.
- **Retrieval Engine:** Implement a lightweight local search algorithm (TF-IDF/Keyword) in Python to retrieve the top 5-10 most relevant reviews from `raw_data.csv` based on the user's query.
- **LLM Generation:** Integrate the `groq` Python SDK. Feed the retrieved reviews as system context into a Groq model (e.g., `llama3-8b-8192`) to generate highly accurate, dynamic answers.
- **Frontend Refactor:** Update `script.js` to send asynchronous HTTP requests to the local Flask backend rather than using the simulated JS database.

**Deliverable:** A fully functional Full-Stack Web Dashboard running on `localhost:5000` featuring a true LLM-powered RAG Chatbot.


---

## Phase 3: Metric Decomposition & Target Selection
**Goal:** Connect qualitative insights back to business metrics and choose a focus area.
**Corresponds to:** `architecture.md` (Output Layer), `context.md` (Part 2)

### Sub-Phase 3.1: Metric Decomposition
- Break down `Wishlist → Purchase Conversion` into leading indicators (e.g., Wishlist to Cart %, Cart to Checkout %, Time spent on Wishlist).

### Sub-Phase 3.2: Insight Mapping
- Map the quantified themes from Sub-Phase 2.3 directly to the decomposed business metrics.

### Sub-Phase 3.3: Target Opportunity Selection
- Decide on the single highest-potential opportunity area (e.g., solving "Fit Uncertainty") ensuring it does *not* rely on monetary incentives.
- Document the rationale for this choice.

**Deliverable:** A documented breakdown of the business metric and the chosen focus area.

---

## Phase 4: Primary User Research & Problem Definition
**Goal:** Validate AI-generated insights with real humans and finalize the exact problem to solve.
**Corresponds to:** `context.md` (Part 3 & 4)

### Sub-Phase 4.1: Survey Preparation
- Identify the target user segment based on previous phases.
- Draft a multiple-choice survey template (optimized for Google Forms) with 6-7 questions focused on the selected opportunity area to rapidly validate insights.

### Sub-Phase 4.2: Conducting the Survey
- Distribute the Google Form to 30 users fitting the target segment to gather robust quantitative data at scale.
- Collect and export the structured survey responses.

### Sub-Phase 4.3: Synthesis & Problem Formulation
- Cross-reference human feedback with the AI Discovery Engine's findings.
- Draft the final Problem Definition, articulating the root cause, existing workarounds, user value, and business value.

**Deliverable:** A finalized Problem Definition document.

---

## Phase 5: MVP Ideation, Build & Deployment
**Goal:** Build a functional, deployable solution that addresses the defined problem.
**Corresponds to:** `context.md` (Part 5)

### Sub-Phase 5.1: Ideation & Architecture Design
- Brainstorm solutions based on the Problem Definition (e.g., an AI styling agent, a social-validation sharing feature, etc.).
- Outline the technical architecture for the chosen MVP.

### Sub-Phase 5.2: MVP Development (Core Sprint)
- Build the MVP frontend (e.g., React/Next.js UI or Streamlit).
- Connect the MVP to required backend logic or AI agent (Antigravity).

### Sub-Phase 5.3: MVP Deployment & E2E Testing
- Deploy the MVP to a publicly accessible platform (e.g., Vercel).
- Perform end-to-end testing to ensure the link works and handles user interaction gracefully.

**Deliverable:** A live, deployed link to the MVP.

---

## Phase 6: Final Deck Assembly & Deliverables
**Goal:** Package all findings and the MVP into a 10-slide deck adhering strictly to the `problemStatement.txt` guidelines.
**Corresponds to:** `context.md` (Part 6, Part 7)

### Sub-Phase 6.1: Metric & Risk Definition (Pre-work)
- Define North Star, Leading, and Guardrail metrics with clear rationales.
- Outline Risks & Mitigation steps.

### Sub-Phase 6.2: Slide Content Drafting
- Draft the precise content for the 10 slides (incorporating NextLeap best practices: Slide Titles = Key Messages, Font 14pt):
  1. **Executive Summary** (No names anywhere)
  2. **Business Metric Decomposition** (Wishlist → Purchase funnel)
  3. **AI Discovery Engine Architecture** (1-slider on how it works)
  4. **Discovery Engine Findings** (Top friction themes)
  5. **Primary User Research** (Survey Data on "Hesitant Wishlister")
  6. **Problem Definition** (Root cause, workarounds, user/biz value)
  7. **Solution Rationale** (Why AJIO Fit-Match AI?)
  8. **MVP Walkthrough** (Screenshots + Deployed Link)
  9. **Success Metrics** (North Star, Leading, Guardrails)
  10. **Risks & Mitigation Plan**

### Sub-Phase 6.3: Final Review & Assembly
- Apply formatting: STRICTLY 14pt font, color-blind friendly contrast.
- Ensure Slide Titles state the key message of the slide.
- Assemble and hyperlink all artifacts.
- Export as PDF.

### Sub-Phase 6.4: Unified Vercel Deployment (Free Tier)
- **Consolidated Hosting:** Deploy both the AI Discovery Engine prototype and the final MVP on a single Vercel project to stay within the free tier limits and maintain a single continuously updated link.
- **Serverless Configuration:** Utilize a `vercel.json` configuration file to define the `@vercel/python` runtime. Route `/api/(.*)` requests to the Flask backend while serving the frontends statically.
- **Secrets Management:** Securely add the `GROQ_API_KEY` to Vercel's Environment Variables dashboard.
- **Dependency Management:** Generate a unified `requirements.txt` file encompassing all required packages for both the engine and MVP.
- **Continuous Deployment (CD):** Connect the GitHub repository directly to Vercel to allow automatic deployments and preview branches on every push.

**Deliverable:** The final 10-slide PDF and a single live URL hosting all project deliverables.
