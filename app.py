import streamlit as st

st.title("TODO App")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "task_input" not in st.session_state:
    st.session_state.task_input = ""

st.text_input("タスクを入力", key="task_input")

if st.button("追加"):
    task_text = st.session_state.task_input.strip()
    if not task_text:
        st.warning("タスクを入力してください。")
    elif task_text in st.session_state.tasks:
        st.warning("同じタスクは追加できません。")
    else:
        st.session_state.tasks.append(task_text)
        st.session_state.task_input = ""
        st.success(f"タスクを追加しました: {task_text}")
        st.rerun()

if st.session_state.tasks:
    st.subheader("タスク一覧")
    for index, task in enumerate(st.session_state.tasks, start=1):
        st.write(f"{index}. {task}")
