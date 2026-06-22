from textnode import TextType, TextNode
from helpers import copy_files

def main() -> None:
    copy_files("./static", "./public", first_iteration = True)


if __name__ == "__main__":
    main()
