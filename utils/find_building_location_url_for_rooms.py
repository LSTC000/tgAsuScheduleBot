from data.config import BUILDINGS_LOCATION_URL_DICT


def find_building_location_url_for_rooms(audience: str) -> str:
    '''
    :param audience: Room name.
        Example: '401 Л'.
    :return: Room name with building location url.
        Example: '<a href="{housing_location_url}" title="корпус"><b>401 Л</b></a>.'.
    '''

    lower_audience = audience.lower()

    if 'сок' in lower_audience:
        return f'<a href="{BUILDINGS_LOCATION_URL_DICT["сок"]}" title="корпус"><b>{audience}</b></a>.'

    if 'лыж' in lower_audience:
        return f'<a href="{BUILDINGS_LOCATION_URL_DICT["лыж.база"]}" title="корпус"><b>{audience}</b></a>.'

    split_lower_audience = lower_audience.split()

    for key in list(BUILDINGS_LOCATION_URL_DICT.keys())[:-2]:
        if key in split_lower_audience:
            return f'<a href="{BUILDINGS_LOCATION_URL_DICT[key]}" title="корпус"><b>{audience}</b></a>.'

    return audience
