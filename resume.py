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
color:blue;
}

section[data-testid="stSidebar"] *{
color:blue;
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
background: yellow;
padding:20px;
border-radius:15px;
box-shadow:0px 4px 15px rgba(0,0,0,.15);
margin-bottom:20px;
}

/* Upload */

[data-testid="stFileUploader"]{
background:;
padding:15px;
border-radius:12px;
}

/* Buttons */

.stButton>button{

width:100%;

background: #2563eb;

color:black;

border-radius:10px;

height:50px;

font-size:18px;

font-weight:bold;

border:none;

}

.stButton>button:hover{

background: #1d4ed8;

#}

#/* TextArea */

#textarea{

#border-radius:10px !important;
#color:block;

}

/* Select Box */

div[data-baseweb="select"]{

border-radius:10px;

}

/* Success */

.success{

background: #dcfce7;

padding:15px;

border-radius:10px;

color:green;

font-weight:bold;

}

</style>"""

, unsafe_allow_html=True)

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
