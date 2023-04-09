from aiogram.dispatcher.filters.state import StatesGroup, State


class ScheduleMenuStatesGroup(StatesGroup):
    student_schedule = State()
    lecturer_schedule = State()
