THROTTLING_SLEEP_TIME = 5

# Messages types
VOICE_TYPE = 'voice'
TEXT_TYPE = 'text'

# Message keys
COMMAND_KEY = 'command'
MENU_REPLAY_KEYBOARD_KEY = 'menu_replay_keyboard'
SCHEDULE_MESSAGE_KEY = 'schedule_message'
CHAT_GPT_MESSAGE_KEY = 'chat_gpt_message'
INVALID_MESSAGE_KEY = 'invalid_messages'

# Callback keys
CHAT_GPT_INLINE_KEYBOARD_KEY = 'chat_gpt_inline_keyboard'
SCHEDULE_INLINE_KEYBOARD_KEY = 'schedule_inline_keyboard'

RATE_LIMIT_DICT = {
    COMMAND_KEY: 2,
    MENU_REPLAY_KEYBOARD_KEY: 0.5,
    SCHEDULE_MESSAGE_KEY: 1,
    SCHEDULE_INLINE_KEYBOARD_KEY: 1,
    CHAT_GPT_INLINE_KEYBOARD_KEY: 1,
    INVALID_MESSAGE_KEY: 2,
    CHAT_GPT_MESSAGE_KEY: 5
}
