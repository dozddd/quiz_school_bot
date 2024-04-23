from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = [
    [InlineKeyboardButton(text="📝Да", callback_data="answer_yes"),
    InlineKeyboardButton(text="❌Нет", callback_data="answer_no")],
]
categoria = [
  [InlineKeyboardButton(text="Биология", callback_data="bio"),
  InlineKeyboardButton(text="История", callback_data="his"),
   InlineKeyboardButton(text="Информатика", callback_data="inf")]
]
bio_questions = [
  [InlineKeyboardButton(text="10 вопросов", callback_data="bio_10"),
   InlineKeyboardButton(text="15 вопросов", callback_data="bio_15")]
]
his_questions = [
  [InlineKeyboardButton(text="10 вопросов", callback_data="his_10"),
   InlineKeyboardButton(text="15 вопросов", callback_data="his_15")]
]
inf_questions = [
  [InlineKeyboardButton(text="10 вопросов", callback_data="inf_10"),
   InlineKeyboardButton(text="15 вопросов", callback_data="inf_15")]
]

bio_questions = InlineKeyboardMarkup(inline_keyboard=bio_questions)
his_questions = InlineKeyboardMarkup(inline_keyboard=his_questions)
inf_questions = InlineKeyboardMarkup(inline_keyboard=inf_questions)
categoria = InlineKeyboardMarkup(inline_keyboard=categoria)
menu = InlineKeyboardMarkup(inline_keyboard=menu)
