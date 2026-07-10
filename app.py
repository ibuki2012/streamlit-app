import streamlit as st


def normalize_tasks(raw_tasks):
    normalized_tasks = []
    for item in raw_tasks:
        if isinstance(item, dict):
            text = item.get("text")
            done = item.get("done", False)
            if isinstance(text, str):
                stripped_text = text.strip()
                if stripped_text:
                    normalized_tasks.append({"text": stripped_text, "done": bool(done)})
        elif isinstance(item, str):
            stripped_text = item.strip()
            if stripped_text:
                normalized_tasks.append({"text": stripped_text, "done": False})
    return normalized_tasks


st.title("TODO App")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "task_input" not in st.session_state:
    st.session_state.task_input = ""

st.session_state.tasks = normalize_tasks(st.session_state.tasks)

st.text_input("タスクを入力", key="task_input")

if st.button("追加"):
    task_text = st.session_state.task_input.strip()
    existing_task_texts = {task["text"] for task in st.session_state.tasks}
    if not task_text:
        st.warning("タスクを入力してください。")
    elif task_text in existing_task_texts:
        st.warning("同じタスクは追加できません。")
    else:
        st.session_state.tasks.append({"text": task_text, "done": False})
        st.session_state.task_input = ""
        st.success(f"タスクを追加しました: {task_text}")
        st.rerun()

if st.session_state.tasks:
    st.subheader("タスク一覧")
    for index, task in enumerate(st.session_state.tasks):
        task_col, delete_col = st.columns([0.85, 0.15])
        checkbox_key = f"task_done_{index}_{task['text']}"
        delete_key = f"delete_task_{index}_{task['text']}"

        with task_col:
            is_done = st.checkbox(task["text"], value=task["done"], key=checkbox_key)
            if is_done != task["done"]:
                st.session_state.tasks[index]["done"] = is_done
                st.rerun()

        with delete_col:
            if st.button("削除", key=delete_key):
                st.session_state.tasks.pop(index)
                st.rerun()
