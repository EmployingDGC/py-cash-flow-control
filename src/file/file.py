import os as _os


def file_exists(
    path: str,
) -> bool:
    return _os.path.exists(path)
