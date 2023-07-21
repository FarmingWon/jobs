import openai
import streamlit as st
from openai.error import OpenAIError

message = """
직업에 대하여 소개를 해줘.
해당 직업이 주로 하는 일, 필요한 skill 및 역량, 전망에 대하여 말해줘.
"""

messages=[{"role": "system", "content": message }]

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def clear_submit():
    st.session_state["submit"] = False
    
def ask(q):
    q = {"role" : "user" , "content" : q}
    messages.append(q)

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = messages
    )

    res = response.to_dict_recursive()
    bot_text  = response['choices'][0]['message']['content']
    bot_input = {"role": "assistant", "content": bot_text }

    messages.append(bot_input)

    return bot_text

# Load your API key from an environment variable or secret management service
GPT_KEY = st.secrets.KEY.GPT_KEY
openai.api_key = GPT_KEY

st.header("직업 상세 설명")
with st.sidebar:
    htmlSide=f"""
        <br/>
        <p>ChatGPT를 이용해 직업의 상세 설명을 제공하는 페이지에요.</p>
        <p>궁금하거나 직업 추천을 통해 나온 결과를 입력해보세요!</p>
        <p>잠시 기다리면 직업에 대한 설명이 나올거에요!</p>
        <div id="logo">
            <h5>
                <span>Powered By  &nbsp; &nbsp; &nbsp;</span>
                <img src="data:image/png;base64,{img_to_bytes("./img/openai_logo.PNG")}" style="width:180px; height:60px;">
            </h5>
        </div>
    """
    st.markdown(htmlSide, unsafe_allow_html=True)

query = st.text_area('직업에 대하여 물어보세요.', value="웹 개발자는 무슨 직업인지 설명해줘.", on_change=clear_submit)
button = st.button("submit")

if button or st.session_state.get("submit"):
    st.session_state["submit"] = True

    try:
        with st.spinner("Calling Job Description API..."):
            ans = ask(query)

        st.markdown("#### Answer")
        st.markdown(ans)

    except OpenAIError as e:
        st.error(e._message)

