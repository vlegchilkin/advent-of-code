import string
from html.parser import HTMLParser


class AoCHTMLParser(HTMLParser):

    def __init__(self, *, convert_charrefs: bool = ...):
        super().__init__(convert_charrefs=convert_charrefs)
        self.tag_stack = []
        self.output = ""
        self.em_table = {
            string.ascii_uppercase + string.ascii_lowercase: 0x1D608,
            string.digits: 0x1D7F6,
            "#": 0x266F,
            # "#": 0x2600,
            # "#": 0x274E,
        }

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append((tag, attrs))

    def handle_endtag(self, tag):
        del self.tag_stack[-1]

    def handle_data(self, data):
        if self.tag_stack and self.tag_stack[-1][0] == "em":
            self.output += self._em(data)
        else:
            self.output += data

    def _em(self, data):
        response = ""
        for c in data:
            for pattern, offset in self.em_table.items():
                if c in pattern:
                    response += chr(pattern.index(c) + offset)
                    break
            else:
                response += c
        return response
