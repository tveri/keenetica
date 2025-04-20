def apply(filter):
    """
    this is decorator that checks 'apply'
    argument in kwargs and applies filter
    if apply is True or None
    """

    def wrapper(*args, **kwargs):
        if kwargs.get("apply", True):
            return filter(*args, **kwargs)
        return {
            "processed_data": (
                data if (data := kwargs.get("data")) is not None else args[0]
            ),
            "stats": None,
        }

    return wrapper
