from loader import voice_cache

from ner.students.extractor import NumberExtractor
from natasha import MorphVocab


async def text_to_student_group_convert(text: str, target: str) -> str:
    '''
    :param text: Text from the voice message.
        Example: 'сто сорок тире два'
    :param target: STUDENT_TARGET from data/config/parser/config
    :return: A string with a student group or room number.
        Example: '140-2'
    '''

    key_cache = text
    # Checking for a request in the voice_cache
    if key_cache in voice_cache:
        return voice_cache[key_cache]

    text = text.replace('точка', '.').replace('тире', '-').replace('слэш', '/')

    morph = MorphVocab()

    text = NumberExtractor(morph=morph).replace_groups(text).replace(' ', '')
    voice_cache[key_cache] = text

    return text
