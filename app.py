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
        <div class="card" name="whatis">
            <div class="card-header" id="whatis">
                <h5>
                    <i class="fas fa-question-circle fa-sm me-2 opacity-70" style="color:skyblue"></i>
                    <span style="color:#DC2D1C">BalanceUP</span>은 어떤 서비스일까?
                </h5>
            </div>
            <div class="card-body">
                내용
            </div>
        </div>
        <br/>
        <div class="card" name="whyis">
            <div class="card-header" id="whyis">
                <h5>
                    <i class="fas fa-question-circle fa-sm me-2 opacity-70" style="color:skyblue"></i>
                    <span style="color:#DC2D1C">BalanceUP</span>이 만들어진 이유:
                </h5>
            </div>
            <div class="card-body">
                내용
            </div>
        </div>
        <br/>
        <div class="card" name="feature">
            <div class="card-header" id="feature">
                <h5>
                    <i class="fas fa-question-circle fa-sm me-2 opacity-70" style="color:skyblue"></i>
                    <span style="color:#DC2D1C">BalanceUP</span>만의 특징!
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
                <span style="color:#DC2D1C">How To Use?</span>
            </h5>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

    with st.sidebar:
        htmlSide=f"""
        <br/>
        <a href="#balanceup"><p>1</p></a>
        <p>2</p>
        <p>3</p>
        <a href="#how-to-use" style="text-align:center; text-decoration:center; color:inherit;"><p>How To Use</p></a>
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
