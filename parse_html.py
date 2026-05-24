# Copyright (c) 2026 Prawin Kumar

from html.parser import HTMLParser

with open("course_runner.py", "r", encoding="utf-8") as f:
    content = f.read()

# Extract the HTML section
start_idx = content.find('INDEX_HTML = """<!doctype html>')
end_idx = content.find('"""', start_idx + 20)
html_content = content[start_idx:end_idx]

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if not self.tags:
            self.errors.append(f"Unexpected end tag </{tag}> at line {self.getpos()[0]}")
            return
        
        last_tag, pos = self.tags.pop()
        if last_tag != tag:
            self.errors.append(f"Mismatched tag: expected </{last_tag}> (started at line {pos[0]}), but got </{tag}> at line {self.getpos()[0]}")
            # Put back the mismatched tag to try and recover
            self.tags.append((last_tag, pos))

parser = MyHTMLParser()
parser.feed(html_content)

print(f"Parsed {len(html_content)} characters.")
if parser.errors:
    print("Found HTML structure errors:")
    for error in parser.errors:
        print(" -", error)
else:
    print("HTML structure is perfectly nested!")
