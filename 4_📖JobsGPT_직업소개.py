import openai
import streamlit as st
from openai.error import OpenAIError

import base64
from pathlib import Path
from streamlit_chat import message


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def clear_submit():
    st.session_state["submit"] = False
    
def ask(q):
    message = """
    직업에 대하여 소개를 해줘.
    해당 직업이 주로 하는 일, 필요한 skill 및 역량, 전망에 대하여 말해줘.
    """
    messages=[{"role": "system", "content": message }]
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

GPT_KEY = st.secrets.KEY.GPT_KEY
openai.api_key = GPT_KEY

with st.sidebar:
    htmlSide=f"""
        <br/>
        <p>ChatGPT를 이용해 직업의 상세 설명을 제공하는 페이지에요.</p>
        <p>궁금하거나 직업 추천을 통해 나온 결과를 입력해보세요!</p>
        <p>잠시 기다리면 직업에 대한 설명이 나올거에요!</p>
    """
    st.markdown(htmlSide, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    htmlSide2=f"""
        <div id="logo">
            <h5>
                <span>Powered By  &nbsp; &nbsp; &nbsp;</span>
                <img src="data:image/png;base64,{img_to_bytes("./img/openai_logo-removebg.PNG")}" style="width:180px; height:60px;">
            </h5>
        </div>
        <div id="logo">
            <h5>
                <span>Powered By  &nbsp; &nbsp; &nbsp;</span>
                <img src="data:image/png;base64,{img_to_bytes("./img/mongodb logo.PNG")}" style="width:180px; height:60px;">
            </h5>
        </div>
        <div id="logo">
            <h5>
                <span>Powered By  &nbsp; &nbsp; &nbsp;</span>
                <img src="data:image/png;base64,{img_to_bytes("./img/Neo4j-logo_color.PNG")}" style="width:180px; height:60px;">
            </h5>
        </div>
        """
    st.markdown(htmlSide2, unsafe_allow_html=True)

empty,con3,empty2= st.columns([0.1,0.5,0.1])

with con3:
    st.title("JobsGPT의 직업소개")

    if 'generated' not in st.session_state: # 초기화
        st.session_state['generated'] = [
                                        """ 웹 개발자는 인터넷에 접속 가능한 웹 사이트를 만들고 유지보수하는 직업입니다.
    웹 개발자는 주로 웹 애플리케이션 또는 웹 사이트를 구축하기 위해 프로그래밍 언어와 웹 기술을 사용합니다. 
    이 직업에서 필요한 기술과 역량은 다양하며, 주로 다음과 같은 것들이 있습니다.
    프로그래밍 언어: 웹 개발자는 주로 HTML, CSS, JavaScript 등을 사용하여 웹사이트를 구축합니다. 
    또한, 백엔드 개발에는 Python, PHP, Ruby 등의 프로그래밍 언어를 사용하기도 합니다.
    프레임워크: 웹 개발자는 프레임워크를 사용하여 개발 속도를 높이고 효율성을 높일 수 있습니다. 
    예를 들어, Django, Ruby on Rails, Laravel 등과 같은 프레임워크는 백엔드 개발에 널리 사용됩니다.
    데이터베이스: 웹 개발자는 데이터를 저장하고 관리하기 위해 데이터베이스를 다룰 수 있어야 합니다. 
    MySQL, PostgreSQL, MongoDB 등과 같은 데이터베이스 시스템을 사용합니다.
    문제 해결 능력: 웹 개발자는 다양한 문제에 직면하며, 이를 해결하기 위해 논리적인 사고와 문제 해결 능력이 필요합니다.
    웹 개발자의 전망은 매우 밝습니다. 
    인터넷이 점점 보편화되고 웹 기술의 발전으로 인해 많은 기업과 조직이 웹사이트 또는 웹 애플리케이션을 필요로 하고 있습니다. 
    따라서 웹 개발자에 대한 수요는 지속적으로 증가할 것으로 예상됩니다. 
    또한, 시장에서 꾸준한 성장을 이루고 있는 모바일 웹 개발 분야에서도 많은 기회가 있습니다.
    """]

    if 'past' not in st.session_state: # 초기화
        st.session_state['past'] = ["웹 개발자는 무슨 직업인지 설명해줘."]


    query = st.text_area('직업에 대하여 물어보세요.', value="", on_change=clear_submit, placeholder="백엔드 개발자는 무슨 직업인지 설명해줘.")
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