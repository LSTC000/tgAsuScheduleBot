import calendar
from datetime import datetime, timedelta

from data.config import RU_MONTH_NAME
from data.config import CALLBACK_DATA_GET_CALENDAR_SCHEDULE_SEPARATOR

from data.messages import CALLBACK_DATA_KEY_ERROR_MESSAGE

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineCalendar:
    async def start_calendar(self, year: int, month: int, state: FSMContext) -> InlineKeyboardMarkup:
        # Create a dictionary in the user memory storage for storing the year and month
        async with state.proxy() as data:
            data['inline_calendar'] = {
                'year': year,
                'month': month
            }

        inline_kb = InlineKeyboardMarkup(row_width=7)
        ignore_callback = "IGNORE"

        # First row - Month and Year
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            text="<<",
            callback_data="PREV-YEAR"
        ))
        inline_kb.insert(InlineKeyboardButton(
            text=f'{RU_MONTH_NAME[calendar.month_name[month]]} {str(year)}',
            callback_data=ignore_callback
        ))
        inline_kb.insert(InlineKeyboardButton(
            text=">>",
            callback_data="NEXT-YEAR"
        ))

        # Second row - Week Days
        inline_kb.row()
        for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
            inline_kb.insert(InlineKeyboardButton(text=day, callback_data=ignore_callback))

        # Calendar rows - Days of month
        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            inline_kb.row()
            for day in week:
                if day == 0:
                    inline_kb.insert(InlineKeyboardButton(text=" ", callback_data=ignore_callback))
                    continue
                inline_kb.insert(InlineKeyboardButton(
                    # Callback data looks like this: DAY_date
                    # DAY_ is CALLBACK_DATA_GET_CALENDAR_SCHEDULE_SEPARATOR
                    # date is the date selected by the user in the format datetime
                    text=str(day), callback_data=CALLBACK_DATA_GET_CALENDAR_SCHEDULE_SEPARATOR + str(day)
                ))

        # Last row - Buttons
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            text="<", callback_data="PREV-MONTH"
        ))
        inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
        inline_kb.insert(InlineKeyboardButton(
            text=">", callback_data="NEXT-MONTH"
        ))

        return inline_kb

    async def process_selection(self, callback: types.CallbackQuery, callback_data: str, state: FSMContext) -> tuple:
        return_data = (False, None)

        try:
            async with state.proxy() as data:
                year = int(data['inline_calendar']['year'])
                month = int(data['inline_calendar']['month'])
                temp_date = datetime(year, month, 1)
            # IGNORE is callback data in CALLBACK_DATA_GET_CALENDAR_SCHEDULE from data/config/keyboards/config
            if callback_data == "IGNORE":
                await callback.answer(cache_time=60)
            # CALLBACK_DATA_GET_CALENDAR_SCHEDULE_SEPARATOR is separator from data/config/keyboards/config
            if CALLBACK_DATA_GET_CALENDAR_SCHEDULE_SEPARATOR in callback_data:
                async with state.proxy() as data:
                    await callback.message.delete_reply_markup()
                    data['calendar_message_id'] = None

                return_data = True, datetime(
                    year,
                    month,
                    int(callback_data.split(CALLBACK_DATA_GET_CALENDAR_SCHEDULE_SEPARATOR)[-1])
                )
            # PREV-YEAR is callback data in CALLBACK_DATA_GET_CALENDAR_SCHEDULE from data/config/keyboards/config
            if callback_data == "PREV-YEAR":
                prev_date = temp_date - timedelta(days=365)
                await callback.message.edit_reply_markup(
                    await self.start_calendar(year=int(prev_date.year), month=int(prev_date.month), state=state)
                )
            # NEXT-YEAR is callback data in CALLBACK_DATA_GET_CALENDAR_SCHEDULE from data/config/keyboards/config
            if callback_data == "NEXT-YEAR":
                next_date = temp_date + timedelta(days=365)
                await callback.message.edit_reply_markup(
                    await self.start_calendar(year=int(next_date.year), month=int(next_date.month), state=state)
                )
            # PREV-MONTH is callback data in CALLBACK_DATA_GET_CALENDAR_SCHEDULE from data/config/keyboards/config
            if callback_data == "PREV-MONTH":
                prev_date = temp_date - timedelta(days=1)
                await callback.message.edit_reply_markup(
                    await self.start_calendar(year=int(prev_date.year), month=int(prev_date.month), state=state)
                )
            # NEXT-MONTH is callback data in CALLBACK_DATA_GET_CALENDAR_SCHEDULE from data/config/keyboards/config
            if callback_data == "NEXT-MONTH":
                next_date = temp_date + timedelta(days=31)
                await callback.message.edit_reply_markup(
                    await self.start_calendar(year=int(next_date.year), month=int(next_date.month), state=state)
                )
        except KeyError:
            await callback.answer(text=CALLBACK_DATA_KEY_ERROR_MESSAGE)

        return return_data
