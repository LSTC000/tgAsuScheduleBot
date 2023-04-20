from fake_useragent import UserAgent


ua = UserAgent()
REQUEST_HEADERS = {
    'user-agent': ua.random
}

COUNT_SHOW_ALLEGED_TARGETS_THRESHOLD = 15

STUDENT_TARGET = 'student'
LECTURER_TARGET = 'lecturer'

STUDENT_TABLE_HEADERS = [
    'date',
    'order',
    'time',
    'subject',
    'lecturer',
    'room',
    'free_rooms'
]
LECTURER_TABLE_HEADERS = [
    'date',
    'order',
    'time',
    'subject',
    'group',
    'room',
    'free_rooms'
]
