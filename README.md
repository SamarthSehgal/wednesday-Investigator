# 🕵️‍♀️ Project: WEDNESDAY - Multimodal AI Evidence Analyzer

**Final Submission for the Google Cloud Build and Blog Marathon**

**Live Demo URL:** https://wednesday-final-v2-61655539898.us-central1.run.app/

**Repo Link:** https://github.com/SamarthSehgal/wednesday-Investigator

**Blog Link :** https://medium.com/@samarthsehgal2006/how-to-build-wednesday-a-cynical-anti-hallucination-ai-agent-on-google-cloud-run-1ae893e34f74

---

## 💡 Overview: The Anti-Hallucination Agent

Wednesday is a specialized AI agent designed for **real-time evidence analysis** and **fact verification**. The application functions as a **Multimodal Evidence Analyzer**, capable of accepting complex inputs via voice command and image uploads (charts, documents, and visual data). It was built to solve the critical problem of AI hallucination by ensuring all responses are rigorously checked against **live web data** using the **Google Search Grounding** tool. The application features a unique, cynical persona deployed on Google Cloud's  **Serverless** architecture, every interaction is logged to **Google Firestore**, providing a verifiable **immutable audit trail**—a crucial feature for any real-world compliance or enterprise application.

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

**Diagram Final.png**

https://github.com/SamarthSehgal/wednesday-Investigator/blob/541d028ea8903268aef634c5fb006eb50ca07f78/Diagram%20Final.png

---

## 💻 Setup & Deployment

### Prerequisites

* Google Cloud Account (with billing enabled)
* Python 3.9+
* Google Cloud CLI
* A Gemini API Key (stored as `GOOGLE_API_KEY` in Cloud Run)

### Deployment Steps 

Clone Source Code from GitHub This pulls all files (app.py, Dockerfile, etc.) onto the local machine or Cloud Shell.

```bash
# 1. Clone the repository using the HTTPS URL
git clone https://github.com/SamarthSehgal/wednesday-Investigator.git

# 2. Navigate to the project directory
cd wednesday-Investigator
```

### After Cloning

The application adheres to security best practices by reading secrets only from the runtime environment.

1.  **Configure Dependencies:** The deployment relies on the exact versions specified in `requirements.txt` to maintain stability.
2.  **Authentication:** The application reads secrets securely from the Cloud Run environment variable `GOOGLE_API_KEY`.
3.  **Secure Secret Storage:** The `GOOGLE_API_KEY` is securely stored as an Environment Variable in the Cloud Run service configuration (not in the code).
4.  **Google Cloud Project ID** The `GOOGLE_CLOUD_PROJECT` ID also needs to be stored as an Environment Variable in the Cloud Run service configuration. 
5.  **Run Deployment (using the built-in `Dockerfile`):**
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


