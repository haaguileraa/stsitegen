from helpers import copy_files
from markdown import generate_pages_recursive


def main() -> None:
    copy_files("./static", "./public", first_iteration = True)
    generate_pages_recursive("./content", "template.html", "./public")


if __name__ == "__main__":
    main()
