def get_safe_name(name: str) -> str:
    """Get a safe name that could be used as a file name for the given name.
    '*' will be replaced with '-' and the rest will be replaced with '_'. (For better compatibility with PSDToolKit (well-known AviUtl Plugin))

    Parameters
    ----------
    name : str
        The name to get a safe name for.

    Returns
    -------
    str
        The safe name.
    """
    return name.translate(str.maketrans('*\\/:?"<>| ', "-_________"))
