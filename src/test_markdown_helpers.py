import unittest
from helpers import extract_markdown_images, extract_markdown_links
from markdown import extract_title

class TestMarkdownHelpers(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_no_image(self):
        matches = extract_markdown_images(
            "This is text with an wrong [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with ![this image](https://i.imgur.com/zjjcJKZ.png) and ![this other image](ressources/example.png)"
        )
        self.assertListEqual([("this image", "https://i.imgur.com/zjjcJKZ.png"), ("this other image", "ressources/example.png")], matches)

    def test_no_images_as_link(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This text has a [link](https://github.com)")
        self.assertListEqual([("link", "https://github.com")], matches)

    def test_extract_title(self):
        md: str = "\n# Hello"  
        self.assertEqual("Hello", extract_title(md))
        md = "# This is my title\n\nAnd this part shouldn't matter"
        self.assertEqual("This is my title", extract_title(md))
        wrong_format_func = lambda : extract_title("")
        self.assertRaises(ValueError, wrong_format_func)
        wrong_format_func = lambda : extract_title("\n## Test")
        self.assertRaises(ValueError, wrong_format_func)

if __name__ == "__main__":
    unittest.main()
