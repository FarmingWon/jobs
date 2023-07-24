# -- import modules start --
import streamlit as st
import extra_streamlit_components as stx
from st_pages import add_page_title
from streamlit.components.v1 import html

# customized modules
from recommend import jaccard
from recommend import region as r
from recommend import company as corp

import numpy as np
import pandas as pd

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import base64
from pathlib import Path

# -- import modules end --
def set_variable():
    st.session_state.selected_region = None
    st.session_state.selected_job = None
    st.session_state.recommend_jobs = None
    st.session_state.similarity_jobs = None
    st.session_state.jobs = None
    st.session_state.score = None

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def get_progress_score():
    st.session_state.barScore = 0
    if st.session_state.selectJob:
        st.session_state.barScore = 25
        if st.session_state.selectRegion:
            st.session_state.barScore = 50
            if st.session_state.selectCompany:
                st.session_state.barScore = 75
                if st.session_state.selectWLB:
                    st.session_state.barScore = 100

# func: save pdf file
def save_upload_file(dir, file):
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(os.path.join(dir, file.name), 'wb') as f:
        f.write(file.getbuffer())

# func: UI for Select Region
def showRegion(regions):
    regionsNm = [reg[1] for reg in regions]
    st.session_state.selected_region = st.radio(label = '', options= regionsNm)
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

# func: UI for Select Job
def showJob(recommend_jobs, similarity_jobs):
    st.session_state.jobs = [[recommend_jobs[0]['occupation3'], recommend_jobs[0]['occupation3Nm']]]
    tmp2 = [[job[0]['occupation3'],job[0]['occupation3Nm']] for job in similarity_jobs]
    st.session_state.jobs.extend(tmp2)
    jobsNm = [job[1] for job in st.session_state.jobs]
    st.session_state.selected_job= st.radio(label='',options=jobsNm)
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

#download resume
def download_link(data, file_name, file_label):
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">{file_label}</a>'
    return href

get_progress_score()
htmlTitle = """
    <div><h3>📝이력서를 통한 직업 추천</h3></div>
    """
st.markdown(htmlTitle, unsafe_allow_html=True)

with st.sidebar:
    htmlSide=f"""
        <br/>
        <ul>
            <li style="text-align:left; text-decoration:center; color:inherit;">이력서를 올려서 추천직업을 확인해보세요.</li>
            <li style="text-align:left; text-decoration:center; color:inherit;"> 가장 적합한 직업과 유사한 직업을 추천해드릴게요!</li>
            <li style="text-align:left; text-decoration:center; color:inherit;"> 지역과 직업을 고르면 채용정보도 추천해드릴게요!</li>
        </ul>
    """
    st.markdown(htmlSide, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    bar = st.progress(st.session_state.barScore, text= f"진행률 {st.session_state.barScore}%")
    st.sidebar.markdown("---")
    htmlSide2=f"""
        <div id="logo">
            <h5>
                <span>Powered By  &nbsp; &nbsp; &nbsp;</span>
                <img src="data:image/png;base64,{img_to_bytes("./img/openai_logo-removebg.png")}" style="width:180px; height:60px;">
            </h5>
        </div>
        <div id="logo">
            <h5>
                <span>Powered By  &nbsp; &nbsp; &nbsp;</span>
                <img src="data:image/png;base64,{img_to_bytes("./img/mongodb logo.png")}" style="width:180px; height:60px;">
            </h5>
        </div>
        <div id="logo">
            <h5>
                <span>Powered By  &nbsp; &nbsp; &nbsp;</span>
                <img src="data:image/png;base64,{img_to_bytes("./img/Neo4j-logo_color.png")}" style="width:180px; height:60px;">
            </h5>
        </div>
        """
    st.markdown(htmlSide2, unsafe_allow_html=True)

file_path = './_pdf/ws.pdf'
with open(file_path, 'rb') as file:
    pdf_data= file.read()
download_btn = download_link(pdf_data, "sample_data.pdf", "여기")
htmlCode= f"""
샘플 파일을 다운하고싶으면 {download_btn}를 눌러봐요.
"""
st.markdown(htmlCode, unsafe_allow_html=True)
uploaded_file = st.file_uploader("이력서를 올려보세요!", type="pdf")
st.session_state.regions = r.getRegion()

if uploaded_file:
    if 'recommend_jobs' not in st.session_state or st.session_state.recommend_jobs is None:
        save_upload_file('_pdf', uploaded_file)
        GPT_KEY = st.secrets.KEY.GPT_KEY
        st.session_state.recommend_jobs = jaccard.recommend_job(uploaded_file, GPT_KEY)
    if st.session_state.recommend_jobs :
        recommend_jobs = st.session_state.recommend_jobs
        if 'similarity_jobs' not in st.session_state or st.session_state.similarity_jobs is None:
            st.session_state.similarity_jobs = jaccard.recommend_similarity_job(recommend_jobs)
        jobsHtml = f"""
            <p>가장 적합한 직업은 <strong>{recommend_jobs[0]['occupation3Nm']}</strong>이네요. 유사한 직업도 같이 보여드릴게요.</p>
            <p>지역과 직업을 선택하면 채용공고를 보여드릴게요.</p>
        """
        st.markdown(jobsHtml, unsafe_allow_html=True)
        st.write(f"")
    if 'selected_region' not in st.session_state or st.session_state.selected_region is None:
        with st.expander(label="지역 선택", expanded=True):
            regions = st.session_state.regions
            showRegion(regions)

    if 'selected_job' not in st.session_state or st.session_state.selected_job is None:
        with st.expander(label = '직업 선택', expanded=True):
             if st.session_state.recommend_jobs is not None and st.session_state.similarity_jobs is not None:
                recommend_jobs = st.session_state.recommend_jobs
                similarity_jobs = st.session_state.similarity_jobs
                showJob(st.session_state.recommend_jobs, st.session_state.similarity_jobs)
    regionBtn_clicked = st.button("선택")
    if regionBtn_clicked:
        st.session_state.clicked_regionCd = None
        st.session_state.clicked_regionNm = None
        st.session_state.clicked_jobCd = None
        st.session_state.clicked_jobNm = None
        for region in st.session_state.regions:
            if st.session_state.selected_region == region[1]:
                st.session_state.clicked_regionCd = region[0]
                st.session_state.clicked_regionNm = region[1]
                st.session_state.selectRegion = True
                get_progress_score()
                break
        if st.session_state.jobs is not None:
            for job in st.session_state.jobs:
                if st.session_state.selected_job == job[1]:
                    st.session_state.clicked_jobCd = job[0]
                    st.session_state.clicked_jobNm = job[1]
                    st.session_state.selectJob = True
                    get_progress_score()
                    break
        bar.progress(st.session_state.barScore, text= f"진행률 {st.session_state.barScore}%")
        st.write('-----completed-----')
        for k in st.session_state:
            st.write(k)
        st.markdown("<script type='text/javascript'>location.href='/직장_선택'</script>", unsafe_allow_html=True)

