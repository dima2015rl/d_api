import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from starlette.middleware.cors import CORSMiddleware

from database import engine, Base, async_session
from src.routers import main_router
from src.auth.models import User
from src.theme.models.theme import Theme
from src.theme.models.test import Test
from src.theme.models.question import Question
from src.theme.models.test_questions import TestQuestion
from src.theme.models.answers import Answer
from src.theme.models.question_answers import QuestionAnswer


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("+Tables.")
    questions_data = [
        {"question": "Как переводится слово 'apple'?", "answers": ["Banana", "Orange", "Apple", "Pear"],
         "correct": "Apple"},
        {"question": "Как переводится слово 'book'?", "answers": ["Notebook", "Book", "Magazine", "Paper"],
         "correct": "Book"},
        {"question": "Какой из вариантов переведен как 'собака'?", "answers": ["Dog", "Cat", "Bird", "Fish"],
         "correct": "Dog"},
        {"question": "Какой из вариантов переводится как 'молоко'?", "answers": ["Water", "Milk", "Bread", "Cheese"],
         "correct": "Milk"},
        {"question": "Как переводится фраза 'Good morning'?",
         "answers": ["Доброе утро", "Добрый вечер", "Здравствуйте", "Привет"], "correct": "Доброе утро"},
        {"question": "Как переводится фраза 'How are you?'",
         "answers": ["Как дела?", "Где ты?", "Что нового?", "Как ты?"], "correct": "Как дела?"},
        {"question": "Что означает фраза 'I am hungry'?", "answers": ["Я хочу пить", "Я устал", "Я голоден", "Я весел"],
         "correct": "Я голоден"},
        {"question": "Какой из вариантов означает 'пожалуйста'?",
         "answers": ["Thank you", "Sorry", "Please", "Excuse me"], "correct": "Please"},
        {"question": "Что означает слово 'house'?", "answers": ["Квартира", "Дом", "Мебель", "Улица"],
         "correct": "Дом"},
        {"question": "Как переводится слово 'friend'?", "answers": ["Друг", "Сестра", "Мама", "Брат"],
         "correct": "Друг"},
        {"question": "Как переводится фраза 'See you later'?",
         "answers": ["Увидимся позже", "До свидания", "Привет", "Спокойной ночи"], "correct": "Увидимся позже"},
        {"question": "Какой из вариантов переводится как 'сегодня'?",
         "answers": ["Tomorrow", "Yesterday", "Today", "Always"], "correct": "Today"},
        {"question": "Как переводится фраза 'I love you'?",
         "answers": ["Я тебя ненавижу", "Я люблю тебя", "Я боюсь тебя", "Ты мне нравишься"], "correct": "Я люблю тебя"},
        {"question": "Какой из вариантов переводится как 'солнце'?", "answers": ["Moon", "Star", "Sun", "Cloud"],
         "correct": "Sun"},
        {"question": "Как переводится фраза 'What time is it?'",
         "answers": ["Сколько времени?", "Как ты?", "Где ты?", "Когда это?"], "correct": "Сколько времени?"},
        {"question": "Какой из вариантов переводится как 'яблоко'?", "answers": ["Pear", "Orange", "Apple", "Banana"],
         "correct": "Apple"},
        {"question": "Какой из вариантов означает 'погода'?", "answers": ["Weather", "Climate", "Time", "Season"],
         "correct": "Weather"},
        {"question": "Как переводится фраза 'Where is the bathroom?'",
         "answers": ["Где находится ресторан?", "Где находится баня?", "Где находится туалет?", "Где находится стол?"],
         "correct": "Где находится туалет?"},
        {"question": "Какой из вариантов переводится как 'утро'?", "answers": ["Night", "Morning", "Noon", "Evening"],
         "correct": "Morning"},
        {"question": "Что означает слово 'goodbye'?", "answers": ["Привет", "Пожалуйста", "До свидания", "Извините"],
         "correct": "До свидания"},
    ]

    # Уникальные ответы
    unique_answers = set()
    questions = []
    async with async_session() as session:
        async with session.begin():
            # Создаем тему
            theme = Theme(name="Основы английского", description="Тесты на базовые знания английского языка")
            session.add(theme)
            theme1 = Theme(name="Основы английского1", description="Тесты на базовые знания английского языка1")
            session.add(theme1)
            session.add(theme)
            await session.flush()  # Получаем ID темы

            # Создаем тесты
            test1 = Test(theme_id=theme.id,name="Тест_1")
            test2 = Test(theme_id=theme.id, name="Тест_2")
            session.add_all([test1, test2])
            await session.flush()  # Получаем ID тестов

            # Уникальные ответы
            unique_answers = set()
            for q in questions_data:
                unique_answers.update(q["answers"])

            # Добавляем уникальные ответы
            answers_id_map = {}
            for answer_text in unique_answers:
                answer = Answer(text=answer_text)
                session.add(answer)
                await session.flush()  # Получаем ID ответа
                answers_id_map[answer_text] = answer.id

            # Разделяем вопросы на два теста
            questions_test1 = questions_data[:10]
            questions_test2 = questions_data[10:]

            # Добавляем вопросы для первого теста
            for q in questions_test1:
                question = Question(text=q["question"])
                session.add(question)
                await session.flush()

                # Привязываем вопрос к тесту
                test_question = TestQuestion(test_id=test1.id, question_id=question.id)
                session.add(test_question)

                # Привязываем правильный ответ
                correct_answer_id = answers_id_map[q["correct"]]
                qa = QuestionAnswer(question_id=question.id, answer_id=correct_answer_id)
                session.add(qa)

            # Добавляем вопросы для второго теста
            for q in questions_test2:
                question = Question(text=q["question"])
                session.add(question)
                await session.flush()

                # Привязываем вопрос к тесту
                test_question = TestQuestion(test_id=test2.id, question_id=question.id)
                session.add(test_question)

                # Привязываем правильный ответ
                correct_answer_id = answers_id_map[q["correct"]]
                qa = QuestionAnswer(question_id=question.id, answer_id=correct_answer_id)
                session.add(qa)

            print("Тесты, вопросы и ответы успешно добавлены.")
    yield
    await engine.dispose()
    print("-Tables.")


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",  # Ваш фронтенд на React/Vue/другом фреймворке
    "http://127.0.0.1:3000",  # На случай, если используется 127.0.0.1
]

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешенные источники
    allow_credentials=True,  # Разрешение на отправку cookies
    allow_methods=["*"],  # Разрешенные HTTP-методы (GET, POST, PUT, DELETE и т. д.)
    allow_headers=["*"],  # Разрешенные заголовки (Authorization, Content-Type и т. д.)
)
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
