# Сайт-заметки

Простой CRUD-сайт на Flask + SQLite для хранения личных заметок.

## Возможности

- Создать, посмотреть, изменить и удалить заметку
- Сохранение данных в SQLite
- Валидация пустых полей
- Flash-сообщения после добавления, редактирования и удаления

## Установка и запуск

```bash
git clone https://github.com/beut99095-cyber/lesson.git
cd lesson
pip install -r requirements.txt
python app.py
```

Открыть в браузере: http://127.0.0.1:5000

## Структура проекта

```text
notes_app/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── note_form.html
│   └── note_detail.html
└── static/
    └── style.css
```

Файл `notes.db` создается автоматически при запуске приложения и не добавляется в Git.

## Технологии

- Python 3.11
- Flask 3.0
- SQLite

## Автор

Имя Фамилия, IT Step, 2026
