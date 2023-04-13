def rate_limit(limit: int, key: str):
    '''
    :param limit: The time that must pass between two messages of a user of the same key.
    :param key: Key for different types of messages. You can find them all in data/config/middlewares/config.
    :return: Decorator.
    '''

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator
