import streamlit as st

import os
import tempfile
import pdfplumber
import docx
import textract
from striprtf.striprtf import rtf_to_text
# --------------------------------------------------------
# Page Configuration
# --------------------------------------------------------
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------------
# Professional CSS
# --------------------------------------------------------

st.markdown("""
<style>

/* Main App */
.stApp{
background:linear-gradient(135deg,#eef5ff,#dbeafe,#ffffff);
}

/* Sidebar */
section[data-testid="stSidebar"]{
background:#0f172a;
color:white;
}

section[data-testid="stSidebar"] *{
color:white;
}

/* Title */

.main-title{
font-size:40px;
font-weight:bold;
color:#0f172a;
text-align:center;
padding:10px;
}

/* Cards */

.card{
background:white;
padding:20px;
border-radius:15px;
box-shadow:0px 4px 15px rgba(0,0,0,.15);
margin-bottom:20px;
}

/* Upload */

[data-testid="stFileUploader"]{
background:white;
padding:15px;
border-radius:12px;
}

/* Buttons */

.stButton>button{

width:100%;

background:#2563eb;

color:white;

border-radius:10px;

height:50px;

font-size:18px;

font-weight:bold;

border:none;

}

.stButton>button:hover{

background:#1d4ed8;

}

/* TextArea */

textarea{

border-radius:10px !important;

}

/* Select Box */

div[data-baseweb="select"]{

border-radius:10px;

}

/* Success */

.success{

background:#dcfce7;

padding:15px;

border-radius:10px;

color:green;

font-weight:bold;

}

</style>

""", unsafe_allow_html=True)

# --------------------------------------------------------
# Sidebar
# --------------------------------------------------------

st.sidebar.title("🤖 AI HR Assistant")

st.sidebar.markdown("---")

# API KEY

api_key = st.sidebar.text_input(
    "🔑 API Key",
    type="password",
    placeholder="Enter API Key"
)

# LLM Provider

provider = st.sidebar.selectbox(

"Choose LLM Provider",

[
"OpenAI",
"Google Gemini",
"Groq",
"Together AI",
"OpenRouter"
]

)

# Model Selection

if provider=="OpenAI":

    model=st.sidebar.selectbox(

    "Model",

    [

    "gpt-4.1",

    "gpt-4o",

    "gpt-4o-mini"

    ]

    )

elif provider=="Google Gemini":

    model=st.sidebar.selectbox(

    "Model",

    [

    "gemini-2.5-pro",

    "gemini-2.5-flash"

    ]

    )

elif provider=="Groq":

    model=st.sidebar.selectbox(

    "Model",

    [

    "llama-3.3-70b",

    "mixtral-8x7b"

    ]

    )

elif provider=="Together AI":

    model=st.sidebar.selectbox(

    "Model",

    [

    "Llama-3.1-70B",

    "Mixtral-8x22B"

    ]

    )

else:

    model=st.sidebar.selectbox(

    "Model",

    [

    "gpt-4o",

    "claude-3.7",

    "gemini-2.5"

    ]

    )

temperature = st.sidebar.slider(

"Temperature",

0.0,

1.0,

0.3

)

top_k = st.sidebar.slider(

"Top Candidates",

1,

20,

5

)

st.sidebar.markdown("---")

# --------------------------------------------------------
# Main Header
# --------------------------------------------------------

st.markdown(
"""
<div class='main-title'>
AI Resume Screening & Ranking System
</div>
""",
unsafe_allow_html=True
)

# --------------------------------------------------------
# Layout
# --------------------------------------------------------

left,right=st.columns([2,1])

# --------------------------------------------------------
# Job Description
# --------------------------------------------------------

with left:

    st.markdown("<div class='card'>",unsafe_allow_html=True)

    st.subheader("📄 Upload Job Description")

    jd_file=st.file_uploader(

    "Upload Job Description",

    type=["pdf","docx","txt"],

    key="jd"

    )

    st.markdown("### OR")

    job_description=st.text_area(

    "Paste Job Description",

    height=250,

    placeholder="""
Example

Python Developer

Skills

Python

Machine Learning

SQL

Pandas

NumPy

TensorFlow

Experience

3 Years

Education

B.Tech/MCA

"""

    )

    st.markdown("</div>",unsafe_allow_html=True)

# --------------------------------------------------------
# Resume Upload
# --------------------------------------------------------

with right:

    st.markdown("<div class='card'>",unsafe_allow_html=True)

    st.subheader("📂 Upload Resumes")

    resumes=st.file_uploader(

    "Upload Multiple Resumes",

    type=[

    "pdf",

    "docx",

    "doc",

    "txt",

    "rtf"

    ],

    accept_multiple_files=True

    )

    st.markdown("</div>",unsafe_allow_html=True)

# --------------------------------------------------------
# Uploaded File Summary
# --------------------------------------------------------

