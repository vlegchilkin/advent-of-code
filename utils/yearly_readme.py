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
            r"(\s<script>.*</script>.*)?"
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
    hti = Html2Image(custom_flags=["--default-background-color=0", "--virtual-time-budget=10000", "--hide-scrollbars"])
    height = 440
    if year == 2015:
        height += 20
    elif year == 2016:
        height += 90
    elif year == 2017:
        height += 100
    s = len('<pre class="calender">')
    nbsp_eol = "&nbsp;\n"
    _ = days[:s] + nbsp_eol + days[s:]
    ga = """
<!-- ga -->
<script>
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');
ga('create', 'UA-69522494-1', 'auto');
ga('set', 'anonymizeIp', true);
ga('send', 'pageview');
</script>
<!-- /ga -->
    """
    html_str = (
        f'<!DOCTYPE html><html lang="en-us"><head><meta charset="utf-8"/>'
        f"<link href='//fonts.googleapis.com/css?family=Source+Code+Pro:300&subset=latin,latin-ext' "
        f"rel='stylesheet' type='text/css'/>"
        f"</head><body>"
        f"{main_content}"
        f"{ga}"
        f"</body></html>"
    )
    path = hti.screenshot(html_str=html_str, css_str=styles, save_as=f"{year}.png", size=(400, height))
    shutil.copyfile(path[0], f"../resources/{year}/progress.png")

    captions = get_day_captions(year)
    parser = AoCHTMLParser()
    parser.feed(days)

    readme = '<img align="left" style="float: left;" src="progress.png" width="530px">\n\n<pre>\n'

    for h in parser.headers[:-1]:
        for _ in range(len(h["data"].split("\n")) - 1):
            readme += nbsp_eol

    if year == 2016 and 25 not in captions:
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
    build_year(2017)
