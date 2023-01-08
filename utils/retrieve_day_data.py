import html
import re
import sys

from markdownify import markdownify as md

from utils import day_template, Context, slice_content
from utils.html_parser import AoCHTMLParser
from utils.yearly_readme import build_year

if __name__ == "__main__":
    context = Context(*sys.argv[1:])

    if not (input_file := context.resource("puzzle.in")).exists():
        resp = context.request_day("/input")
        if resp.status_code < 300:
            input_file.write(resp.content.decode("utf-8"))
        else:
            print(resp.text)
            exit(0)

    r_src = context.request_day()
    page = r_src.content.decode("utf-8")
    main_content = slice_content(page, "<main>", "</main>")[0].strip()
    r = re.compile(r"^<style>(.*)</style>(.*)$", re.DOTALL)
    if (matcher := r.match(main_content)) and (groups := matcher.groups()):
        main_content = groups[1]

    r = re.compile(
        r"^<article class=\"day-desc\">(.*)</article>\n"
        r"<p>Your puzzle answer was <code>(.*)</code>.</p>"
        r"<article class=\"day-desc\">(.*)</article>\n"
        r"(<p>Your puzzle answer was <code>(.*)</code>.</p>)?.*$",
        re.DOTALL,
    )
    if not (matcher := r.match(main_content)) or not (groups := matcher.groups()):
        print("Puzzle wasn't solved yet!")
        groups = [main_content, "", "", ""]

    task_md = md(groups[0] + groups[2])
    context.resource("README.md").write(task_md)
    context.resource("puzzle.out").write((groups[1] or "") + "\n" + (groups[4] or "" if len(groups) > 4 else "") + "\n")

    if not (source_file := context.source(f"day_{context.day}.py")).exists():
        title = task_md.splitlines()[0].split(": ")[1][:-4]
        with open(day_template.__file__) as f:
            tpl = f.read()
            filtered = tpl.replace("{YEAR}", context.year).replace("{DAY}", context.day).replace("{TITLE}", title)
        source_file.write(filtered)

    for i, pre_content in enumerate(slice_content(main_content, "<pre><code>", "</code></pre>")):
        if not (input_i_file := context.resource(f"{i}.in")).exists():
            unescaped = html.unescape(pre_content)
            parser = AoCHTMLParser()
            parser.feed(unescaped)
            input_i_file.write(parser.output)

    year_page = context.request_year().content.decode("utf-8")
    build_year(int(context.year), year_page)
