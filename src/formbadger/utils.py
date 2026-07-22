import re


def sanitize_names(names: str) -> str:
    return re.sub(r'[<>:"/\\\\|?*]', "_", names).strip(" .")
