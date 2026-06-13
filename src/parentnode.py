from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, 
                 tag: str,
                 children: list["HTMLNode"],
                 props: dict[str, str] | None = None) -> None:
        super().__init__(tag = tag,
                   value = None,
                   children = children,
                   props = props)

    def to_html(self) -> str:
        if self.tag is None or self.tag == "":
            raise ValueError("Member 'tag' must have a value")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Member 'children' missing")
        children_html: list[str] = [child.to_html() for child in self.children]
        return f"<{self.tag}{self.props_to_html()}>{"".join(children_html)}</{self.tag}>"
