

class HTMLNode():
    def __init__(self,tag = None,value = None, children = None,props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props 

    def to_html(self):
        raise NotImplementedError("to_html not implemented yet")
    
    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        props_string = ""
        for key, value in self.props.items():
            props_string = props_string + f' {key}="{value}"'
        return props_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        else:
            return False
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf nodes must have a value")
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    def __repr__(self):
        return f"LeafNode({self.tag},{self.value},{self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag == None:
            raise ValueError("HTML invalid: parent node must have a tag")
        if len(self.children) == 0:
            raise ValueError("HTML invalid: parent class must have children")
        else:
            children_combined = [child.to_html() for child in self.children]
            result = "".join(children_combined)
            return f"<{self.tag}>{result}</{self.tag}>"
    def __repr__(self):
        return f"ParentNode({self.tag}, children:{self.children}, {self.props})"