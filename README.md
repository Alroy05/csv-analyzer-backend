# 📡 RAG CSV Analyzer Backend

This is the FastAPI backend for **RAG CSV Analyzer**, a web-based tool that enables users to upload, analyze, and query CSV files using AI-powered search capabilities. The backend is responsible for handling file uploads, storing CSV data in MongoDB, and processing user queries using Google Gemini AI.

## 🌐 Deployed URL
`https://csv-analyzer-alroy.streamlit.app/`

## 🖼️ Project Screenshots

![Screenshot 1](/assets/ss1.png)
![Screenshot 2](/assets/ss2.png)

## 🚀 Installation Steps

### Backend Setup (FastAPI)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Alroy05/csv-analyzer-backend.git
   cd csv-analyzer-backend
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   - Create a `.env` file in the project root and add the following:
   ```env
   MONGO_URI=your_mongodb_connection_uri
   GOOGLE_API_KEY=your_google_gemini_api_key
   ```

5. **Run the FastAPI Server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 🔗 Frontend Repository
The frontend for this project is available at:
[CSV Analyzer Frontend](https://github.com/Alroy05/csv-analyzer-frontend)

---

Made with ❤️ by Alroy

