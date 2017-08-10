"""Gather necessary data and create JSON with resulting dictionaries."""

from bs4 import BeautifulSoup as bs

from dateutil import parser

import pickle

import json

titles = []
posts = []
dates = []

"""Import gathered enpoint content."""
with open("body_dump.pkl", "rb") as f:
    response = pickle.load(f)

"""Create list containing titles."""
for r in response:
    soup = bs(r, 'html.parser')
    pretty = soup.div.prettify()
    titles.append(soup.find_all('h3', class_='post-title entry-title'))

"""Create list containing posts."""
for r in response:
    soup = bs(r, 'html.parser')
    pretty = soup.div.prettify()
    posts.append(soup.find_all(True, {"class": ["date-outer"]}))

"""Create dictionaries with new key list and endpoint data."""

for num, p in enumerate(posts):
    for enum, i in enumerate(p):
        if len(i) == 0:
            dates[num].append([])
            continue
        else:
            keys = ['title', 'date', 'post', 'pictures']
            vals = []
            title = titles[num][enum].text
            date = i.h2
            text_date = date.text
            parse_date = parser.parse(text_date)
            final_date = str(parse_date)
            content = i.find_all("div", class_="post-body")
            for c in content:
                new_list = []
                images = []
                for im in c.find_all('a'):
                    if im.img:
                        images.append(str(im.img['src']))
                post_text = c.text
                new_list.extend((title, final_date, post_text, images))
                dictionary = dict(zip(keys, new_list))
                dates.append(dictionary)

with open('all_posts.json', 'wb') as outfile:
    json.dump(dates, outfile)
