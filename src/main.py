from helpers import copy_files
from markdown import generate_pages_recursive
import sys


def main() -> None:
    basepath = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "" else "/"
    copy_files("./static", "./docs", first_iteration = True)
    generate_pages_recursive(basepath, "template.html", "./docs")


if __name__ == "__main__":
    main()
