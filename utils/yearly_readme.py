import html
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
    main_content = slice_content(src, "<main>", "</main>")[0].strip()
    groups = (
        re.compile(
            r"^(<style>(.*)</style>\s)?(<pre class=\"calendar\">.*</pre>)(\s<div class=\"calendar-bkg\">.*</div>)?$",
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

    # filtered = re.sub(
    #     r"<a .* class=\"calendar-(.*)\">",
    #     "",
    #     days
    # )
    # filtered = filtered.replace("</a>", "")
    styles = (styles or "") + "a:link {text-decoration: none; color: grey;}"
    hti = Html2Image()
    if year == 2015:
        height = 430
    elif year == 2016:
        height = 520
    else:
        height = 420
    path = hti.screenshot(html_str=days, css_str=styles, save_as=f"{year}.png", size=(400, height))
    shutil.copyfile(path[0], f"../resources/{year}/progress.png")

    captions = get_day_captions(year)
    parser = AoCHTMLParser()
    parser.feed(days)

    readme = '<img align="left" style="float: left;" src="progress.png" width="530px">\n\n<pre>\n'
    for day, value in parser.days.items():
        v = ""
        lines = value["data"].split("\n")
        for _ in range(len(lines) - 3):
            v += "&nbsp;\n"
        if day in captions:
            v += captions[day]
        else:
            v += "&nbsp;"
        readme += v + "\n"
    readme += "</pre>\n"
    with open(f"../resources/{year}/README.md", "w") as f:
        f.write(readme)


if __name__ == "__main__":
    build_year(2022)
