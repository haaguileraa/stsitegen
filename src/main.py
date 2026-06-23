from helpers import copy_files
from markdown import generate_page
from textnode import TextType, TextNode


def main() -> None:
    copy_files("./static", "./public", first_iteration = True)
    generate_page("./content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
