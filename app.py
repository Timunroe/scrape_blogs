from requests_html import HTMLSession
import time
import urllib.request
import re

'''
<a class="content-nav-prev" href="https://e2e.thespec.com/2018/08/hanley-dealt-to-guelph.html">« Bulldogs send Hanley to Storm</a>
Need the href attribute of .content-nav-prev

what are the image links in posts?
img with class .asset
'''

config = [
    {'blog': 'e2e', 'url_start': 'https://e2e.thespec.com/2018/09/matsos-undergoing-tests-after-behind-bench-collapse-.html', 'url_prev': '.content-nav-prev'},
    {'blog': 'scratchingpost', 'url_start': 'https://scratchingpost.thespec.com/2015/05/christian-covington-son-of-grover-drafted-by-texans.html',
        'url_prev': '.content-nav-prev'}
]

# https://e2e.thespec.com/2018/09/matsos-undergoing-tests-after-behind-bench-collapse-.html

# https://a6.typepad.com/6a01b7c6e18f48970b01bb07b6c4b6970d-800wi
# https://ideas.typepad.com/.a/6a00d83451bb7469e201bb09ffeb44970d-800wi

session = HTMLSession()


def download_image(data):
    # expects list of dicts {'url': xxx, 'name': xxx}
    for item in data:
        # download image used
        print("Downloading image: ", item['fname'])
        urllib.request.urlretrieve(item['url'], item['fname'])
        time.sleep(5)
        # download full image
        print("Downloading image: ", (item['fname']).replace('-800wi', '-pi'))
        urllib.request.urlretrieve((item['url']).replace('-800wi', '-pi'), (item['fname']).replace('-800wi', '-pi'))
        time.sleep(10)
    pass


def get_image_links(r, blog):
    images_list = r.html.find('.asset.image-full')
    if images_list:
        print(f'''{len(images_list)} image(s) found''')
        images_urls = [
            {'url': (x.attrs)[
                'src'], 'fname': f'''{blog}/{(re.match('https://.*com/(.a/)?(.*-800wi)', (x.attrs)['src'])).group(2)}'''}
            for x in images_list
        ]
        download_image(images_urls)
    else:
        print('No images found')


def process_url(link, blog):
    print("Processing: ", link)
    r = session.get(link)
    get_image_links(r, blog)
    # find 'prev' link
    time.sleep(5)
    try:
        prev_url = ((r.html.find('.content-nav-prev', first=True)).attrs)['href']
        print("Previous url is: ", prev_url)
        process_url(prev_url, blog)
    except:
        print("End of posts")


for i in config:
    process_url(i['url_start'], i['blog'])
    time.sleep(5)
