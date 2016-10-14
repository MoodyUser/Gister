import threading

from requests import get as _get
from gistsapi import models as gm
from gistsapi.models import Gist
from gistx import settings
from gistx import console as base_console
from languages import models as lm
from lxml import html

url_string = "?client_id={}&client_secret={}".format(settings.GITHUB_APP_ID, settings.GITHUB_API_SECRET)
x_lock = threading.Lock()


def populate():
    pages = []
    for page in range(1, 30):
        pages.append(r"https://api.github.com/gists?page={}&per_page=100&client_id={}&client_secret={}"
                     .format(page, settings.GITHUB_APP_ID, settings.GITHUB_API_SECRET))
    base_console.work(items=pages, callback=populate_page, workers=5)


def update():
    items = gm.Gist.objects.all().iterator()
    base_console.work(items=items, callback=update_gist_likes, workers=50)
    base_console.work(items=items, callback=update_gist, workers=50)


def update_gist_likes(gist):
    try:
        if gist.html_url is None:
            print("Passed gist number {} html_url is none".format(gist.git_id))
            return

        request = _get("{}{}".format(gist.html_url, url_string))
        with x_lock:
            if request.status_code != 200:
                print("Passed gist number {}".format(gist.git_id))
                return
            tree = html.fromstring(request.content)
            likes_count, forks_count = tree.xpath('//a[@class="social-count"]/text()')
            gist.likes_count = likes_count
            gist.forks_count = forks_count
            gist.save()
            print("Updating gist number {}".format(gist.git_id))
    except Exception:
        print("Exception at gist {} - {} - {}".format(gist.git_id, gist.html_url, Exception))


def update_gist(gist):
    request = _get(gist.self_url +
                   "?client_id={}&client_secret={}".format(settings.GITHUB_APP_ID, settings.GITHUB_API_SECRET))
    if request.status_code != 200:
        return
    print("Updating gist number {}".format(gist.git_id))
    gist = request.json()
    gm.save_github_api(gist, lm.endings())


def populate_page(url):
    request = _get(url)
    gists = request.json()
    endings = lm.endings()
    with x_lock:
        for item in gists:
            gist, ok = Gist.objects.update_or_create(
                git_id=item['id'], defaults=gm.get_from_api(item))
            for file in item['files']:
                ending = file.split(".")[-1]
                lang = endings.get(ending, None)
                if lang:
                    gist.language.add(lang)
            gist.save()
            print("New - {}".format(item['id']))
