import streamlit as st
import anthropic

client = anthropic.Anthropic()
st.title("Chat helper")
q = st.text_input("Ask")
if q:
    r = client.messages.create(model="claude-sonnet-4-5", max_tokens=500, messages=[{"role": "user", "content": q}])
    st.write(r.content[0].text)
