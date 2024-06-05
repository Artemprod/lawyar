from aiogram.fsm.state import State, StatesGroup


class FSMSummaryLode(StatesGroup):
    load_one_file = State()
    load_two_file = State()
    load_partaily = State()
    get_result = State()
