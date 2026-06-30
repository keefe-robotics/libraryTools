"""
Destiny MARC Builder

Program entry point.
"""

from config import load_settings


def main():
    settings = load_settings()
    print("Destiny MARC Builder")
    print(settings)


if __name__ == "__main__":
    main()
