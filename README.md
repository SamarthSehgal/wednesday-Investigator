# 🕵️‍♀️ Project: WEDNESDAY — Multimodal AI Evidence Analyzer

**Final Submission for the Google Cloud Build and Blog Marathon**

**Live Demo URL:** [INSERT YOUR CLOUD RUN URL HERE]
**Repo Link:** https://github.com/SamarthSehgal/wednesday-Investigator

---

## 💡 Overview: The Anti-Hallucination Agent

Wednesday is a specialized AI agent designed for **real-time evidence analysis** and **fact verification**. It was built to solve the critical problem of AI hallucination by enforcing strict grounding protocols. The application features a unique, cynical persona and a multimodal interface (Voice and Vision) deployed on Google Cloud's serverless infrastructure.

### 🚀 Key Technical Decisions
| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Compute / Host** | **Google Cloud Run** | Serverless, scalable to zero, ensuring cost efficiency. |
| **Intelligence** | **Gemini 2.5 Flash** | Chosen for fast inference speed (low-latency voice interaction) and native multimodal capabilities. |
| **Grounding** | **Direct REST API / Google Search** | **CRITICAL: Bypassed the SDK** to send raw JSON payload, ensuring the `Google Search` tool works without library version conflicts. |
| **Memory / Audit** | **Google Firestore** | Used for immutable, persistent logging of all case files and transactions. |

---

## 🏛️ Architecture

The solution uses a **Serverless Microservices Architecture** with a **Direct REST API Integration Pattern**. This design ensures robustness and immediate feature access.

**[INSERT YOUR ARCHITECTURE DIAGRAM PNG HERE]**
*(Note: Upload your `Diagram Final.png` to your GitHub repo and link it here.)*

---

## 💻 Setup & Deployment

### Prerequisites

* Google Cloud Account (with billing enabled)
* Python 3.9+
* Google Cloud CLI
* A Gemini API Key (stored as `GOOGLE_API_KEY` in Cloud Run)

### Deployment Steps (After Cloning)

1.  **Configure Dependencies:** The deployment relies on the exact versions specified in `requirements.txt` to maintain stability.
2.  **Authentication:** The application reads secrets securely from the Cloud Run environment variable `GOOGLE_API_KEY`.
3.  **Run Deployment (using the built-in `Dockerfile`):**
    ```bash
    gcloud run deploy wednesday-final \
      --source . \
      --region us-central1 \
      --allow-unauthenticated
    ```

---

### 🗂️ How to Run Locally (Optional)

1.  Set the API Key: `export GOOGLE_API_KEY="[YOUR_KEY]"`
2.  Install dependencies: `pip install -r requirements.txt`
3.  Run Streamlit: `streamlit run app.py`

*(End of File)*

### 📝 Final Action
1.  Create the `README.md` file in your `wednesday-deploy` folder.
2.  Run the following Git commands in your terminal to stage the new file and push the final documentation:

```bash
git add README.md
git commit -m "feat: Add final README.md for submission"
git push origin main
