from bs4 import BeautifulSoup

html_file = "/tmp/vol-19.html"

with open(html_file, "r") as f:
    html = f.read()

bs = BeautifulSoup(html, "html.parser")

title_tags = bs.body.find_all("div", "title")
for div in title_tags:
    print(div.string)
