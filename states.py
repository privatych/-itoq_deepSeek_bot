from aiogram.fsm.state import State, StatesGroup

class BroadcastState(StatesGroup):
    broadcast_message = State()
    confirm_message = State()

class UserStates(StatesGroup):
    waiting_for_prompt = State()
    waiting_for_image_prompt = State() 