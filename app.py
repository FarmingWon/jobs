# -- import modules start --
#streamlit
import streamlit as st
import extra_streamlit_components as stx
from st_pages import Page, add_page_title, show_pages
import streamlit.components.v1 as components

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
    components.html("""
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
    <div class="About">
        <div class="card">
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
    </div>
    """, height=600,)

    with st.sidebar:
        htmlSide="""
        1
        """
        st.markdown(htmlSide, unsafe_allow_html=True)

if __name__ == "__main__":
    set_variable()
    st.set_page_config(page_title="BalanceUp", layout="wide")
    main()
