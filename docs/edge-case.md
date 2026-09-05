# AI-Powered Discovery Engine: Edge Cases & Corner Scenarios

This document outlines potential edge cases, risks, and corner scenarios across the entire lifecycle of the **Wishlist to Purchase Conversion** project, based on the definitions in `architecture.md` and `implementation-plan.md`. For each scenario, a mitigation strategy is provided.

---

## 1. Data Ingestion Layer

### Scenario 1.1: Scraper Blocking & Rate Limits
- **Edge Case:** Scripts utilizing `google-play-scraper`, `app-store-scraper`, or `praw` face rate limiting, IP blocks, or CAPTCHA challenges during batch ingestion.
- **Mitigation:** Implement randomized delays (`time.sleep()`) between requests. If issues persist, reduce the batch size or use a rotating proxy. For Reddit, strictly adhere to the API guidelines and user-agent requirements.

### Scenario 1.2: API Structure Changes
- **Edge Case:** Underlying HTML or API endpoints for app stores/social media change unexpectedly, causing the scrapers to return `None` or throw exceptions.
- **Mitigation:** Wrap scraping functions in `try-except` blocks. Log failures to a secondary `failed_ingestion.log` file rather than crashing the entire pipeline. Fall back to manual CSV exports if automated scraping completely fails.

### Scenario 1.3: Low Data Relevance / High Noise
- **Edge Case:** Keyword searches (e.g., "cart", "wait", "save") pull highly irrelevant data (e.g., users talking about saving a game, not a fashion item).
- **Mitigation:** Refine keyword combinations to be platform-specific (e.g., "AJIO wishlist"). Add a preliminary filter script to drop rows that don't contain secondary fashion-related keywords (e.g., clothes, size, fit, fabric).

### Scenario 1.4: Insufficient Data Volume
- **Edge Case:** The scraping process yields too few reviews discussing the specific Wishlist to Purchase friction.
- **Mitigation:** Broaden the search scope to include general fashion forums or competitors (e.g., Amazon Fashion, Flipkart) to gather a wider, statistically significant corpus of user psychology.

---

## 2. Processing & Analytics Layer (Antigravity AI)

### Scenario 2.1: LLM Context Window Overflow
- **Edge Case:** The chunking script feeds too much data into a single prompt, exceeding the LLM's token limit and resulting in a truncation error.
- **Mitigation:** Use a strict token-counting library (e.g., `tiktoken`) during the preprocessing phase to ensure chunks remain well below the maximum limit. Summarize chunks hierarchically if needed.

### Scenario 2.2: Unstructured/Malformed LLM Output
- **Edge Case:** The AI fails to return the requested JSON format (e.g., adding conversational text outside the JSON block), causing the quantification script to fail.
- **Mitigation:** Use strong system prompt constraints (e.g., "Return ONLY valid JSON"). Implement a regex-based parser to extract the JSON block from the response, and validate it using a JSON schema parser before proceeding.

### Scenario 2.3: Hallucinations & Miscategorization
- **Edge Case:** The LLM hallucinates themes that do not exist in the raw data or incorrectly categorizes a positive review as a friction point.
- **Mitigation:** Force the LLM to include direct, verbatim quotes from the raw text to justify its categorization.

### Scenario 2.4: Data Privacy Leakage (PII)
- **Edge Case:** Usernames, emails, or personal identifiers are accidentally passed into the LLM context.
- **Mitigation:** Run a regex-based anonymization script on the `raw_data.csv` to strip handles (e.g., `@username`) and standard PII patterns before it reaches the AI processing layer.

---

## 3. Metric Decomposition & Opportunity Selection

### Scenario 3.1: Only Monetary Friction Identified
- **Edge Case:** The AI analysis overwhelmingly concludes that "Waiting for a sale/discount" is the *only* reason users keep items in their wishlist, violating the project constraint (no monetary incentives).
- **Mitigation:** Filter out pure price-related feedback early in the processing phase. Force the analysis to focus on the secondary tier of friction (e.g., fit uncertainty, decision paralysis, styling doubts).

---

## 4. Primary User Research

### Scenario 4.1: Research Contradicts AI Insights
- **Edge Case:** During user interviews, the 5-6 participants state that the AI-identified friction point (e.g., "Sizing Uncertainty") is actually not a big deal for them.
- **Mitigation:** Treat the AI insights as hypotheses, not absolute truths. If invalidated, pivot back to the second highest-ranked friction point from the AI Discovery Engine and validate that instead.

---

## 5. MVP Ideation & Deployment

### Scenario 5.1: MVP Scope Creep
- **Edge Case:** The envisioned solution (e.g., an AI styling agent) becomes too technically complex to build within the short sprint timeframe.
- **Mitigation:** Strictly adhere to the MVP definition. Build a Wizard of Oz prototype or a simplified Streamlit app that fakes the heavy backend processing, just to prove the user flow and value proposition.

### Scenario 5.2: Deployment Failures
- **Edge Case:** The MVP frontend fails to deploy on Vercel/Streamlit due to dependency conflicts or environment variable misconfigurations.
- **Mitigation:** Use standard, well-tested boilerplate templates for deployment. Maintain a local fallback (e.g., running `npm run dev` and recording a video) to embed in the final presentation if cloud deployment critically fails.
