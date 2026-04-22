Структура проекту:
tutor-finder/
├── backend/
│   ├── app/
│   │   ├── api.py           # Усі ендпоінти (Subjects, Tutors, Bookings)
│   │   ├── database.py      # Налаштування БД та SQLAlchemy моделі
│   │   ├── schemas.py       # Pydantic моделі (валідація даних)
│   │   └── main.py          # Ініціалізація FastAPI та підключення CORS
│   ├── tests/
│   │   └── test_main.py     # Unit-тести для всього бекенду
├── frontend/
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/script.js     # Уся логіка (fetch + UI)
│   ├── index.html           # Головна та Пошук
│   └── tests/
│       └── ui.test.js       # Прості тести логіки JS
├── docker-compose.yml       # Запуск Postgres + Backend
├── .gitignore
│── requirements.txt         # Залежності (fastapi, sqlalchemy, psycopg2-binary, pytest)
│── .env                     # Налаштування підключення до БД
└── README.md