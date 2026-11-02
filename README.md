# 🎯 AI Interview Coach

**Practice Smart. Answer Confidently. Get Hired.**

AI Interview Coach helps you prepare for job interviews. Enter your target role and experience level, and an AI interviewer asks you five questions one at a time. Each answer is scored and reviewed, and at the end you get a personalised performance report.

## Features

- Choose a job role and a level (Beginner, Intermediate, Advanced).
- Five questions, one per category: technical knowledge, communication, problem-solving, leadership, and situational judgment.
- You must answer each question before the next one appears.
- Every answer gets a score out of 10, strengths, weaknesses, improvement suggestions, and an example of a stronger answer.
- Live progress bar and running average score.
- Final report with category scores and personalised recommendations.
- Restart the same interview or start a new one at any time.

## Tech stack

| Part | Choice |
|---|---|
| Frontend | Streamlit |
| AI | Gemini Flash via the Google Gen AI SDK (`google-genai`) |
| Language | Python |
| Hosting | Streamlit Community Cloud |
| Version control | GitHub |

## Project structure

```
ai-interview-coach/
├── app.py             # the whole application
├── requirements.txt   # Python dependencies
└── README.md
```

## 1. Get a Gemini API key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey) and sign in with your Google account.
2. Click **Create API key** and choose (or create) a project.
3. Copy the key and keep it private. Never paste it into `app.py` or commit it to GitHub.

The free tier has usage limits. If you see a "rate limit" message in the app, wait a minute and try again.

## 2. Run locally

Requires Python 3.10 or newer.

```bash
# 1. Open a terminal in the project folder
cd ai-interview-coach

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

Add your API key using **one** of these options:

**Option A: Streamlit secrets file (recommended)**

Create the file `.streamlit/secrets.toml` in the project folder:

```toml
GEMINI_API_KEY = "your-api-key-here"
```

**Option B: environment variable**

```bash
export GEMINI_API_KEY="your-api-key-here"      # Windows PowerShell: $env:GEMINI_API_KEY="your-api-key-here"
```

Start the app:

```bash
streamlit run app.py
```

It opens at <http://localhost:8501>.

### Changing the model

The app uses `gemini-3.8-flash` by default. Google renames and retires models over time, so if you ever see a "model not found" message, set a different Flash model name without editing the code. Add this line to your secrets (or set it as an environment variable):

```toml
GEMINI_MODEL = "gemini-3.8-flash"
```

Check [the Gemini models page](https://ai.google.dev/gemini-api/docs/models) for current names.

## 3. Upload to GitHub

First, make sure your secrets are never uploaded. In the project folder, create a file named `.gitignore` containing:

```
.streamlit/secrets.toml
venv/
__pycache__/
```

**Option A: command line**

1. Create a new empty repository on [github.com/new](https://github.com/new) (for example `ai-interview-coach`). Do not add a README there, since you already have one.
2. In your project folder, run:

```bash
git init
git add app.py README.md requirements.txt .gitignore
git commit -m "Initial commit: AI Interview Coach"
git branch -M main
git remote add origin https://github.com/<your-username>/ai-interview-coach.git
git push -u origin main
```

**Option B: GitHub website (no Git needed)**

1. Create a new repository on GitHub.
2. Click **Add file → Upload files**, drag in `app.py`, `README.md`, and `requirements.txt`, and click **Commit changes**.

## 4. Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub. Allow access to your repository if asked.
2. Click **Create app** and choose to deploy from an existing GitHub repo.
3. Select your repository, the branch `main`, and set **Main file path** to `app.py`.
4. Click **Advanced settings**:
   - Pick Python 3.11 or newer.
   - In the **Secrets** box, paste:
     ```toml
     GEMINI_API_KEY = "your-api-key-here"
     ```
5. Click **Deploy**. The first build takes a couple of minutes, then you get a public `*.streamlit.app` link.

To update the app later, push new commits to GitHub and it redeploys automatically. To change the API key, open your app's **Settings → Secrets** in Streamlit Community Cloud.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Gemini API key not found" | Add `GEMINI_API_KEY` to `.streamlit/secrets.toml` (local) or the Secrets box (cloud). |
| "API key was rejected" | Re-copy the key from Google AI Studio and make sure it has no extra spaces or quotes. |
| "Model not found" | Set `GEMINI_MODEL` to a current Flash model name. |
| "Rate limit reached" | Wait a minute, or use a key with higher quota. |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` (cloud: check the file is in the repo root). |

## Privacy note

Your role and answers are sent to the Gemini API to generate questions and feedback. Do not enter confidential or personal information.

## Disclaimer

Scores and feedback are AI-generated practice guidance, not a prediction of real interview results.
