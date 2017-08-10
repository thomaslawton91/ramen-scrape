"""Request and store each endpoint on Ramen Adventures."""

import requests as rq

import pickle

urls = []
base = 'http://www.ramenadventures.com/'
year = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]


def get_urls(base, years):
    """Create list of enpoints with supplied dates."""
    m = 8
    y = 2008
    while y < 2018:
        if m > 9:
            if m == 12:
                urls.append(base + str(y) + '/' + str(m))
                # print('going up a year from ' + str(year))
                m = 1
                y = y + 1
            else:
                urls.append(base + str(y) + '/' + str(m))
                # print('over 9' + str(year))
                m = m + 1
        else:
            urls.append(base + str(y) + '/0' + str(m))
            # print('under 9' + str(year))
            m = m + 1


get_urls(base, year)

response = []

"""Store each endpoint's contents in response list."""
for url in urls:
    result = rq.get(url)
    content = result.content
    response.append(content)

with open("body_dump.pkl", "wb") as f:
    pickle.dump(response, f)
