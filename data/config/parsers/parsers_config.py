from fake_useragent import UserAgent


ua = UserAgent()
HEADERS = {
    'user-agent': ua.random
}

COUNT_SHOW_ALLEGED_TARGETS_THRESHOLD = 15

STUDENT_TARGET = 'student'
LECTURER_TARGET = 'lecturer'

STUDENT_TABLE_HEADERS = [
    'Дата',
    'Порядок',
    '🕑 Время',
    '📚 Предмет',
    '👩‍🏫 Преподаватель',
    '🚪 Аудитория',
    'Свободные аудитории'
]
LECTURER_TABLE_HEADERS = [
    'Дата',
    'Порядок',
    '🕑 Время',
    '📚 Предмет',
    '👨‍🎓 Группа',
    '🚪 Аудитория',
    'Свободные аудитории'
]
