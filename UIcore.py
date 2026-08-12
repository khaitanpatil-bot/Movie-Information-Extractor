import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

load_dotenv()

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Information Extractor",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #0b0f19;
        color: #f5f7fa;
    }

    /* Remove default top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Main title */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 8px;
        letter-spacing: -1px;
    }

    .main-title span {
        color: #7c3aed;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 17px;
        margin-bottom: 40px;
    }

    /* Section heading */
    .section-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 12px;
        color: #f3f4f6;
    }

    /* Input container */
    .input-box {
        background: #111827;
        border: 1px solid #293244;
        border-radius: 16px;
        padding: 20px;
    }

    /* Result container */
    .result-box {
        background: #111827;
        border: 1px solid #293244;
        border-radius: 16px;
        padding: 25px;
        margin-top: 25px;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        height: 52px;
        border-radius: 12px;
        border: none;
        background: #7c3aed;
        color: white;
        font-size: 16px;
        font-weight: 700;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        background: #6d28d9;
        border: none;
        transform: translateY(-1px);
    }

    /* Text area */
    textarea {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
    }

    textarea:focus {
        border: 1px solid #7c3aed !important;
        box-shadow: 0 0 0 1px #7c3aed !important;
    }

    /* Markdown result */
    .result-box h1,
    .result-box h2,
    .result-box h3 {
        color: #ffffff;
    }

    .result-box p,
    .result-box li {
        color: #d1d5db;
        line-height: 1.7;
    }

    /* Divider */
    .divider {
        height: 1px;
        background: #293244;
        margin: 35px 0;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 13px;
        margin-top: 45px;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🔎 Information <span>Extractor</span></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Extract useful factual information from any text using AI'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# YOUR EXISTING MODEL
# ---------------------------------------------------------

model = ChatMistralAI(model="mistral-small-2603")


# ---------------------------------------------------------
# YOUR EXISTING PROMPT
# ---------------------------------------------------------

prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an intelligent Information Extraction and Summarization AI.

Your task is to analyze the text provided by the user and extract the most useful factual information.

First, identify what type of content the text describes, such as:

- Movie / TV Show
- Person
- Product
- Company
- Event
- News
- Book
- Technology
- Place
- Organization
- Other

Then extract the information that is relevant to that type of content.

IMPORTANT RULES:

- Extract information ONLY from the provided text.
- Never invent, guess, or hallucinate information.
- If a requested detail is not mentioned, write "Not mentioned".
- Preserve exact names, dates, monetary values, percentages, locations, and important numbers.
- Remove unnecessary repetition.
- Keep the extracted information concise and easy to understand.
- Do NOT use JSON.
- Use clear headings and bullet points.
- Do not add outside knowledge.

EXTRACTED INFORMATION:

Basic Information

- Name / Title:
- Type / Category:
- Genre / Industry:
- Date / Release Date:
- Location:
- Status:

People / Organizations

- Main People:
- Creator / Director / Author:
- Companies / Organizations:
- Other Important People:

Main Information

- Purpose / Premise:
- Description:
- Key Features:
- Main Events / Plot:
- Problems / Conflicts:
- Important Relationships:

Financial Information

- Cost / Budget:
- Price:
- Revenue / Earnings:
- Financial Milestones:

Performance / Achievements

- Ratings:
- Awards:
- Records:
- Achievements:
- Important Statistics:

Other Important Facts

- Key Facts:
- Additional Information:

QUICK SUMMARY:
Write a clear 2–4 sentence summary of the entire text.

KEY TAKEAWAYS:
Provide 3–5 of the most important facts from the text.
"""
    ),

    ("human",
     """Analyze the following text and extract the useful information according to your instructions.

TEXT:
{text}
""")
])


# ---------------------------------------------------------
# INPUT AREA
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">📝 Enter your text</div>',
    unsafe_allow_html=True
)

para = st.text_area(
    label="Text",
    placeholder="Paste the text you want to analyze here...",
    height=300,
    label_visibility="collapsed"
)


# ---------------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------------

st.write("")

analyze = st.button("🔍 Analyze Information")


# ---------------------------------------------------------
# PROCESSING
# ---------------------------------------------------------

if analyze:

    if not para.strip():

        st.warning("Please enter some text before analyzing.")

    else:

        with st.spinner("Analyzing your text..."):

            try:

                final_prompt = prompt.invoke(
                    {"text": para}
                )

                response = model.invoke(final_prompt)

                result = response.content

                st.markdown(
                    '<div class="divider"></div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="section-title">✨ Extracted Information</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="result-box">',
                    unsafe_allow_html=True
                )

                st.markdown(result)

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            except Exception as e:

                st.error(f"Something went wrong: {e}")


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    '<div class="footer">'
    'Powered by LangChain + Mistral AI'
    '</div>',
    unsafe_allow_html=True
)