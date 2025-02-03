#!/usr/bin/env python
import os


def file_requirements():
    """
    Reads the file requirements.txt and checks if it exists
    If it does not exist, it creates it with the command pip freeze > requirements.txt
    """

    try:
        with open("requirements.txt", "r"):
            return 0
    except FileNotFoundError:
        req = "pipreqs"
        print("File requirements.txt not found")
        print("Make pipreqs")
        os.system(req)
        print("New file requirements.txt created")
        print("Run git add requirements.txt and commit again")
        return 1


def main():
    """
    Calls the function file_requirements()
    """
    raise SystemExit(file_requirements())


if __name__ == "__main__":
    """
    Calls the function file_requirements()
    """
    raise SystemExit(main())
