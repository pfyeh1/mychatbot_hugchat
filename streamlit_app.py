import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

st.set_page_config(page_title = "🤗💬 HugChat")

with st.sidebar:
    st.title("PF's 🤗💬 HugChat")
    if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
        st.success("Login credentials already provided", icon = '✅')
        hf_email = st.secrets['EMAIL']
        hf_pass = st.secrets['PASS']
    else:
        hf_email = st.text_input('Enter E-mail:', type = 'password')
        hf_pass = st.text_input('Enter password:', type = 'password')
        
        if not(hf_email and hf_pass):
            st.warning("Please enter your credentials!")
        else:
            st.success('Proceed to entering your prompt message!')

# store LLM generated responses
if 'messages' not in st.session_state.keys():
    st.session_state.messages = [
                                {"role":"assistant",
                                "content":"How may I help you?"
                                }]

# display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# function for generating LLM response
def generate_response(prompt_input, email, passwd):
    # hugging face login
    sign = Login(email, passwd)
    cookies = sign.login()
    
    sign.saveCookies() # save cookies
    
    # create chat bot
    chatbot = hugchat.ChatBot(cookies = cookies.get_dict())
    response = chatbot.chat(prompt_input)
    return response
    
    #return chatbot.chat(prompt_input)
    
# accept user prompt
if prompt := st.chat_input(disabled = not (hf_email and hf_pass)):
    st.session_state.messages.append({'role':'user', 'content':prompt})
    with st.chat_message('user'):
        st.write(prompt)

# generate bot response outout
if st.session_state.messages[-1]['role'] != 'assistant':
    with st.chat_message('assistant'):
        with st.spinner("Tinking..."):
            response = generate_response(prompt, hf_email, hf_pass)
            st.write(response)
    message = {'role':'assistant', 'content':response}
    st.session_state.messages.append(message)