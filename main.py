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
from src.theme.models.wrong_answer import WrongAnswer
from src.theme.models.question_true_answers import QuestionTrueAnswer
from src.theme.models.user_test_progress import UserTestProgress
from src.shop.models.product import Product
from src.shop.models.cart_product import CartProduct
from src.shop.models.cart import Cart


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("+Tables.")
    tests_data = {
        "Основные слова и фразы": {
            "Изучаем легкие слова": [
                {"text": "Как по-английски 'привет'?", "answers": ["Hello", "Bye", "Good morning"], "correct": "Hello",
                 "points": 1},
                {"text": "Выберите правильный перевод слова 'кошка'.", "answers": ["Dog", "Cat", "Mouse"],
                 "correct": "Cat", "points": 2},
                {"text": "Что означает фраза 'Thank you'?", "answers": ["Пожалуйста", "Извини", "Спасибо"],
                 "correct": "Спасибо", "points": 2},
                {"text": "Как сказать 'пока' по-английски?", "answers": ["Good night", "Goodbye", "See you"],
                 "correct": "Goodbye", "points": 1},
                {"text": "Как перевести слово 'яблоко'?", "answers": ["Banana", "Cherry", "Apple"], "correct": "Apple",
                 "points": 3},
                {"text": "Что мы скажем, если хотим приглашать друзей поиграть?",
                 "answers": ["Let's play!", "Sit down!", "Go away!"], "correct": "Let's play!", "points": 3},
                {"text": "Какое слово означает 'дом'?", "answers": ["House", "Car", "School"], "correct": "House",
                 "points": 2},
                {"text": "Как на английском языке будет 'мама'?", "answers": ["Mother", "Sister", "Father"],
                 "correct": "Mother", "points": 2},
                {"text": "Как перевести фразу 'Как дела?'?",
                 "answers": ["What is your name?", "How are you?", "Where are you from?"], "correct": "How are you?",
                 "points": 3},
                {"text": "Как по-английски 'это' в контексте предмета?", "answers": ["That", "This", "These"],
                 "correct": "This", "points": 2},
            ],
            "Изучаем новые слова": [
                {"text": "Как будет 'да' по-английски?", "answers": ["Yes", "No", "Maybe"], "correct": "Yes",
                 "points": 1},
                {"text": "Переведите слово 'собака'.", "answers": ["Cat", "Dog", "Bird"], "correct": "Dog",
                 "points": 2},
                {"text": "Как перевести 'я люблю тебя'?", "answers": ["I miss you", "I love you", "I see you"],
                 "correct": "I love you", "points": 3},
                {"text": "Как сказать 'спасибо' по-английски?", "answers": ["Sorry", "Thank you", "Yes, please"],
                 "correct": "Thank you", "points": 2},
                {"text": "Как перевести слово 'школа'?", "answers": ["Office", "Playground", "School"],
                 "correct": "School", "points": 3},
                {"text": "Что означает фраза 'Good morning'?", "answers": ["Доброе утро", "Спокойной ночи", "Привет"],
                 "correct": "Доброе утро", "points": 2},
                {"text": "Как будет 'стол' на английском?", "answers": ["Chair", "Table", "Sofa"], "correct": "Table",
                 "points": 3},
                {"text": "Как спросить 'где это?' по-английски?",
                 "answers": ["Where is it?", "What is it?", "How is it?"], "correct": "Where is it?", "points": 3},
                {"text": "Как сказать 'я голоден'?", "answers": ["I am tired", "I am hungry", "I am happy"],
                 "correct": "I am hungry", "points": 2},
                {"text": "Что означает фраза 'Please sit down'?",
                 "answers": ["Пожалуйста, встаньте", "Пожалуйста, сядьте", "Пожалуйста, идите"],
                 "correct": "Пожалуйста, сядьте", "points": 3},
            ]
        },
        "Животные": {
            "Знакомимся с животными": [
                {"text": "Как звучит слово 'кот' на английском?", "answers": ["Dog", "Cat", "Rabbit"], "correct": "Cat",
                 "points": 2},
                {"text": "Какое из этих животных летающее?", "answers": ["Elephant", "Tiger", "Bird"],
                 "correct": "Bird", "points": 2},
                {"text": "Как называют 'собака' на английском?", "answers": ["Cat", "Dog", "Fish"], "correct": "Dog",
                 "points": 3},
                {"text": "Какое животное является домашним?", "answers": ["Lion", "Horse", "Hamster"],
                 "correct": "Hamster", "points": 3},
                {"text": "Какой звук издает корова?", "answers": ["Meow", "Moo", "Bark"], "correct": "Moo",
                 "points": 2},
                {"text": "Какое из этих животных обитает в воде?", "answers": ["Shark", "Monkey", "Eagle"],
                 "correct": "Shark", "points": 3},
                {"text": "Как сказать 'жираф' на английском?", "answers": ["Giraffe", "Rhino", "Zebra"],
                 "correct": "Giraffe", "points": 2},
                {"text": "Какое животное самое большое на Земле?", "answers": ["Blue whale", "Elephant", "Giraffe"],
                 "correct": "Blue whale", "points": 4},
                {"text": "Какое слово означает 'бегемот'?", "answers": ["Hippo", "Crocodile", "Bear"],
                 "correct": "Hippo", "points": 3},
                {"text": "Кого называют 'королевой джунглей'?", "answers": ["Tiger", "Lion", "Cheetah"],
                 "correct": "Lion", "points": 4},
            ]
        }
    }
    async with async_session() as session:
        async with session.begin():# Используем `begin()`, чтобы не делать `commit()` вручную
            begun = 0
            for theme_name, tests in tests_data.items():
                # Создаем тему
                theme = Theme(name=theme_name,points_to_access=begun)
                session.add(theme)
                await session.flush()  # Получаем `theme.id`

                for test_name, questions in tests.items():
                    # Создаем тест
                    test = Test(name=test_name, theme_id=theme.id)
                    session.add(test)
                    await session.flush()  # Получаем `test.id`

                    for q_data in questions:
                        # Создаем вопрос
                        question = Question(text=q_data["text"], points=q_data["points"])
                        begun +=q_data["points"]*1/2
                        session.add(question)
                        await session.flush()  # Получаем `question.id`

                        # Создаем список id для ответов
                        answer_ids = []
                        for ans_text in q_data["answers"]:
                            answer = Answer(text=ans_text)
                            session.add(answer)
                            await session.flush()  # Получаем `answer.id`
                            answer_ids.append(answer.id)

                            # Если это правильный ответ, то добавляем его в `QuestionTrueAnswer`
                            if ans_text == q_data["correct"]:
                                true_answer = QuestionTrueAnswer(question_id=question.id, answer_id=answer.id)
                                session.add(true_answer)

                            # Если это неправильный ответ, то добавляем его в `WrongAnswer`
                            else:
                                wrong_answer = WrongAnswer(question_id=question.id, answer_id=answer.id)
                                session.add(wrong_answer)

                        # Добавляем вопрос в тест
                        test_question = TestQuestion(test_id=test.id, question_id=question.id)
                        session.add(test_question)

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
