import streamlit as st
import extra_streamlit_components as stx
from st_pages import add_page_title

# customized modules
from recommend import jaccard
from recommend import region as r
from recommend import company as corp

import numpy as np
import pandas as pd

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

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

add_page_title(layout="wide")
bar = st.progress(0, text="진행률")
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
st.session_state.regions = r.getRegion()

if uploaded_file:
    bar.progress(25, text="진행률")
    if 'recommend_jobs' not in st.session_state or st.session_state.recommend_jobs is None:
        save_upload_file('_pdf', uploaded_file)
        GPT_KEY = st.secrets.KEY.GPT_KEY
        st.session_state.recommend_jobs = jaccard.recommend_job(uploaded_file, GPT_KEY)
    if st.session_state.recommend_jobs :
        recommend_jobs = st.session_state.recommend_jobs
        if 'similarity_jobs' not in st.session_state or st.session_state.similarity_jobs is None:
            st.session_state.similarity_jobs = jaccard.recommend_similarity_job(recommend_jobs)
        st.write(f"추천 직업 : {recommend_jobs[0]['occupation3Nm']}")
    if 'selected_region' not in st.session_state or st.session_state.selected_region is None:
        with st.expander(label="지역 선택", expanded=True):
            regions = st.session_state.regions
            showRegion(regions)
            if st.session_state.selected_region is not None:
                print("get region")
    if st.session_state.selected_job is None:
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
                break
        if st.session_state.jobs is not None:
            for job in st.session_state.jobs:
                if st.session_state.selected_job == job[1]:
                    st.session_state.clicked_jobCd = job[0]
                    st.session_state.clicked_jobNm = job[1]
                    break
            router.route('/view')
