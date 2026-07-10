import json
from pathlib import Path

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


TODO_FILE_PATH = Path(__file__).resolve().parent / "todos.json"


def load_tasks_from_file(file_path: Path = TODO_FILE_PATH):
    if not file_path.exists():
        return []

    with file_path.open("r", encoding="utf-8") as file:
        raw_tasks = json.load(file)

    if not isinstance(raw_tasks, list):
        raise ValueError("todos.json は配列形式である必要があります。")

    return normalize_tasks(raw_tasks)


def save_tasks_to_file(tasks, file_path: Path = TODO_FILE_PATH):
    normalized_tasks = normalize_tasks(tasks)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(normalized_tasks, file, ensure_ascii=False, indent=2)


st.title("TODO App")

if "tasks" not in st.session_state:
    try:
        st.session_state.tasks = load_tasks_from_file()
    except (json.JSONDecodeError, OSError, ValueError) as error:
        st.session_state.tasks = []
        st.error(f"todos.json の読み込みに失敗しました: {error}")

if "task_input" not in st.session_state:
    st.session_state.task_input = ""

if "task_filter" not in st.session_state:
    st.session_state.task_filter = "すべて"

st.session_state.tasks = normalize_tasks(st.session_state.tasks)

st.text_input("タスクを入力", key="task_input")
filter_options = ["すべて", "未完了", "完了"]
selected_filter = st.radio("表示フィルター", filter_options, key="task_filter")

if st.button("追加"):
    task_text = st.session_state.task_input.strip()
    existing_task_texts = {task["text"] for task in st.session_state.tasks}
    if not task_text:
        st.warning("タスクを入力してください。")
    elif task_text in existing_task_texts:
        st.warning("同じタスクは追加できません。")
    else:
        new_task = {"text": task_text, "done": False}
        st.session_state.tasks.append(new_task)
        try:
            save_tasks_to_file(st.session_state.tasks)
            st.session_state.task_input = ""
            st.success(f"タスクを追加しました: {task_text}")
            st.rerun()
        except OSError as error:
            st.session_state.tasks.pop()
            st.error(f"todos.json の保存に失敗しました: {error}")

if selected_filter == "未完了":
    filtered_indexes = [
        index for index, task in enumerate(st.session_state.tasks) if not task["done"]
    ]
elif selected_filter == "完了":
    filtered_indexes = [
        index for index, task in enumerate(st.session_state.tasks) if task["done"]
    ]
else:
    filtered_indexes = list(range(len(st.session_state.tasks)))

if st.session_state.tasks:
    st.subheader("タスク一覧")

    if not filtered_indexes:
        st.info("現在のフィルターではタスクが表示されていません。")
        if st.session_state.task_filter != "すべて" and st.button("すべてを表示"):
            st.session_state.task_filter = "すべて"
            st.rerun()
    else:
        for index in filtered_indexes:
            task = st.session_state.tasks[index]
            task_col, delete_col = st.columns([0.85, 0.15])
            checkbox_key = f"task_done_{index}_{task['text']}"
            delete_key = f"delete_task_{index}_{task['text']}"

            with task_col:
                is_done = st.checkbox(task["text"], value=task["done"], key=checkbox_key)
                if is_done != task["done"]:
                    previous_done = task["done"]
                    st.session_state.tasks[index]["done"] = is_done
                    try:
                        save_tasks_to_file(st.session_state.tasks)
                        st.rerun()
                    except OSError as error:
                        st.session_state.tasks[index]["done"] = previous_done
                        st.error(f"todos.json の保存に失敗しました: {error}")

            with delete_col:
                if st.button("削除", key=delete_key):
                    deleted_task = st.session_state.tasks.pop(index)
                    try:
                        save_tasks_to_file(st.session_state.tasks)
                        st.rerun()
                    except OSError as error:
                        st.session_state.tasks.insert(index, deleted_task)
                        st.error(f"todos.json の保存に失敗しました: {error}")
else:
    st.info("タスクはまだありません。")
