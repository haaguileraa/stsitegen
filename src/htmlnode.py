
class HTMLNode():
    def __init__(self, 
                 tag: str | None = None, 
                 value: str | None = None, 
                 children: list["HTMLNode"] | None = None, 
                 props: dict[str, str] | None = None
                 ) -> None:

        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list["HTMLNode"] | None = children
        self.props: dict[str, str] | None = props

    def to_html(self) -> None:
        raise NotImplementedError("method to_html not yet implemented")

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        formatted_props: list[str] = []
        for key, value in self.props.items():
            formatted_props.append(f" {key}=\"{value}\"")
        return "".join(formatted_props)

    def __repr__(self) -> str: 
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
