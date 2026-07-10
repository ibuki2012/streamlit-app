import streamlit as st

st.title("TODO App")

task_text = st.text_input("タスクを入力")

if st.button("追加"):
    if task_text.strip():
        st.success(f"タスクを追加しました: {task_text}")
    else:
        st.warning("タスクを入力してください。")
