import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="Nyaya AI", page_icon="⚖️", layout="wide")

SOURCES = [
    {
        "name": "Consumer Protection Act, 2019 (India Code)",
        "url": "https://www.indiacode.nic.in/bitstream/123456789/15256/5/A2019-35.pdf",
        "facts": "The Consumer Protection Act, 2019 is India's central consumer protection law. Do not infer a specific entitlement from this summary; check the Act and applicable rules."
    },
    {
        "name": "National Consumer Helpline",
        "url": "https://consumerhelpline.gov.in/",
        "facts": "The Department of Consumer Affairs' National Consumer Helpline is a pre-litigation grievance-redressal channel. Consumers can register grievances through the portal or call 1915. The official contact page lists 1915 and 1800-11-4000 (8 AM–8 PM, except national holidays)."
    },
    {
        "name": "e-Jagriti",
        "url": "https://e-jagriti.gov.in/",
        "facts": "The Government of India's e-Jagriti platform supports consumer commission case filing and case-status access. Filing a case is a formal legal step; eligibility, jurisdiction, documents and fees must be checked for the user's circumstances."
    },
    {
        "name": "NCH Consumer Protection Act FAQ",
        "url": "https://consumerhelpline.gov.in/public/knowledgebasedetails/Consumer%20Protection%20Act%202019",
        "facts": "The National Consumer Helpline FAQ describes consumer rights and possible reliefs that consumer commissions may grant, including refund, replacement, removal of defects and compensation, depending on the case."
    }
]

SOURCE_TEXT = "\n".join(
    f"- {s['name']}: {s['facts']} Source: {s['url']}" for s in SOURCES
)

SYSTEM_PROMPT = """You are Nyaya AI, an informational assistant for everyday consumer disputes in India.
You are NOT a lawyer and do not create an attorney-client relationship.
Your job is to help users organise facts, understand general options, and prepare a draft they can review.

STRICT SAFETY AND ACCURACY RULES:
1. Use only the supplied verified knowledge base for legal claims. Do not invent statutes, sections, rules, case names, court judgments, deadlines, fees, or guaranteed outcomes.
2. If the knowledge base does not establish an answer, say so clearly and suggest checking an official source or consulting a qualified Indian lawyer.
3. Do not state that the user will definitely win or is definitely entitled to compensation/refund. Explain that outcomes depend on facts, evidence, terms, and applicable law.
4. Separate (A) facts supplied by the user, (B) general information supported by sources, and (C) practical suggestions.
5. Do not treat the National Consumer Helpline as a court or guarantee that it will resolve the dispute.
6. Do not claim to file a complaint, contact a company, or provide legal representation.
7. Do not ask for Aadhaar, passwords, full card/bank numbers, OTPs, or other unnecessary sensitive information. Tell users to redact such data from evidence.
8. If the user describes threats, violence, criminal conduct, urgent limitation concerns, a large financial loss, or a complex dispute, recommend prompt advice from a qualified lawyer or appropriate authority.
9. If key facts are missing, list the missing facts and qualify the guidance rather than making assumptions.
10. Respond in the user's selected language where possible, using plain language.

VERIFIED KNOWLEDGE BASE:
""" + SOURCE_TEXT + """

OUTPUT FORMAT:
## 1. Your case, summarised
## 2. Important facts and missing information
## 3. What the available information says
## 4. Suggested next steps
## 5. Draft message / complaint
## 6. Sources and limitations

For the draft, use placeholders for unknown facts. Make clear it is a draft for the user to review, not a filed legal notice or a lawyer-approved document.
Cite source names and their URLs inline. Do not cite a source for a proposition it does not support.
"""

st.title("⚖️ Nyaya AI")
st.caption("An everyday consumer-dispute assistant | India | Prototype")
st.info("Nyaya AI provides general legal information and drafting support, not legal representation. Verify important steps with official sources or a qualified lawyer.")

with st.sidebar:
    st.header("Settings")
    language = st.selectbox("Response language", ["English", "Hindi", "Malayalam", "Tamil", "Telugu"])
    issue = st.selectbox(
        "Type of consumer problem",
        ["Refund not received", "Damaged / defective product", "Wrong product delivered", "Service not provided", "Other consumer issue"]
    )
    st.markdown("---")
    st.markdown("**Official resources**")
    for source in SOURCES:
        st.markdown(f"- [{source['name']}]({source['url']})")

st.subheader("Tell us what happened")
st.write("Describe the issue in your own words. Avoid sharing passwords, OTPs, Aadhaar numbers or full payment-card details.")

with st.form("case_form"):
    story = st.text_area(
        "Describe your problem",
        height=180,
        placeholder="Example: I ordered a laptop for ₹55,000 on 2 October. It arrived damaged on 5 October. I requested a return on 6 October and the product was collected on 9 October. I have not received the refund. The seller has not replied to my last two emails."
    )
    col1, col2 = st.columns(2)
    with col1:
        amount = st.text_input("Amount involved (optional)", placeholder="e.g. ₹55,000")
        purchase_date = st.text_input("Purchase date (optional)", placeholder="e.g. 2 October 2026")
    with col2:
        company = st.text_input("Company / seller (optional)")
        state = st.text_input("Your state (optional)")
    evidence = st.multiselect(
        "What evidence do you have?",
        ["Invoice / bill", "Order confirmation", "Payment proof", "Photos / videos", "Emails / chat messages", "Return / pickup confirmation", "Warranty / terms", "None yet"]
    )
    submitted = st.form_submit_button("Analyse my case", type="primary", use_container_width=True)


# ==========================================
# AI CASE ANALYSIS
# ==========================================

if submitted:

    # 1. Validate user input
    if not story.strip():
        st.error("Please describe your legal problem.")
        st.stop()

    # 2. Get Groq API key
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            api_key = None

    if not api_key:
        st.error("Groq API key not found. Please configure GROQ_API_KEY.")
        st.stop()

    # 3. Prepare user information
    user_context = f"""
    Selected issue: {issue}
    Language: {language}
    Amount: {amount or 'Not provided'}
    Purchase date: {purchase_date or 'Not provided'}
    Company: {company or 'Not provided'}
    State: {state or 'Not provided'}
    Evidence: {', '.join(evidence) if evidence else 'Not specified'}

    User's description:
    {story}
    """

    # 4. Connect to Groq and generate analysis
    try:
        with st.spinner("Nyaya AI is analysing your case..."):

            client = Groq(api_key=api_key)

            model = "openai/gpt-oss-120b"

            completion = client.chat.completions.create(
                model=model,
                temperature=0.1,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_context
                    }
                ]
            )

            answer = completion.choices[0].message.content

            if not answer:
                raise ValueError("The AI returned an empty response.")

            # Save the generated answer
            st.session_state["last_answer"] = answer

        st.success("Your case analysis is ready!")

    except Exception as e:
        st.error("AI analysis failed. Please check the error below.")
        st.exception(e)


# ==========================================
# DISPLAY AI RESPONSE
# ==========================================

if "last_answer" in st.session_state:

    st.divider()
    st.subheader("Your Case Analysis")

    st.markdown(st.session_state["last_answer"])

    st.download_button(
        label="Download analysis",
        data=st.session_state["last_answer"],
        file_name="nyaya_ai_case_analysis.md",
        mime="text/markdown"
    )


st.divider()
st.caption("Prototype limitation: this version focuses on consumer disputes. It does not submit complaints, verify uploaded documents, or replace advice from a qualified lawyer.")
