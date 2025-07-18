from bs4 import BeautifulSoup

from barks_fantagraphics.barks_titles import get_title_dict

#html_file = "/home/greg/Downloads/the-beagle-boys_I.N.D.U.C.K.S.html"
#html_file = "/home/greg/Downloads/gladstone_I.N.D.U.C.K.S.html"
#html_file = "/home/greg/Downloads/gyro_I.N.D.U.C.K.S.html"
#html_file = "/home/greg/Downloads/magica_I.N.D.U.C.K.S.html"
#html_file = "/home/greg/Downloads/herbert_I.N.D.U.C.K.S.html"
#html_file = "/home/greg/Downloads/jones_I.N.D.U.C.K.S.html"
#html_file = "/home/greg/Downloads/snozzie_I.N.D.U.C.K.S.html"
#html_file = "/home/greg/Downloads/duckburg_I.N.D.U.C.K.S.html"
#html_file = "/home/greg/Downloads/scrooge_I.N.D.U.C.K.S.html"
html_file = "/home/greg/Downloads/daisy_I.N.D.U.C.K.S.html"

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

table = bs.find('table', class_="boldtable itemTable storyTable")

data = []
for row in table.find_all('tr'):
    #print(row)
    cols = row.find_all(['td', 'th'])
    cols_code = [col.find('div', class_='storycode') for col in cols]
    cols_code = [col.text.strip() for col in cols_code if col is not None]
    cols_title = [col.find('div', class_='title') for col in cols]
    cols_title = [col.text.strip() for col in cols_title if col is not None]
    cols = cols_code + cols_title
    if cols:
        data.append(cols)

print("Raw story codes and titles:")
for row in data:
    print(row)

filtered_data = []
for row in data:
    if row[0].startswith("W US") or row[0].startswith("CX US"):
        continue
    filtered_data.append(row)

print("Filtered story codes and titles:")
for row in filtered_data:
    print(row)

# Character searches
barks_titles = get_title_dict()
character_titles = []
for row in filtered_data:
    print(row)
    title = row[1]
    if title in barks_titles:
        character_titles.append(barks_titles[title])
    else:
        print("Not a Barks title: ", title)

character_titles = sorted(character_titles, key=lambda x:x.value)
print(f"Tags.DAISY: [")
for title in character_titles:
    print(f"    Titles.{title.name},")
print(f"],")

# title_tags = bs.body.find_all("div", ["storycode","title"])
# for div in title_tags:
#     print(div.string)
