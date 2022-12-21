import html
import re
from html.parser import HTMLParser

from utils.retrieve_day_data import slice_content, Context


class AoCHTMLParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.tag_stack = []
        self.days = {}
        self.current_day = None
        self.classes = []

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append((tag, attrs))
        if tag == "span" or tag == "a":
            clazz = attrs[-1][1]
            self.classes.append(clazz)
            if clazz.startswith("calendar-day"):
                if clazz != "calendar-day":
                    self.current_day = {"data": ""}

    def handle_endtag(self, tag):
        del self.tag_stack[-1]
        del self.classes[-1]

    def handle_data(self, data):
        if not self.tag_stack:
            return

        if self.classes[-1] == "calendar-day":
            self.days[int(data)] = self.current_day
        else:
            self.current_day["data"] += data


R_TITLE = re.compile(r"^--- (.*) ---$")


def get_day_captions():
    result = {}
    for d in range(1, 25):
        if (readme_file := Context("2022", str(d)).resource("README.md")).exists():
            title = readme_file.read().splitlines()[0]
            g = R_TITLE.match(title).groups()
            title = f"<a href='day/{d}'>{g[0]}</a>"
            result[d] = title
    return result


if __name__ == "__main__":
    with open("../resources/2022/readme.src") as f:
        src = f.read()
    main_content = slice_content(src, "<main>", "</main>")[0].strip()
    groups = (
        re.compile(r"^<style>(.*)</style>\s<pre class=\"calendar\">(.*)</pre>$", re.DOTALL).match(main_content).groups()
    )
    styles = groups[0]
    calendar = groups[1]
    groups = (
        re.compile(r"^(.*)<span id=\"calendar-countdown\"></span><script>(.*)</script>(.*)$", re.DOTALL)
        .match(calendar)
        .groups()
    )
    days = groups[0] + groups[2]

    captions = get_day_captions()
    unescaped = html.unescape(days)
    parser = AoCHTMLParser()
    parser.feed(unescaped)
    print('<pre class="calendar">')
    for day, value in parser.days.items():
        v = value["data"]
        v = v[:-3] if v.endswith("**") else v
        if day in captions:
            v += f"\t{captions[day]}"
        print(v)
    print("</pre>")
