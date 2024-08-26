from aiogram.dispatcher.filters.state import StatesGroup, State

class RegistrationStates(StatesGroup):
    language = State()
    region = State()


###sozlamala til
class Sozlamalar(StatesGroup):
    language = State()


class CreatePost(StatesGroup):
    choose_post_type = State()
    post_title_link = State()
    send_buttons = State()

class SavePosts(StatesGroup):
    postname = State()