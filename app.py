import os
import sqlite3
import tempfile
from pathlib import Path

from flask import Flask, abort, flash, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
DATABASE = Path(os.environ.get("NOTES_DATABASE", BASE_DIR / "notes.db"))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-notes-secret")


def get_db_connection():
    try:
        connection = sqlite3.connect(DATABASE)
    except sqlite3.OperationalError:
        fallback_dir = Path(tempfile.gettempdir()) / "notes_app"
        fallback_dir.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(fallback_dir / "notes.db")

    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def get_note(note_id):
    with get_db_connection() as connection:
        note = connection.execute(
            "SELECT * FROM notes WHERE id = ?",
            (note_id,),
        ).fetchone()

    if note is None:
        abort(404)

    return note


@app.route("/")
def index():
    with get_db_connection() as connection:
        notes = connection.execute(
            "SELECT * FROM notes ORDER BY updated_at DESC, id DESC"
        ).fetchall()

    return render_template("index.html", notes=notes)


@app.route("/notes/<int:note_id>")
def note_detail(note_id):
    note = get_note(note_id)
    return render_template("note_detail.html", note=note)


@app.route("/notes/new", methods=["GET", "POST"])
def create_note():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Заполните заголовок и текст заметки.", "error")
            return render_template(
                "note_form.html",
                mode="create",
                note={"title": title, "content": content},
            )

        with get_db_connection() as connection:
            connection.execute(
                "INSERT INTO notes (title, content) VALUES (?, ?)",
                (title, content),
            )

        flash("Заметка добавлена.", "success")
        return redirect(url_for("index"))

    return render_template(
        "note_form.html",
        mode="create",
        note={"title": "", "content": ""},
    )


@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
def edit_note(note_id):
    note = get_note(note_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Заполните заголовок и текст заметки.", "error")
            return render_template(
                "note_form.html",
                mode="edit",
                note={"id": note_id, "title": title, "content": content},
            )

        with get_db_connection() as connection:
            connection.execute(
                """
                UPDATE notes
                SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (title, content, note_id),
            )

        flash("Заметка обновлена.", "success")
        return redirect(url_for("note_detail", note_id=note_id))

    return render_template("note_form.html", mode="edit", note=note)


@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def delete_note(note_id):
    get_note(note_id)

    with get_db_connection() as connection:
        connection.execute("DELETE FROM notes WHERE id = ?", (note_id,))

    flash("Заметка удалена.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
