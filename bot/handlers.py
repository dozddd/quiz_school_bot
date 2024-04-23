from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message

import kb
import text
from que import *

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.message(F.text == "Начать")
@router.message(F.text == "Начать викторину")
async def menu(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.callback_query(F.data == "answer_yes")
async def categoria(callback: types.CallbackQuery):
    await callback.message.edit_text(text.categoria, reply_markup=kb.categoria)
    await callback.answer()


@router.callback_query(F.data == "answer_no")
async def no(callback: types.CallbackQuery):
    await callback.message.edit_text(text.no, reply_markup=None)
    await callback.answer()


@router.callback_query(F.data == "bio")
async def bio(callback: types.CallbackQuery):
    await callback.message.edit_text(text.bio_questions, reply_markup=kb.bio_questions)
    await callback.answer()


@router.callback_query(F.data == "his")
async def his(callback: types.CallbackQuery):
    await callback.message.edit_text(text.his_questions, reply_markup=kb.his_questions)
    await callback.answer()

@router.callback_query(F.data == "inf")
async def inf(callback: types.CallbackQuery):
    await callback.message.edit_text(text.inf_questions, reply_markup=kb.inf_questions)
    await callback.answer()


# ______________________________ Отсюда идет новый код ____________________________________
# Класс вопроса
# class Question:
#     def __init__(self, q_text: str, right_answer: str, incorrect_answers: list[str]):
#         self.q_text = q_text
#         self.right_answer = right_answer
#         self.incorrect_answers = incorrect_answers
#
#     def to_inline_keyboard(self, callback_data: str) -> InlineKeyboardMarkup:
#         """
#         Преобразовывает варианты ответа в inline клавиатуру
#
#         :param callback_data: префикс callback_data
#         :return:
#         """
#
#         # Каждый ответ занимает всю строку
#         # *[1, 2, 3] производит распаковку объектов в список
#         questions_btn = [
#             [InlineKeyboardButton(text=self.right_answer, callback_data=callback_data+"_right")],  # добавляет обозначение верного ответа
#             *[
#                 [InlineKeyboardButton(text=i, callback_data=callback_data+"_incorrect")]  # добавляет обозначение неверного ответа
#                 for i in self.incorrect_answers
#             ]
#         ]
#         # Перемешиваем варианты ответов
#         shuffle(questions_btn)
#         return InlineKeyboardMarkup(inline_keyboard=questions_btn)

#
# questions_rus_10 = [
#     Question("Вопрос 1", "Ответ 1", ["Ответ 2", "Ответ 3", "Ответ 4"]),
#     Question("Вопрос 2", "Ответ 1", ["Ответ 2", "Ответ 3", "Ответ 4"]),
#     Question("Вопрос 3", "Ответ 1", ["Ответ 2", "Ответ 3", "Ответ 4"]),
#     Question("Вопрос 4", "Ответ 1", ["Ответ 2", "Ответ 3", "Ответ 4"]),
#     Question("Вопрос 5", "Ответ 1", ["Ответ 2", "Ответ 3", "Ответ 4"]),
#     Question("Вопрос 6", "Ответ 1", ["Ответ 2", "Ответ 3", "Ответ 4"]),
#     Question("Вопрос 7", "Ответ 1", ["Ответ 2", "Ответ 3", "Ответ 4"]),
#     Question("Вопрос 8", "Ответ 1", ["Ответ 2", "Ответ 3", "Ответ 4"]),
#     Question("Вопрос 9", "Ответ 1", ["Ответ 2", "Ответ 3", "Ответ 4"]),
#     Question("Вопрос 10", "Ответ 1", ["Ответ 2", "Ответ 3", "Ответ 4"]),
# ]


"""
Хранилище набранных баллов

Формат данных:
{
    user_id: {
        "Выбранная викторина (rus_10)": Набрано баллов
    }
}
"""
user_score = {}

#биология 10

@router.callback_query(F.data == "bio_10")
async def bio(callback: types.CallbackQuery):
    # Берем первый вопрос из questions_rus_10
    shuffle(questions_bio_10)
    q = questions_bio_10[0]

    # Меняем текущее сообщение на вопрос и варианты ответа
    # В качестве префикса callback_data задаем строку вида "answer_предмет_количество-вопросов_номер-вопроса"
    await callback.message.edit_text(q.q_text, reply_markup=q.to_inline_keyboard("answer_bio_10_0"))
    await callback.answer()


# Отлавливаем все callback начинающиеся на answer_rus
@router.callback_query(F.func(lambda callback: "answer_bio_10" in callback.data))
async def bio(callback: types.CallbackQuery):
    # Парсим строку вида answer_rus_10_0_incorrect
    # incorrect добавляется автоматически, как признак неверного ответа (right - верного)
    cur_index = int(callback.data.split("_")[-2])
    user_id = callback.message.chat.id

    # Проверяем правильно ли ответил пользователь
    is_right = callback.data.split("_")[-1] == "right"
    if is_right:
        # Проверяем есть ли текущий прогресс (чтобы не получить ошибку)
        if user_id not in user_score:
            user_score[user_id] = {"bio_10": 0}

        # Добавляем балл
        user_score[user_id]["bio_10"] += 1

    # Берем следующий индекс вопроса
    next_index = cur_index + 1

    # Если вопросы закончились...
    if next_index >= len(questions_bio_10):
        # Выводим кол-во набранных баллов
        await callback.message.edit_text(
            f"Конец викторины!\nНабрано баллов: {user_score[user_id]['bio_10']}\nНажми /start или напиши 'Начать', чтобы начать заново.",
            reply_markup=None
        )
        # Обнуляем баллы для следующей викторины
        user_score[user_id]['bio_10'] = 0
        await callback.answer()
        return

    # Получаем следующий вопрос
    next_q = questions_bio_10[next_index]

    # Задаем этот вопрос
    await callback.message.edit_text(
        next_q.q_text,
        reply_markup=next_q.to_inline_keyboard(f"answer_bio_10_{next_index}")
    )
    await callback.answer()

#история 10
@router.callback_query(F.data == "his_10")
async def his(callback: types.CallbackQuery):
    # Берем первый вопрос из questions_rus_10
    shuffle(questions_his_10)
    q = questions_his_10[0]

    # Меняем текущее сообщение на вопрос и варианты ответа
    # В качестве префикса callback_data задаем строку вида "answer_предмет_количество-вопросов_номер-вопроса"
    await callback.message.edit_text(q.q_text, reply_markup=q.to_inline_keyboard("answer_his_10_0"))
    await callback.answer()


# Отлавливаем все callback начинающиеся на answer_rus
@router.callback_query(F.func(lambda callback: "answer_his_10" in callback.data))
async def his(callback: types.CallbackQuery):
    # Парсим строку вида answer_rus_10_0_incorrect
    # incorrect добавляется автоматически, как признак неверного ответа (right - верного)
    cur_index = int(callback.data.split("_")[-2])
    user_id = callback.message.chat.id

    # Проверяем правильно ли ответил пользователь
    is_right = callback.data.split("_")[-1] == "right"
    if is_right:
        # Проверяем есть ли текущий прогресс (чтобы не получить ошибку)
        if user_id not in user_score:
            user_score[user_id] = {"his_10": 0}

        # Добавляем балл
        user_score[user_id]["his_10"] += 1

    # Берем следующий индекс вопроса
    next_index = cur_index + 1

    # Если вопросы закончились...
    if next_index >= len(questions_his_10):
        # Выводим кол-во набранных баллов
        await callback.message.edit_text(
            f"Конец викторины!\nНабрано баллов: {user_score[user_id]['his_10']}",
            reply_markup=None
        )
        # Обнуляем баллы для следующей викторины
        user_score[user_id]['his_10'] = 0
        await callback.answer()
        return

    # Получаем следующий вопрос
    next_q = questions_his_10[next_index]

    # Задаем этот вопрос
    await callback.message.edit_text(
        next_q.q_text,
        reply_markup=next_q.to_inline_keyboard(f"answer_his_10_{next_index}")
    )
    await callback.answer()

#информатика 10

@router.callback_query(F.data == "inf_10")
async def inf(callback: types.CallbackQuery):
    # Берем первый вопрос из questions_rus_10
    shuffle(questions_inf_10)
    q = questions_inf_10[0]

    # Меняем текущее сообщение на вопрос и варианты ответа
    # В качестве префикса callback_data задаем строку вида "answer_предмет_количество-вопросов_номер-вопроса"
    await callback.message.edit_text(q.q_text, reply_markup=q.to_inline_keyboard("answer_inf_10_0"))
    await callback.answer()


# Отлавливаем все callback начинающиеся на answer_rus
@router.callback_query(F.func(lambda callback: "answer_inf_10" in callback.data))
async def inf(callback: types.CallbackQuery):
    # Парсим строку вида answer_rus_10_0_incorrect
    # incorrect добавляется автоматически, как признак неверного ответа (right - верного)
    cur_index = int(callback.data.split("_")[-2])
    user_id = callback.message.chat.id

    # Проверяем правильно ли ответил пользователь
    is_right = callback.data.split("_")[-1] == "right"
    if is_right:
        # Проверяем есть ли текущий прогресс (чтобы не получить ошибку)
        if user_id not in user_score:
            user_score[user_id] = {"inf_10": 0}

        # Добавляем балл
        user_score[user_id]["inf_10"] += 1

    # Берем следующий индекс вопроса
    next_index = cur_index + 1

    # Если вопросы закончились...
    if next_index >= len(questions_inf_10):
        # Выводим кол-во набранных баллов
        await callback.message.edit_text(
            f"Конец викторины!\nНабрано баллов: {user_score[user_id]['inf_10']}",
            reply_markup=None
        )
        # Обнуляем баллы для следующей викторины
        user_score[user_id]['inf_10'] = 0
        await callback.answer()
        return

    # Получаем следующий вопрос
    next_q = questions_inf_10[next_index]

    # Задаем этот вопрос
    await callback.message.edit_text(
        next_q.q_text,
        reply_markup=next_q.to_inline_keyboard(f"answer_inf_10_{next_index}")
    )
    await callback.answer()

#биология 15 работает!!!

@router.callback_query(F.data == "bio_15")
async def bio(callback: types.CallbackQuery):
    # Берем первый вопрос из questions_rus_10
    shuffle(questions_bio_15)
    q = questions_bio_15[0]

    # Меняем текущее сообщение на вопрос и варианты ответа
    # В качестве префикса callback_data задаем строку вида "answer_предмет_количество-вопросов_номер-вопроса"
    await callback.message.edit_text(q.q_text, reply_markup=q.to_inline_keyboard("answer_bio_15_0"))
    await callback.answer()


# Отлавливаем все callback начинающиеся на answer_rus
@router.callback_query(F.func(lambda callback: "answer_bio_15" in callback.data))
async def bio15(callback: types.CallbackQuery):
    # Парсим строку вида answer_rus_10_0_incorrect
    # incorrect добавляется автоматически, как признак неверного ответа (right - верного)
    cur_index = int(callback.data.split("_")[-2])
    user_id = callback.message.chat.id

    # Проверяем правильно ли ответил пользователь
    is_right = callback.data.split("_")[-1] == "right"
    if is_right:
        # Проверяем есть ли текущий прогресс (чтобы не получить ошибку)
        if user_id not in user_score:
            user_score[user_id] = {"bio_15": 0}

        # Добавляем балл
        user_score[user_id]["bio_15"] += 1

    # Берем следующий индекс вопроса
    next_index = cur_index + 1

    # Если вопросы закончились...
    if next_index >= len(questions_bio_15):
        # Выводим кол-во набранных баллов
        await callback.message.edit_text(
            f"Конец викторины!\nНабрано баллов: {user_score[user_id]['bio_15']}",
            reply_markup=None
        )
        # Обнуляем баллы для следующей викторины
        user_score[user_id]['bio_15'] = 0
        await callback.answer()
        return

    # Получаем следующий вопрос
    next_q = questions_bio_15[next_index]

    # Задаем этот вопрос
    await callback.message.edit_text(
        next_q.q_text,
        reply_markup=next_q.to_inline_keyboard(f"answer_bio_15_{next_index}")
    )
    await callback.answer()

# история 10
@router.callback_query(F.data == "his_15")
async def his(callback: types.CallbackQuery):
    # Берем первый вопрос из questions_rus_10
    shuffle(questions_his_15)
    q = questions_his_15[0]

    # Меняем текущее сообщение на вопрос и варианты ответа
    # В качестве префикса callback_data задаем строку вида "answer_предмет_количество-вопросов_номер-вопроса"
    await callback.message.edit_text(q.q_text, reply_markup=q.to_inline_keyboard("answer_his_15_0"))
    await callback.answer()


# Отлавливаем все callback начинающиеся на answer_rus
@router.callback_query(F.func(lambda callback: "answer_his_15" in callback.data))
async def his(callback: types.CallbackQuery):
    # Парсим строку вида answer_rus_10_0_incorrect
    # incorrect добавляется автоматически, как признак неверного ответа (right - верного)
    cur_index = int(callback.data.split("_")[-2])
    user_id = callback.message.chat.id

    # Проверяем правильно ли ответил пользователь
    is_right = callback.data.split("_")[-1] == "right"
    if is_right:
        # Проверяем есть ли текущий прогресс (чтобы не получить ошибку)
        if user_id not in user_score:
            user_score[user_id] = {"his_15": 0}

        # Добавляем балл
        user_score[user_id]["his_15"] += 1

    # Берем следующий индекс вопроса
    next_index = cur_index + 1

    # Если вопросы закончились...
    if next_index >= len(questions_his_15):
        # Выводим кол-во набранных баллов
        await callback.message.edit_text(
            f"Конец викторины!\nНабрано баллов: {user_score[user_id]['his_15']}",
            reply_markup=None
        )
        # Обнуляем баллы для следующей викторины
        user_score[user_id]['his_15'] = 0
        await callback.answer()
        return

    # Получаем следующий вопрос
    next_q = questions_his_15[next_index]

    # Задаем этот вопрос
    await callback.message.edit_text(
        next_q.q_text,
        reply_markup=next_q.to_inline_keyboard(f"answer_his_15_{next_index}")
    )
    await callback.answer()

#информатика 15

@router.callback_query(F.data == "inf_15")
async def inf(callback: types.CallbackQuery):
    # Берем первый вопрос из questions_rus_10
    shuffle(questions_inf_15)
    q = questions_inf_15[0]

    # Меняем текущее сообщение на вопрос и варианты ответа
    # В качестве префикса callback_data задаем строку вида "answer_предмет_количество-вопросов_номер-вопроса"
    await callback.message.edit_text(q.q_text, reply_markup=q.to_inline_keyboard("answer_inf_15_0"))
    await callback.answer()


# Отлавливаем все callback начинающиеся на answer_rus
@router.callback_query(F.func(lambda callback: "answer_inf_15" in callback.data))
async def inf(callback: types.CallbackQuery):
    # Парсим строку вида answer_rus_10_0_incorrect
    # incorrect добавляется автоматически, как признак неверного ответа (right - верного)
    cur_index = int(callback.data.split("_")[-2])
    user_id = callback.message.chat.id

    # Проверяем правильно ли ответил пользователь
    is_right = callback.data.split("_")[-1] == "right"
    if is_right:
        # Проверяем есть ли текущий прогресс (чтобы не получить ошибку)
        if user_id not in user_score:
            user_score[user_id] = {"inf_15": 0}

        # Добавляем балл
        user_score[user_id]["inf_15"] += 1

    # Берем следующий индекс вопроса
    next_index = cur_index + 1

    # Если вопросы закончились...
    if next_index >= len(questions_inf_15):
        # Выводим кол-во набранных баллов
        await callback.message.edit_text(
            f"Конец викторины!\nНабрано баллов: {user_score[user_id]['inf_15']}",
            reply_markup=None
        )
        # Обнуляем баллы для следующей викторины
        user_score[user_id]['inf_15'] = 0
        await callback.answer()
        return

    # Получаем следующий вопрос
    next_q = questions_inf_15[next_index]

    # Задаем этот вопрос
    await callback.message.edit_text(
        next_q.q_text,
        reply_markup=next_q.to_inline_keyboard(f"answer_inf_15_{next_index}")
    )
    await callback.answer()