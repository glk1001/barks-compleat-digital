import html2text

h = html2text.HTML2Text()

# Ignore converting links from HTML
h.ignore_links = True
with open("/tmp/fg.html", "r") as f:
    html = f.read()

text = h.handle(html)
print(text)