st.markdown("---")

if jd_file:

    st.success(f"✅ Job Description Uploaded : {jd_file.name}")

if resumes:

    st.success(f"✅ {len(resumes)} Resume(s) Uploaded")

    st.markdown("### Uploaded Files")

    for file in resumes:

        st.write("📄",file.name)

# --------------------------------------------------------
# Analyze Button
# --------------------------------------------------------

analyze = st.button("🚀 Analyze Resumes")

if analyze:

    if not api_key:

        st.error("Please Enter API Key")

    elif not resumes:

        st.error("Upload Resumes")

    elif not (jd_file or job_description):

        st.error("Upload or Paste Job Description")

    else:

        st.success("✅ Ready for Resume Parsing...")




# ==========================================================
# Resume Text Extraction Functions
# ==========================================================

def extract_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        st.error(f"PDF Error: {e}")
    return text


def extract_docx(file):
    text = ""
    try:
        document = docx.Document(file)
        for para in document.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        st.error(f"DOCX Error: {e}")
    return text


def extract_doc(file):
    text = ""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".doc") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        text = textract.process(tmp_path).decode("utf-8")

        os.remove(tmp_path)

    except Exception as e:
        st.error(f"DOC Error: {e}")

    return text


def extract_txt(file):
    try:
        return file.read().decode("utf-8")
    except:
        return ""


def extract_rtf(file):
    try:
        raw = file.read().decode("utf-8")
        return rtf_to_text(raw)
    except:
        return ""


def extract_resume(file):

    extension = file.name.split(".")[-1].lower()

    if extension == "pdf":
        return extract_pdf(file)

    elif extension == "docx":
        return extract_docx(file)

    elif extension == "doc":
        return extract_doc(file)

    elif extension == "txt":
        return extract_txt(file)

    elif extension == "rtf":
        return extract_rtf(file)

    return ""


# ==========================================================
# Parse Uploaded Resumes
# ==========================================================

parsed_resumes = []

if resumes:

    st.markdown("---")
    st.subheader("📑 Resume Preview")

    for file in resumes:

        with st.spinner(f"Reading {file.name}..."):

            resume_text = extract_resume(file)

            resume_data = {
                "filename": file.name,
                "text": resume_text,
                "characters": len(resume_text),
                "words": len(resume_text.split())
            }

            parsed_resumes.append(resume_data)

            with st.container():

                st.markdown(
                    f"""
                    <div class="card">
                    <h4>📄 {file.name}</h4>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Characters", len(resume_text))

                with col2:
                    st.metric("Words", len(resume_text.split()))

                with st.expander("Preview Resume Text"):

                    if resume_text.strip():

                        st.text_area(
                            "",
                            value=resume_text[:3000],
                            height=250,
                            disabled=True,
                            key=file.name
                        )

                    else:

                        st.warning("No readable text found.")

st.session_state["parsed_resumes"] = parsed_resumes





# ==========================================================
# Simple Resume Ranking
# ==========================================================

if analyze:

    parsed_resumes = st.session_state.get("parsed_resumes", [])

    if len(parsed_resumes) == 0:

        st.error("No resumes available.")

    else:

        # Read Job Description

        if job_description.strip():

            jd_text = job_description.lower()

        else:

            jd_text = ""

        candidate_scores = []

        # ------------------------------------------
        # Calculate Similarity Score
        # ------------------------------------------

        for resume in parsed_resumes:

            resume_text = resume["text"].lower()

            jd_words = set(jd_text.split())

            resume_words = set(resume_text.split())

            matched_words = jd_words.intersection(resume_words)

            if len(jd_words) == 0:
                score = 0
            else:
                score = round(
                    (len(matched_words) / len(jd_words)) * 100,
                    2
                )

            candidate_scores.append({

                "filename": resume["filename"],

                "score": score,

                "matched_words": sorted(list(matched_words)),

                "missing_words": sorted(list(jd_words - resume_words)),

                "resume_text": resume["text"]

            })

        # ------------------------------------------
        # Sort Highest Score First
        # ------------------------------------------

        candidate_scores = sorted(

            candidate_scores,

            key=lambda x: x["score"],

            reverse=True

        )

        st.session_state["candidate_scores"] = candidate_scores



# ==========================================================
# Best Candidate
# ==========================================================

if "candidate_scores" in st.session_state:

    candidates = st.session_state["candidate_scores"]

    if len(candidates):

        best = candidates[0]

        st.markdown("---")

        st.markdown(
        f"""
        <div style="background:#dcfce7;
                    padding:25px;
                    border-radius:15px;
                    border-left:8px solid green;">

        <h2>🏆 Best Candidate</h2>

        <h3>{best['filename']}</h3>

        <h1 style="color:green;">
        {best['score']}%
        </h1>

        </div>
        """,
        unsafe_allow_html=True
        )


