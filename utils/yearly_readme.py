import re
import shutil
from html.parser import HTMLParser

from utils import Context, slice_content
from html2image import Html2Image


class AoCHTMLParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.tag_stack = []
        self.days = {}
        self.headers = []
        self.footers = []
        self.current_day = None
        self.classes = []

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append((tag, attrs))
        clazz = attrs[-1][1] if attrs and attrs[-1][0] == "class" else ""
        self.classes.append(clazz)
        if tag == "span" or tag == "a":
            if clazz.startswith("calendar-day"):
                if clazz != "calendar-day":
                    self.current_day = {"data": ""}
            elif clazz.startswith("calendar-") and not any([cls.startswith("calendar-day") for cls in self.classes]):
                self.current_day = {"data": ""}
                if self.days:
                    self.footers.append(self.current_day)
                else:
                    self.headers.append(self.current_day)

    def handle_endtag(self, tag):
        del self.tag_stack[-1]
        del self.classes[-1]

    def handle_data(self, data):
        if not self.tag_stack:
            return

        if self.classes and self.classes[-1] == "calendar-day":
            self.days[int(data)] = self.current_day
        else:
            self.current_day["data"] += data


R_TITLE = re.compile(r"^--- (.*) ---$")


def get_day_captions(year):
    result = {}
    for d in range(1, 26):
        if (readme_file := Context(f"{year}", str(d), create_roots=False).resource("README.md")).exists():
            title = readme_file.read().splitlines()[0]
            g = R_TITLE.match(title).groups()
            title = f"<a href='day/{d}'>{g[0]}</a>"
            result[d] = title
    return result


def build_year(year, src=None):
    if not src:
        with open(f"../resources/{year}/readme.src") as f:
            src = f.read()
    else:
        with open(f"../resources/{year}/readme.src", "w") as f:
            f.write(src)

    main_content = slice_content(src, "<main>", "</main>")[0].strip()
    groups = (
        re.compile(
            r"^(<style>(.*)</style>\s)?"
            r"(<pre class=\"calendar.*</pre>)"
            r"(\s<div class=\"calendar-bkg\">.*</div>)?"
            r"(\s<script>.*</script>)?"
            r"$",
            re.DOTALL,
        )
        .match(main_content)
        .groups()
    )
    styles = groups[1]  # styles
    calendar = groups[2]
    match = re.compile(r"^(.*)<span id=\"calendar-countdown\"></span><script>(.*)</script>(.*)$", re.DOTALL).match(
        calendar
    )
    if match:
        groups = match.groups()
        days = groups[0] + groups[2]
    else:
        days = calendar

    styles = (styles or "") + "a:link {text-decoration: none; color: grey;}"
    hti = Html2Image()
    height = 440
    if year == 2015:
        height += 20
    elif year == 2016:
        height += 90
    s = len('<pre class="calender">')
    nbsp_eol = "&nbsp;\n"
    html_str = days[:s] + nbsp_eol + days[s:]
    path = hti.screenshot(html_str=html_str, css_str=styles, save_as=f"{year}.png", size=(400, height))
    shutil.copyfile(path[0], f"../resources/{year}/progress.png")

    captions = get_day_captions(year)
    parser = AoCHTMLParser()
    parser.feed(days)

    readme = '<img align="left" style="float: left;" src="progress.png" width="530px">\n\n<pre>\n'

    for h in parser.headers:
        for _ in range(len(h["data"].split("\n")) - 1):
            readme += nbsp_eol

    if year == 2016:
        readme += nbsp_eol

    for day, value in parser.days.items():
        v = ""
        lines = value["data"].split("\n")
        for _ in range(len(lines) - 3):
            v += nbsp_eol
        if day in captions:
            v += captions[day]
        else:
            v += "&nbsp;"
        readme += v + "\n"

    for h in parser.footers:
        for _ in range(len(h["data"].split("\n")) - 1):
            readme += nbsp_eol

    readme += "</pre>\n"
    with open(f"../resources/{year}/README.md", "w") as f:
        f.write(readme)


if __name__ == "__main__":
    build_year(2016)
