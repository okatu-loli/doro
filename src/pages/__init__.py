import os


def get_page(name: str) -> str:
    pages = os.listdir(os.path.dirname(__file__))
    if name in pages:
        with open(
            os.path.join(os.path.dirname(__file__), name), "r", encoding="utf-8"
        ) as f:
            return f.read()
    raise FileNotFoundError(f"Page '{name}' not found in pages directory.")
