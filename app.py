import streamlit as st
import pandas as pd 
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from recommend import jaccard
from recommend import region as r
from recommend import company as corp

def showRegion(regions):
    regionsNm = [reg[1] for reg in regions]
    st.session_state.selected_region = st.radio(label = '', options= regionsNm)
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

def showJob(recommend_jobs, similarity_jobs):
    st.session_state.jobs = [[recommend_jobs[0]['occupation3'], recommend_jobs[0]['occupation3Nm']]]
    tmp2 = [[job[0]['occupation3'],job[0]['occupation3Nm']] for job in similarity_jobs]
    st.session_state.jobs.extend(tmp2)
    jobsNm = [job[1] for job in st.session_state.jobs]
    st.session_state.selected_job= st.radio(label='',options=jobsNm)
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
 

def save_upload_file(dir, file):
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(os.path.join(dir, file.name), 'wb') as f:
        f.write(file.getbuffer())
    # return st.success("save file : {} in {}".format(file.name, dir))

def initRouter():
  return stx.Router({'/': recom, '/map': map})
    
def recom():
    st.title("이력서 PDF파일을 통한 직업 추천")
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    st.session_state.regions = r.getRegion()
    st.session_state.selected_region = None
    st.session_state.selected_job = None
    st.session_state.recommend_jobs = None
    st.session_state.similarity_jobs = None
    st.session_state.jobs = None
    if uploaded_file:
        if st.session_state.recommend_jobs is None:
            save_upload_file('_pdf', uploaded_file)
            GPT_KEY = st.secrets.KEY.GPT_KEY
            st.session_state.recommend_jobs = jaccard.recommend_job(uploaded_file, GPT_KEY)
        if st.session_state.recommend_jobs :
            recommend_jobs = st.session_state.recommend_jobs
            if st.session_state.similarity_jobs is None:
                st.session_state.similarity_jobs = jaccard.recommend_similarity_job(recommend_jobs)
            st.write(f"추천 직업 : {recommend_jobs[0]['occupation3Nm']}")
        if st.session_state.selected_region is None:
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
            if st.session_state.clicked_regionCd != None and st.session_state.clicked_regionNm != None and st.session_state.clicked_jobCd != None and st.session_state.clicked_jobNm != None:
                st.session_state.gangso, st.session_state.recommend_company = corp.find_company(st.session_state.clicked_regionCd, st.session_state.clicked_jobCd, st.secrets.KEY.MONGO_KEY)
                cols = ['기업명',' 기업규모 ',' 근로계약 ',' 기업위치 ',' 근무시간' ,'URL']
                if len(st.session_state.gangso) != 0:
                    # with st.expander(label = '강소기업 추천', expanded=True):
                    gangso_df = pd.DataFrame(st.session_state.gangso, columns=cols)
                    # gangso_df['URL'] = gangso_df['URL'].apply(format_link)
                    st.subheader('강소기업 기업목록')
                    st.table(gangso_df.head())
                if len(st.session_state.recommend_company) != 0:
                    # with st.expander(label = '일반기업 추천', expanded=True):
                    company_df = pd.DataFrame(st.session_state.recommend_company, columns=cols)
                    # company_df['URL'] = company_df['URL'].apply(format_link)
                    st.subheader('기업 기업목록')
                    # st.dataframe(company_df.to_html(escape=False), unsafe_allow_html=True)
                    st.table(company_df)
                st.session_state.clicked_regionCd = None
                st.session_state.clicked_regionNm = None
                st.session_state.clicked_jobCd = None
                st.session_state.clicked_jobNm = None

def map():
    st.title('주변 인프라')

def main():
    with st.sidebar:
        if st.button('직장 선택'):
          router.route('/')
        elif st.button('인프라 확인'):
          router.route('/map')

if __name__ == "__main__":
    main()
