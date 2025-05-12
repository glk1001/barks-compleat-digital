from bs4 import BeautifulSoup

from barks_fantagraphics.barks_titles import get_title_dict

#html_file = "/home/greg/Downloads/the-beagle-boys_I.N.D.U.C.K.S.html"
#html_file = "/home/greg/Downloads/gladstone_I.N.D.U.C.K.S.html"
#html_file = "/home/greg/Downloads/gyro_I.N.D.U.C.K.S.html"
#html_file = "/home/greg/Downloads/magica_I.N.D.U.C.K.S.html"
#html_file = "/home/greg/Downloads/herbert_I.N.D.U.C.K.S.html"
#html_file = "/home/greg/Downloads/jones_I.N.D.U.C.K.S.html"
#html_file = "/home/greg/Downloads/snozzie_I.N.D.U.C.K.S.html"
html_file = "/home/greg/Downloads/duckburg_I.N.D.U.C.K.S.html"

# def get_normalised_title(title_str: str) -> str:
#     if title_str.startswith("The"):
#        return title_str[4:] + ", The"
#     if title_str.startswith("A"):
#        return title_str[2:] + ", A"
#
#     return title_str


with open(html_file, "r") as f:
    html = f.read()

bs = BeautifulSoup(html, "html.parser")

table = bs.find('table')
data = []

for row in table.find_all('tr'):
    cols = row.find_all(['td', 'th'])
    cols = [col.find('div', class_='title') for col in cols]
    cols = [col.text.strip() for col in cols if col is not None]
    if cols:
        data.append(cols)

for row in data:
    print(row[0])

barks_titles = get_title_dict()
for row in data:
    title = row[0]
    if title in barks_titles:
        print(f"BARKS_TAGS[Tags.DUCKBURG].append((Titles.{barks_titles[title].name}, []))")
    else:
        print("Not a Barks title: ", title)

# title_tags = bs.body.find_all("div", "title")
# for div in title_tags:
#     print(div.string)
