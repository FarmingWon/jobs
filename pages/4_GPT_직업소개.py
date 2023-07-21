import openai
import streamlit as st
from openai.error import OpenAIError

message = """
직업에 대하여 소개를 해줘.
해당 직업이 주로 하는 일, 필요한 skill 및 역량, 전망에 대하여 말해줘.
"""

messages=[{"role": "system", "content": message }]


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

