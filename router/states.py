from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    menu = State()
    categories = State()
    sub_categories = State()
    set_booking_day = State()
    set_booking_time = State()
    confirm_booking = State()
    cancel_booking = State()
    get_booking = State()
    get_help = State()

    switch_index = State()
    switch_index_read_index = State()
    switch_index_closest_category = State()
    switch_index_closest_subcategory = State()