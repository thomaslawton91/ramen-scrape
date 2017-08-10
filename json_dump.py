from bs4 import BeautifulSoup as bs

from dateutil import parser

import pickle

import json

import datetime

titles = []
new_titles = []
enum_titles = []
posts = []
dates = []

with open("body_dump.pkl", "rb") as f:
    response = pickle.load(f)

with open("titles.pkl", "rb") as f:
    titles = pickle.load(f)

for t in titles:
    soup = bs(t, 'html.parser')
    pretty = soup.div.prettify()
    new_titles.append(soup.find_all('h3', class_='post-title entry-title'))

for r in response:
    soup = bs(r, 'html.parser')
    pretty = soup.div.prettify()
    posts.append(soup.find_all(True, {"class": ["date-outer"]}))

for num, p in enumerate(posts):
    for enum, i in enumerate(p):
        if len(i) == 0:
            dates[num].append([])
            continue
        else:
            keys = ['title', 'date', 'post', 'pictures']
            vals = []
            title = new_titles[num][enum].text
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


# Find all by date-outer class
# this will create 113 date sorted lists
# each list has several lists, each has a date
# sort each sub list out by h2 for date and post-body
# for content, then map the date to each corresponding
# content for date, pics pulled by img tag, date parse
# is parser.parse(date)
