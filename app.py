"""InterviewCoach AI - practice interview questions for a job role.
The AI asks questions one by one, scores each answer out of 10 and gives tips.
Streamlit UI + Gemini Flash."""

import json
import re

import streamlit as st
from google import genai
from google.genai import types

DEFAULT_MODEL = "gemini-3.8-flash"
LEVELS = ["Fresher", "Mid-level", "Senior"]


# ---------- helpers (pure functions, easy to test) ----------
def clean_json(raw: str):
    """Parse JSON even if the model wrapped it in ```json fences."""
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw)
    return json.loads(raw)


def questions_prompt(role: str, level: str, n: int) -> str:
    return f"""Write {n} interview questions for a {level} {role} job.
Mix technical and behavioral questions. Keep each question short and clear.
Return ONLY a JSON list of {n} strings."""


def evaluate_prompt(role: str, level: str, question: str, answer: str) -> str:
    return f"""You are a strict but kind interviewer for a {level} {role} job.
Question: {question}
Candidate answer: {answer}

Return ONLY JSON with exactly these keys:
"score" (integer 0-10), "good" (string, what was good),
"missing" (string, what was missing or wrong), "sample" (string, a better sample answer)."""


def summary_prompt(role: str, level: str, results: list) -> str:
    lines = "\n".join(f"- Q: {r['question']} | Score: {r['score']}/10" for r in results)
    return f"""A candidate practiced interview questions for a {level} {role} job.
Results:
{lines}

In Markdown, write: "## Overall Feedback" (3-4 sentences) and "## Top 5 Tips to Improve" (numbered list)."""


def validate_questions(data, n: int) -> list:
    if not isinstance(data, list):
        return []
    return [q.strip() for q in data if isinstance(q, str) and q.strip()][:n]


def validate_eval(data):
    """Return a clean evaluation dict, or None if the model reply is unusable."""
    try:
        score = int(data["score"])
        return {
            "score": max(0, min(10, score)),
            "good": str(data.get("good", "")),
            "missing": str(data.get("missing", "")),
            "sample": str(data.get("sample", "")),
        }
    except (KeyError, TypeError, ValueError):
        return None


def ask_gemini(client, model: str, prompt: str, as_json: bool = False) -> str:
    config = types.GenerateContentConfig(
        response_mime_type="application/json" if as_json else "text/plain",
        temperature=0.5,
    )
    response = client.models.generate_content(model=model, contents=prompt, config=config)
    return response.text or ""


# ---------- UI ----------
def main():
    st.set_page_config(page_title="InterviewCoach AI", page_icon="🎤", layout="centered")
    st.title("🎤 InterviewCoach AI")
    ss = st.session_state
    ss.setdefault("stage", "setup")

    with st.sidebar:
        st.header("Settings")
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            api_key = ""
        if not api_key:
            api_key = st.text_input("Gemini API key", type="password")
        model = st.text_input("Model name", value=DEFAULT_MODEL)

    # ----- Stage 1: setup -----
    if ss["stage"] == "setup":
        st.caption("Practice real interview questions and get instant feedback.")
        role = st.text_input("Job role", placeholder="e.g. Python Developer, Data Analyst")
        level = st.selectbox("Experience level", LEVELS)
        n = st.slider("Number of questions", 3, 10, 5)

        if st.button("Start interview", type="primary"):
            if not api_key:
                st.error("Please enter your Gemini API key in the sidebar.")
                st.stop()
            if not role.strip():
                st.error("Please enter a job role.")
                st.stop()
            try:
                client = genai.Client(api_key=api_key)
                with st.spinner("Preparing your questions..."):
                    raw = ask_gemini(client, model, questions_prompt(role.strip(), level, n), as_json=True)
                    questions = validate_questions(clean_json(raw), n)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.stop()
            if not questions:
                st.error("Could not create questions. Please try again.")
                st.stop()
            ss.update(role=role.strip(), level=level, questions=questions,
                      idx=0, results=[], current_eval=None, stage="quiz")
            st.rerun()

    # ----- Stage 2: answering questions -----
    elif ss["stage"] == "quiz":
        total = len(ss["questions"])
        idx = ss["idx"]
        question = ss["questions"][idx]
        st.progress(idx / total)
        st.subheader(f"Question {idx + 1} of {total}")
        st.write(question)

        ev = ss.get("current_eval")
        answer = st.text_area("Your answer", key=f"ans{idx}", height=160, disabled=ev is not None)

        if ev is None:
            if st.button("Submit answer", type="primary"):
                if not answer.strip():
                    st.error("Please type your answer first.")
                    st.stop()
                try:
                    client = genai.Client(api_key=api_key)
                    with st.spinner("Checking your answer..."):
                        raw = ask_gemini(client, model,
                                         evaluate_prompt(ss["role"], ss["level"], question, answer), as_json=True)
                        result = validate_eval(clean_json(raw))
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
                    st.stop()
                if result is None:
                    st.error("Could not read the feedback. Please click Submit again.")
                    st.stop()
                ss["current_eval"] = result
                ss["current_answer"] = answer
                st.rerun()
        else:
            st.metric("Score", f"{ev['score']} / 10")
            st.success(f"**What was good:** {ev['good']}")
            st.warning(f"**What was missing:** {ev['missing']}")
            st.info(f"**Better sample answer:** {ev['sample']}")
            label = "Next question" if idx + 1 < total else "Finish interview"
            if st.button(label, type="primary"):
                ss["results"].append({"question": question, "answer": ss["current_answer"], **ev})
                ss["current_eval"] = None
                ss["idx"] = idx + 1
                if ss["idx"] >= total:
                    ss["stage"] = "done"
                st.rerun()

    # ----- Stage 3: final result -----
    else:
        results = ss["results"]
        total_score = sum(r["score"] for r in results)
        if "shown" not in ss:
            ss["shown"] = True
            if total_score >= len(results) * 7:
                st.balloons()
        st.header(f"Your score: {total_score} / {len(results) * 10}")

        if "summary" not in ss:
            try:
                client = genai.Client(api_key=api_key)
                with st.spinner("Writing your feedback..."):
                    ss["summary"] = ask_gemini(client, model, summary_prompt(ss["role"], ss["level"], results))
            except Exception as e:
                ss["summary"] = f"Could not create feedback: {e}"
        st.markdown(ss["summary"])

        for i, r in enumerate(results, 1):
            with st.expander(f"Q{i}: {r['question']}  -  {r['score']}/10"):
                st.write(f"**Your answer:** {r['answer']}")
                st.write(f"**Missing:** {r['missing']}")
                st.write(f"**Sample answer:** {r['sample']}")

        if st.button("Start a new interview"):
            for k in list(ss.keys()):
                del ss[k]
            st.rerun()


if __name__ == "__main__":
    main()
