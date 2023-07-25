# -- import modules start --
#streamlit
import streamlit as st
import extra_streamlit_components as stx
from st_pages import Page, add_page_title, show_pages
from streamlit_extras.switch_page_button import switch_page
from streamlit_javascript import st_javascript

import sys
import base64
from pathlib import Path
import pandas as pd
import math

#openai
import openai
from openai.error import OpenAIError
from streamlit_chat import message
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

def clear_submit():
    st.session_state["submit"] = False
    
def ask(q):
    message = """
    직업에 대하여 소개를 해줘. 질문에도 답하고,
    해당 직업이 주로 하는 일, 필요한 skill 및 역량, 전망에 대하여 말해줘.
    """
    messages=[{"role": "system", "content": q },
              {"role" : "assistant", "content" : message}]
    q = {"role" : "user" , "content" : q}
    messages.append(q)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages = messages
    )

    bot_text  = response['choices'][0]['message']['content']
    bot_input = {"role": "assistant", "content": bot_text }

    messages.append(bot_input)

    return bot_text


def main():
    #side
    with st.sidebar:
        htmlSide=f"""
        <div class="container sidebar">
            <a href="#" style="text-align:left; text-decoration:center; color:inherit;"><p>✔ What is BalanceUP?</p></a>
            <a href="#" style="text-align:left; text-decoration:center; color:inherit;"><p>🔔 How To Use</p></a>
            <a href="#" style="text-align:left; text-decoration:center; color:inherit;"><p>❓ Why BalanceUP?</p></a>
            <a href="#" style="text-align:left; text-decoration:center; color:inherit;"><p>📝Feature</p></a>
        </div>
        """
        st.markdown(htmlSide, unsafe_allow_html=True)

    #main
    htmlHeader = f"""
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
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="./script/jquery-fadethis-master/dist/jquery.fadethis.min.js"></script>
    """
    st.markdown(htmlHeader, unsafe_allow_html=True)
    st_javascript("""
    <script>$(window).fadeThis();</script>
    """)
    html1=f"""
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
            padding: 450px 0px 0px 0px;
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
            margin-top:5px;
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


    htmlt = """
        <div style = "height : 150px"></div>    
    """
    st.markdown(htmlt, unsafe_allow_html=True)

    empty,con3,empty2= st.columns([0.1,0.8,0.1])
    with con3:
        GPT_KEY = st.secrets.KEY.GPT_KEY
        openai.api_key = GPT_KEY
        st.title("JobsGPT의 직업 상담")

        if 'generated' not in st.session_state: # 초기화
            st.session_state['generated'] = [
                                            """웹 개발자가 되기 위해서는 몇 가지 단계를 거쳐야합니다. 먼저, 프로그래밍 언어를 학습해야합니다. 웹 개발에서는 일반적으로 HTML, CSS, JavaScript와 같은 기본 언어를 알아야합니다. 이러한 언어들은 웹 사이트의 구조, 디자인 및 상호 작용을 구현하는 데 사용됩니다.


또한, 웹 개발에 필요한 프레임워크나 라이브러리를 습득하는 것이 중요합니다. 예를 들어, React, Angular 또는 Vue.js와 같은 프레임워크를 사용하여 웹 애플리케이션을 개발할 수 있습니다. 이러한 도구들은 개발 시간을 단축하고 효율적인 코드 작성을 도와줍니다.


또한, 데이터베이스 및 서버 측 기술을 이해하는 것도 중요합니다. 웹 개발자는 사용자 데이터를 저장하고 관리하기 위해 데이터베이스를 사용하며, 서버 측 기술을 사용하여 웹 애플리케이션을 호스팅하고 구동시킵니다. 대표적인 데이터베이스는 MySQL, PostgreSQL, MongoDB 등이 있습니다.


웹 개발자가 가져야할 기타 필수 스킬에는 문제 해결 능력, 시스템 아키텍처 이해, 협업 능력, 디자인 원칙에 대한 이해 등이 있습니다.


