# NyayaAI
a conversational AI that takes a person's problem by text or voice, in the language they're comfortable with, and helps them act on it.
# Nyaya AI — Kuku AI Generalist Assignment prototype

A small Streamlit prototype for helping Indian consumers organise a dispute, understand general routes for redressal, and draft a message/complaint for review.

## Scope
Initial focus: consumer disputes such as refunds not received, damaged/defective products, wrong products, and services not provided.

## Run locally
1. Install Python 3.10+.
2. Create and activate a virtual environment.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Set your Groq API key:
   - macOS/Linux: `export GROQ_API_KEY="your_key"`
   - Windows PowerShell: `$env:GROQ_API_KEY="your_key"`
5. Run:
   `streamlit run app.py`

Optional model override:
- Set `GROQ_MODEL` to a model currently available in your Groq account.

For Streamlit Community Cloud, add `GROQ_API_KEY` under App Settings → Secrets.

## What it does
- Collects the user's narrative and basic case details.
- Sends the case plus a small official-source knowledge base to an LLM.
- Requests a structured summary, missing facts, general options, next steps, and a draft.
- Lets the user download the raw answer as Markdown.

## What it does NOT do
- It does not file a complaint or contact a company.
- It does not verify evidence or independently retrieve current laws.
- It does not provide legal representation or guarantee an outcome.
- The legal knowledge base is deliberately narrow and should be reviewed/expanded before real-world deployment.

## Evaluation / quality checks
Run all test cases in `test_cases.md`. Check whether the app:
1. Avoids inventing sections, deadlines, judgments, fees, and guarantees.
2. Identifies missing facts.
3. Distinguishes NCH from e-Jagriti / Consumer Commissions.
4. Produces a usable draft with placeholders.
5. Advises professional help when the issue is urgent or complex.

## AI tools used
- Groq-hosted language model for generation.
- Streamlit for the user interface.
- Python for input handling and prompt orchestration.

## Known limitation
The model may still produce incorrect or incomplete legal explanations. The source list is intentionally small; important claims must be checked against the official sources and a qualified lawyer.
