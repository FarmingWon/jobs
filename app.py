# -- import modules start --
#streamlit
import streamlit as st
import extra_streamlit_components as stx
from st_pages import Page, add_page_title, show_pages

import sys
import base64
from pathlib import Path

# -- import modules end --

# func: setting variable & files
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

def main():
    html = """
    <!-- Font Awesome -->
    <link
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
      rel="stylesheet"
    />
    <!-- Google Fonts -->
    <link
      href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"
      rel="stylesheet"
    />
    <!-- MDB -->
    <link
      href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/6.4.0/mdb.min.css"
      rel="stylesheet"
    />
    <!-- MDB -->
    <script
      type="text/javascript"
      src="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/6.4.0/mdb.min.js"
    ></script>
    <div class="title"><h3>🎈Balance UP!</h3></div>
    <div><p>반가워요. BalanceUP 직업추천 서비스에요.</p><div>
    <hr/>
    <div class="About" id="About">
        <div class="card" id="whatis">
            <div class="card-header" id="whatis">
                <h5>
                    <i class="fas fa-question-circle fa-sm me-2 opacity-70" style="color:skyblue"></i>
                    What is
                    <span style="color:#DC2D1C">BalanceUP</span>:
                    <span>&nbsp; BalanceUP은 어떤 서비스일까?</span>
                </h5>
            </div>
            <div class="card-body">
                <p>BalanceUP은 거대언어모델인 GPT와 지식그래프(Knowledge Graph)를 기반으로 구직자의 이력서에 맞춰 직업을 추천해주는 서비스를 제공합니다.</p>
                <p>또 추천된 직업을 바탕으로 워크넷에 채용공고가 올라와 있는 회사의 목록을 보여줍니다. 그리고 그 회사들의 주변 인프라에 대한 점수를 매기고 사용자가 볼 수 있도록 시각화해주죠.</p>
            </div>
        </div>
        <br/>
        <div class="card" id="whyis">
            <div class="card-header" id="whyis">
                <h5>
                    <i class="fas fa-question-circle fa-sm me-2 opacity-70" style="color:skyblue"></i>
                    Why
                    <span style="color:#DC2D1C">BalanceUP</span>:
                    <span>&nbsp; BalanceUP이 만들어진 이유!
                </h5>
            </div>
            <div class="card-body">
                내용
            </div>
        </div>
        <br/>
        <div class="card" id="feature">
            <div class="card-header" id="feature">
                <h5>
                    <i class="fas fa-question-circle fa-sm me-2 opacity-70" style="color:skyblue"></i>
                    Feature: 
                    <span style="color:#DC2D1C">&nbsp; BalanceUP</span>만의 특징!
                </h5>
            </div>
            <div class="card-body">
                내용
            </div>
        </div>
    </div>
    <hr/>
    <div id="howtouse">
        <div id="header">
            <h5>
                <span style="color:#DC2D1C">How To Use?</span>:<span>&nbsp; BalanceUP 사용법!</span>
            </h5>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

    with st.sidebar:
        htmlSide=f"""
        <br/>
        <a href="#what-is-balanceup-balanceup" style="text-align:left; text-decoration:center; color:inherit;"><p>✔ What is BalanceUP?</p></a>
        <a href="#why-balanceup-balanceup" style="text-align:left; text-decoration:center; color:inherit;"><p>❓ Why BalanceUP?</p></a>
        <a href="#feature-balanceup" style="text-align:left; text-decoration:center; color:inherit;"><p>📝Feature</p></a>
        <a href="#how-to-use-balancup" style="text-align:left; text-decoration:center; color:inherit;"><p>🔔 How To Use</p></a>
        <div id="logo">
            <h5>
                <span>Powered By  &nbsp; &nbsp; &nbsp;</span>
                <img src="data:image/png;base64,{img_to_bytes("./img/openai_logo.PNG")}" style="width:180px; height:60px;">
            </h5>
        </div>
        """
        st.markdown(htmlSide, unsafe_allow_html=True)

if __name__ == "__main__":
    set_variable()
    st.set_page_config(page_title="BalanceUp", layout="wide")
    main()
