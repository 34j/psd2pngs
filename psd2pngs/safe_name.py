def get_safe_name(name: str):
    return name.translate(str.maketrans('*\\/:?"<>| ', '-_________'))