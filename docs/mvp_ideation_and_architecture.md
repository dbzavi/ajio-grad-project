# MVP Ideation & Architecture Design (Sub-Phase 5.1)

## 1. Problem Definition Recap
Based on our discovery phase and metric decomposition, the primary blocker for users converting from the Wishlist to Purchase is **Sizing Paranoia (The Visual & Data Trust Gap)**. Users hesitate to buy because they aren't sure how an item will fit their specific body type, and price discounts (monetary incentives) are restricted as a solution.

## 2. Ideation (Brainstorming Solutions)

### Idea 1: AJIO Fit-Match AI + Virtual Try-On (Chosen MVP)
- **Concept:** A dual-engine approach. First, an AI RAG engine synthesizes thousands of sizing reviews (e.g., "runs small", "tight on shoulders") into a personalized recommendation. Second, a Virtual Try-On (VTO) feature visually maps the garment onto a digital mannequin representing the user's body type.
- **Pros:** Directly addresses both the data trust gap (sizing ambiguity) and visual trust gap (how it looks on me). Does not rely on discounts.
- **Cons:** High technical complexity for the VTO component.

### Idea 2: Wishlist "Ask a Friend" Social Voting
- **Concept:** A feature allowing users to share their wishlist directly to WhatsApp/Instagram with a built-in polling widget, letting friends vote on which size or item to buy.
- **Pros:** High virality and potential for new user acquisition.
- **Cons:** High friction. Relies on external parties to unblock the checkout process, which increases Time-to-Checkout rather than decreasing it.

### Idea 3: Intelligent Urgency Nudges (Stock/Scarcity)
- **Concept:** Push notifications indicating that an item in the wishlist is selling out fast in the user's previously purchased size.
- **Pros:** Easy to implement using existing data.
- **Cons:** Doesn't solve the core *sizing* issue for new brands/silhouettes. Only works if the user already knows their size.

## 3. Chosen Solution: AJIO Fit-Match AI + Virtual Try-On
We will proceed with Idea 1 as the core MVP because it is the most direct, high-leverage intervention to transition users from the "evaluation" phase to "checkout" without employing monetary discounts.

---

## 4. Technical Architecture for the MVP

The MVP will be a web-based prototype demonstrating the Fit-Match AI workflow. It will be designed for deployment on Vercel.

### A. Core Components

1. **Frontend UI (AJIO App Simulation)**
   - **Tech Stack:** Next.js (React) or plain HTML/JS depending on sprint constraints.
   - **Role:** Simulates the AJIO Product Details Page (PDP). It houses the "Fit-Match AI" widget and the Virtual Try-On modal interface.
   
2. **Backend API (Context Handler)**
   - **Tech Stack:** Python (Flask or FastAPI).
   - **Role:** Acts as the orchestration layer. It receives the user's profile (height, weight, body type) and routes requests to the AI Engine and VTO Service.

3. **AI Sizing Engine (RAG)**
   - **Tech Stack:** LangChain / Groq API (LLaMA-3 or similar).
   - **Role:** Retrieves relevant reviews from the Vector DB based on the user's body profile and the specific SKU, synthesizing a definitive size recommendation (e.g., "85% confidence you need a Medium").

4. **Vector Database**
   - **Tech Stack:** Pinecone, Qdrant, or a lightweight local vector store (FAISS).
   - **Role:** Stores embeddings of unstructured product reviews and sizing feedback for fast similarity search during the RAG process.

5. **Virtual Try-On (VTO) Service**
   - **Tech Stack:** Simulated Generative AI endpoint (or placeholder for MVP).
   - **Role:** Takes the garment image and the user's body archetype, generating a visual composite to eliminate visual sizing doubt.

### B. High-Level Diagram

```mermaid
flowchart TD
    User([👤 User]) --> |Inputs Height/Weight| Frontend[📱 Frontend UI (AJIO App)]
    Frontend --> |API Request| Backend[⚙️ Context Handler (Flask/FastAPI)]
    
    Backend --> |RAG Query| AIEngine[🧠 AI Engine (Groq/LangChain)]
    Backend --> |Image Request| VTO[📸 VTO Service]
    
    AIEngine <--> |Similarity Search| VectorDB[(Vector DB: Reviews & Fit Data)]
    VTO <--> |Fetch Silhouettes| VectorDB
    
    AIEngine --> |Size Recommendation| Backend
    VTO --> |Try-On Image| Backend
    
    Backend --> |JSON Response| Frontend
```

## 5. Next Steps (Sub-Phase 5.2)
With the architecture defined, the next phase is **Sub-Phase 5.2: MVP Development (Core Sprint)**. We will begin building the frontend UI and the Python backend to simulate this exact flow.
