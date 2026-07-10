# Streamlit TODO App

`streamlit` で作成したシンプルな TODO アプリです。

## 主な機能

- タスク追加（空入力と重複は警告）
- タスクごとの完了チェック（`st.checkbox`）
- タスクごとの削除ボタン
- 操作時の即時 UI 更新（`st.rerun()`）

## 起動方法

1. 依存関係をインストール

   ```bash
   pip install -r requirements.txt
   ```

2. アプリを起動

   ```bash
   streamlit run app.py
   ```

## 実装メモ

- タスクは `st.session_state.tasks` に `{"text": str, "done": bool}` 形式で保持します。
- 旧形式（文字列配列）のデータが残っている場合でも、起動時に互換変換して表示できます。
- 起動時に `todos.json`（`app.py` と同じディレクトリ）を読み込み、存在すれば `session_state` の初期値として復元します。
- タスクの追加・完了切り替え・削除のたびに、最新状態を `todos.json` へ自動保存します。
