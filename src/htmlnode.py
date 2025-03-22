class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return (f"tag = {self.tag}\n"
                f"value = {self.value}\n"
                f"children = {self.children}\n"
                f"props = {self.props}")
      
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        if value is None or value.strip() == "":
            print(f"Warning: Creating a LeafNode with an empty or None value. Tag: {tag}, Props: {props}")
            self.value = ""  # Default to an empty string instead of raising an exception

    def to_html(self):
        if self.tag is None:
            return self.value or ""
        
        if self.value is None or self.value == "":
            if self.tag in ["img", "input", "br", "hr"]:
                props_html = self.props_to_html()
                return f"<{self.tag}{props_html}>"
            else:
                raise ValueError("LeafNode value cannot be empty or None")
        
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
    
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        if not children:
            print(f"Warning: Creating a ParentNode with no children. Tag: {tag}, Props: {props}")
            self.children = [LeafNode(None, "")]  # Default to an empty child
    
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode requires a tag")
        if not self.children:
            # If there are no children, return a self-closing tag or an empty tag
            return f"<{self.tag}></{self.tag}>"

        node_to_html = f"<{self.tag}"
        if self.props:
            node_to_html += self.props_to_html()
        node_to_html += ">"

        for child in self.children:
            # Check if the child is a TextNode from the textnode module
            if hasattr(child, 'text_type') and hasattr(child, 'text'):
                # It's a TextNode, just add its text directly
                node_to_html += child.to_html()
            else:
                # It's an HTMLNode, call its to_html method
                node_to_html += child.to_html()

        return node_to_html + f"</{self.tag}>"