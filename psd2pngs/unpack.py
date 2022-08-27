from collections.abc import Iterable, Mapping


def isnamedtupleinstance(obj: object) -> bool:
    """Check if the given object is a namedtuple.

    Parameters
    ----------
    x : object
        object to check.

    Returns
    -------
    bool
        True if the given object is a namedtuple.
    """
    _type = type(obj)
    bases = _type.__bases__
    if len(bases) != 1 or bases[0] != tuple:
        return False
    fields = getattr(_type, "_fields", None)
    if not isinstance(fields, tuple):
        return False
    return all(type(i) == str for i in fields)


def unpack_nested_namedtuple(obj: object) -> object:
    """Unpack a nested namedtuple to a dict.

    Parameters
    ----------
    obj : object
        object to unpack.

    Returns
    -------
    object
        Unpacked object.
    """
    if isnamedtupleinstance(obj):
        assert hasattr(obj, "_asdict")
        return {key: unpack_nested_namedtuple(value) for key, value in obj._asdict().items()}
    elif isinstance(obj, Mapping):
        return {key: unpack_nested_namedtuple(value) for key, value in obj.items()}
    elif isinstance(obj, Iterable) and not isinstance(obj, str):
        if hasattr(obj, "__init__"):
            return type(obj)([unpack_nested_namedtuple(value) for value in obj])
        else:
            return [unpack_nested_namedtuple(value) for value in obj]
    else:
        return obj
