from helpers import copy_files
from markdown import generate_pages_recursive
import sys


def main() -> None:
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_files("./static", "./docs", first_iteration = True)
    generate_pages_recursive("./content", "template.html", "./docs", basepath)


if __name__ == "__main__":
    main()
