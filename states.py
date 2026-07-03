from aiogram.fsm.state import State, StatesGroup

class GenerateImageStates(StatesGroup):
    waiting_for_prompt = State()
    waiting_for_style = State()
    waiting_for_size = State()

class ConvertImageStates(StatesGroup):
    waiting_for_image = State()
    waiting_for_format = State()

class ShortenURLStates(StatesGroup):
    waiting_for_url = State()
