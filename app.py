# -- import modules start --
#streamlit
import streamlit as st
import extra_streamlit_components as stx
from st_pages import Page, add_page_title, show_pages

# -- import modules end --

# func: setting variable & files
def set_variable():
    st.session_state.selected_region = None
    st.session_state.selected_job = None
    st.session_state.recommend_jobs = None
    st.session_state.similarity_jobs = None
    st.session_state.jobs = None
    st.session_state.score = None

def main():
    html = """
    <div class="title"><h3>🎈Balance UP!</h3></div>
    <div><p>반가워요. BalanceUP 직업추천 서비스에요.</p><div>
    <hr/>
    <div class="About">
        <div class="About_title">
            <h4><span style="color:#DC2D1C">BalanceUP</span>에 대해...</h4>
        </div>
        <div class="subtitle">
            <h6><span>BalanceUP은 무엇인가요?</span></h6>
        </div>
        <div class="context">
            <p><span>BalanceUP이 하는 일</span></p>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

if __name__ == "__main__":
    set_variable()
    st.set_page_config(page_title="BalanceUp", layout="wide")
    main()
