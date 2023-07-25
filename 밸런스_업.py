# -- import modules start --
#streamlit
import streamlit as st
import extra_streamlit_components as stx
from st_pages import Page, add_page_title, show_pages
from streamlit_extras.switch_page_button import switch_page

import sys
import base64
from pathlib import Path
import pandas as pd
import math

# -- import modules end --

# func: setting variable & files
def set_variable():
    st.session_state.selected_region = None
    st.session_state.selected_job = None
    st.session_state.recommend_jobs = None
    st.session_state.similarity_jobs = None
    st.session_state.jobs = None
    st.session_state.pageName = None
    st.session_state.query = None
    st.session_state.infra = None
    if 'score' not in st.session_state:  
      st.session_state.score = None
    if 'selectJob' not in st.session_state:  
      st.session_state.selectJob = False
    if 'selectRegion' not in st.session_state:  
      st.session_state.selectRegion = False
    if 'selectCompany' not in st.session_state:  
      st.session_state.selectCompany = False
    if 'selectWLB' not in st.session_state:  
      st.session_state.selectWLB = False
    if 'barScore' not in st.session_state:
      st.session_state.barScore = False


def set_csv():
  st.session_state.df_subway = pd.read_csv('csv/subway.csv')
  st.session_state.df_bus = pd.read_csv('csv/bus.csv')
  st.session_state.df_hospital = pd.read_csv('csv/hospital.csv')
  st.session_state.df_museum = pd.read_csv('csv/museum.csv')
  st.session_state.df_starbucks = pd.read_csv('csv/starbucks_busan.csv')
  st.session_state.df_exercise = pd.read_csv('csv/exercise.csv')
  st.session_state.df_oliveyoung = pd.read_csv('csv/oliveyoung.csv')

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def main():
    #side
    with st.sidebar:
        htmlSide=f"""
        <br/>
        <a href="#what-is-balanceup-balanceup" style="text-align:left; text-decoration:center; color:inherit;"><p>✔ What is BalanceUP?</p></a>
        <a href="#how-to-use-balancup" style="text-align:left; text-decoration:center; color:inherit;"><p>🔔 How To Use</p></a>
        <a href="#why-balanceup-balanceup" style="text-align:left; text-decoration:center; color:inherit;"><p>❓ Why BalanceUP?</p></a>
        <a href="#feature-balanceup" style="text-align:left; text-decoration:center; color:inherit;"><p>📝Feature</p></a>
        """
        st.markdown(htmlSide, unsafe_allow_html=True)
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

    #main
    html1 = f"""
    <!-- Font Awesome -->
    <link
    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    rel="stylesheet"/>
    <!-- Google Fonts -->
    <link
    href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"
    rel="stylesheet"/>
    <!-- MDB -->
    <link
    href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/6.4.0/mdb.min.css"
    rel="stylesheet"/>
    <!-- MDB -->
    <script
    type="text/javascript"
    src="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/6.4.0/mdb.min.js"></script>
    <div class="container wrap">
        <div class="container title">
            <div class="row" style="margin-top: 0%;">
                <div class="col-md-4"></div>
                <div class="col-md-5 d-flex justify-content-center">
                    <img src="data:image/png;base64,{img_to_bytes("./img/balanceup_logo.png")}" style="width: 200px; height: 200px;">  
                </div>
                <div class="col-md-4"></div>
            </div>
        </div>
        <div class="container">
            <div class="subtitle" id="subtitle">
                <p class="h5 text-center">이력서만 등록해도 맞춤 포지션 추천과 기업 평가까지!!</p>
                <br/>
                <p class="text-center" style="margin-bottom:0px;">
                    <small>내 이력서를 분석하여 연관성이 높은 포지션들을 알려드려요.</small>
                </p>
                <p class="text-center">
                    <small>기업 평가는 기업 주변 인프라의 접근성과 다양성을 기준으로 제공됩니다.</small>
                </p>
            </div>
        </div>
        <br/>
        <div class="container">
            <ol class="c-stepper">
                <li class="c-stepper-item">
                    <p class="c-stepper-title">이력서 파일 입력</p>
                </li>
                <li class="c-stepper-item">
                    <p class="c-stepper-title">개인 맞춤 직무 추천</p>
                </li>
                <li class="c-stepper-item">
                    <p class="c-stepper-title">기업의 직업/지역 선택</p>
                </li>
                <li class="c-stepper-item">
                    <p class="c-stepper-title">기업 인프라 평가 + ELEI 차트</p>
                </li>
            </ol>
        </div>
    </div>
    <div class="container" style="margin-bottom: 10%"></div>
    """ + """
    <style type="text/css">
        @font-face {
            font-family: 'Pretendard-Regular';
            src: url('https://cdn.jsdelivr.net/gh/Project-Noonnu/noonfonts_2107@1.1/Pretendard-Regular.woff') format('woff');
            font-weight: 400;
            font-style: normal;
        }
        .container {
            font-family: 'Pretendard-Regular';
        }
        .container.wrap{
            overflow: hidden;
            #height: 700px;
            padding: 500px 0px 0px 0px;
            top:100%;
            left: 50%;
            position: relative;
            transform: translate(-50%, -50%);
            transition: transform 300ms, box-shadow 300ms;
            display: contents;
        }
        .container.wrap:after {
            left: 80%;
            bottom: -24%;
            background-color: rgb(255 67 67 / 20%);
            animation: wawes 7s infinite;
        }
        .container.wrap::before {
            left: 79%;
            bottom: -20%;
            background-color: rgb(255 0 0 / 21%);
        
            animation: wawes 6s infinite linear;
        }

        
        .container.wrap::before,
        .container.wrap::after {
            content: '';
            position: absolute;
            width: 500px;
            height: 500px;
            border-top-left-radius: 40%;
            border-top-right-radius: 45%;
            border-bottom-left-radius: 35%;
            border-bottom-right-radius: 40%;
            z-index: 0;
        }

        @keyframes wawes {
            from {
                transform: rotate(0);
            }
        
            to {
                transform: rotate(360deg);
            }
        }

        .c-stepper {
            display: flex;
            flex-wrap: wrap;
            margin: 0;
            padding: 0;
        }

        .c-stepper-title {
            font-size: small;
        }
        
        .c-stepper-item {
            flex: 1;
            display: flex;
            flex-direction: column;
            text-align: center;
        }
        
        .c-stepper-item:before {
            --size: 3rem;
            content: '';
            position: relative;
            z-index: 1;
            display: block;
            width: var(--size);
            height: var(--size);
            border-radius: 50%;
            border: 0.5px solid #0E3E89;
            margin: 0 auto;
            background-color: #ffffff;
        }
        .c-stepper-item:not(:last-child):after {
            content: '';
            position: relative;
            top: 1.5rem;
            left: 50%;
            height: 1.5px;
            background-color: #D1D1D1;
            order: -1;
        }
        .c-stepper-item.completed:before {
            --size: 3rem;
            content: '';
            position: relative;
            z-index: 1;
            display: block;
            width: var(--size);
            height: var(--size);
            border-radius: 50%;
            border: 0.5px solid #0E3E89;
            margin: 0 auto;
            background-color: #0E3E89
        }
    </style>
    """
    st.markdown(html1, unsafe_allow_html=True)

    m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #0C377A;
        color: #ffffff;
        width: 100%;
        height: 100%;
        margin-top: 0%;
    }
    </style>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        if st.button("무료로 이용하기"):
            switch_page("이력서를_통한_직업_추천")

    html3 = f"""
        <div class="container" style="margin-top: 30%; background-color: #EDEDED; height: auto;">
            <div class="row">
                <!-- <div style="float: left; margin-left: 25%;"> -->
                <div class="col">
                    <h2>개인 맞춤 직무 추천과<br/>관련 기업의 인프라 평가까지</h2> 
                    <p>거대언어모델을 활용한 <strong>개인 커스텀 AI 직무 추천</strong>과<br/>밸런스업의 내부 평가 모델을 통한 ELEI 차트를 제공합니다.</p>
                    <br/>
                    <p style="align-items-bottom"><small>*ELEI(Enterprise Living Environment Index): 기업 생활 환경 지수 </small></p>
                </div>
                <!-- <div style="float: left;"> -->
                <div class="col">
                    <img src="data:image/png;base64,{img_to_bytes("img/tmpImg.png")}"  style="height: 300px; width: 300px; margin-left: 10%;">
                </div>
            </div>
        </div>
    """
    st.markdown(html3,unsafe_allow_html=True)     

if __name__ == "__main__":
    set_variable()
    set_csv()
    st.set_page_config(page_title="BalanceUp", layout="wide")
    main()
