import os
from pathlib import Path
from requests import get as _get
from pprint import pprint
from gistsapi.models import Gist
from gistx import settings
import re
from .models import Languages
from shutil import copyfile

parent_re = re.compile("(\w+)\((.+)\)")
child_re = re.compile(r"(\w+)\.(\w+)\.\w")


def populate():
    self_path = "/Languages"
    location = settings.ARTIFACTS + self_path
    folder = Path(location)
    if folder is None:
        print("Illegal. please contact a contributor")
        return

    languages = [collect_files(x) for x in folder.iterdir()]
    languages = [get_object(*x) for x in languages]
    parents = filter(lambda x: x != None and x.parent == None, languages)
    children = filter(lambda x: x != None and x.parent != None, languages)
    parents = {x.title: save(x) for x in parents}
    for child in children:
        child.parent = parents.get(child.parent, -1)
        child.save()


def get_object(location, name):
    val = parent_re.match(name)
    if val:
        return get_parent(location, name)

    val = child_re.match(name)
    if val:
        return get_child(location, name)


def save(obj):
    obj.save()
    return obj.id


def get_child(location, name):
    parent = name.split('.')[0]
    title = name.split('.')[1]
    return create_lang(name=title, parent=parent, icon=location)


def get_parent(location, name):
    title = name.split('(')[0]
    endings = name.split('(')[1].split(')')[0]
    return create_lang(name=name.split('(')[0], endings=endings, icon=location)


def create_lang(name, icon, endings=None, parent=None):
    lang = Languages()
    lang.title = name
    lang.file_ending = endings
    lang.icon = icon
    lang.parent = parent
    return lang


def collect_files(file):
    name = os.path.split(str(file))[-1]
    copyfile(str(file), 'languages/static/languages/' + name)
    return 'static/languages/' + name, name
