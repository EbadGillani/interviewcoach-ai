# 🎤 InterviewCoach AI

Practice interviews for any job role.

1. Enter a job role and your level (Fresher, Mid-level, Senior).
2. The AI asks interview questions one by one.
3. Type your answer and get a score out of 10, what was good, what was missing and a better sample answer.
4. At the end you get your total score and 5 tips to improve.

Built with **Streamlit** and **Google Gemini Flash**.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Paste your Gemini API key in the sidebar (free key: https://aistudio.google.com/apikey).

## Deploy on Streamlit Community Cloud
1. Push `app.py`, `README.md` and `requirements.txt` to a public GitHub repo.
2. Go to https://share.streamlit.io and create a new app (main file: `app.py`).
3. In **Advanced settings → Secrets** add:
   ```
   GEMINI_API_KEY = "your-key-here"
   ```

## Notes
- If you get a "model not found" error, change the model name in the sidebar to the current Gemini Flash model.
- Answers are only used to create feedback and are not stored.
-