마지막으로, 웹 개발자의 전망은 매우 밝습니다. 모든 조직과 기업이 온라인 존재를 강화하려고하는 현대 비즈니스 환경에서 웹 개발자는 매우 필요한 직업입니다. 또한, 기술의 빠른 발전으로 인해 웹 개발은 계속해서 성장하고 있는 분야입니다. 따라서 웹 개발자는 취업과 경력 발전에 매우 좋은 전망을 가지고 있습니다."""]

        if 'past' not in st.session_state: # 초기화
            st.session_state['past'] = ["웹 개발자가 되려면 어떻게 해야돼?."]


        query = st.text_area('직업에 대하여 물어보세요.', value="", on_change=clear_submit, placeholder="백엔드 개발자가 되려면 어떤 공부를 해야돼?")
        button = st.button("submit")
        if button or st.session_state.get("submit"):
            st.session_state["submit"] = True
            try:
                with st.spinner("Calling Job Description API..."):
                    
                    output = ask(query)
                    st.session_state.past.append(query)
                    st.session_state.generated.append(output)

            except OpenAIError as e:
                st.error(e._message)

        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])-1, -1, -1):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i)) 

    html3 = f"""
        <div class="slide-bottom">
            <div class="container" style="margin-top: 30%; height: auto;">
                <div class="row">
                    <div class="col">
                        <h2>개인 맞춤 직무 추천과<br/>관련 기업의 인프라 평가까지</h2> 
                        <p>거대언어모델을 활용한 <strong>개인 커스텀 AI 직무 추천</strong>과<br/>밸런스업의 내부 평가 모델을 통한 ELEI 차트를 제공합니다.</p>
                        <br/>
                        <p style="align-items-bottom"><small>*ELEI(Enterprise Living Environment Index): 기업 생활 환경 지수로
    MZ 세대가 선호하는 인프라 환경을 기반으로 해당 기업에 대한 평가를 진행합니다.</small></p>
                    </div>
                    <div class="col">
                        <img src="data:image/png;base64,{img_to_bytes("img/tmpImg.png")}"  style="height: 300px; width: 300px; margin-left: 10%;">
                    </div>
                </div>
            </div>
        </div>
        <div class="container" style="margin-top: 10%"></div>
        <div class="container">
            <h5>Powered by</h5>
            <div class="row d-flex justify-content-center">
                <div class="col">
                    <div class="card">
                        <div class="card-body">
                            <div class="d-flex justify-content-center align-items-center" id="logo">
                                <img src="data:image/png;base64,{img_to_bytes("./img/openai_logo-removebg.png")}" style="width:180px; height:60px;">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col">
                    <div class="card">
                        <div class="card-body">
                            <div class="d-flex justify-content-center align-items-center" id="logo">
                                <img src="data:image/png;base64,{img_to_bytes("./img/mongodb logo.png")}" style="width:200px; height:60px;">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col">
                    <div class="card">
                        <div class="card-body">
                            <div class="d-flex justify-content-center align-items-center" id="logo">
                                <img src="data:image/png;base64,{img_to_bytes("./img/Neo4j-logo_color.png")}" style="width:180px; height:60px;">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row d-flex justify-content-center" style="margin-top: 5%">
                <div class="col">
                    <div class="card">
                        <div class="card-body">
                            <div class="d-flex justify-content-center align-items-center" id="logo">
                                <img src="data:image/png;base64,{img_to_bytes("./img/kakaomap_logo.jpg")}" style="width:180px; height:60px;">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col">
                    <div class="card">
                        <div class="card-body">
                            <div class="d-flex justify-content-center align-items-center" id="logo">
                                <img src="data:image/png;base64,{img_to_bytes("./img/vworld_logo.png")}" style="width:180px; height:59px;">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col">
                    <div class="card">
                        <div class="card-body">
                            <div class="d-flex justify-content-center align-items-center" id="logo">
                                <img src="data:image/png;base64,{img_to_bytes("./img/worknet_logo.png")}" style="width:180px; height:60px;">
                            </div>
                        </div>
                    </div>
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
