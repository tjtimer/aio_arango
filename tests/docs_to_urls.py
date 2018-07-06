# aio_arango docs_to_urls
# created: 05.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com
import re
import yaml
from pathlib import Path
from pprint import pprint

from bs4 import BeautifulSoup

method_re = re.compile(r'[GOSUPCLTHEAD]+')
code_re = re.compile(r'({(?P<obj>\w+)-(?P<key>\w+)*\})')

def serialize(content: str):
    target = {}
    cont = BeautifulSoup(content, 'lxml-xml')
    for h3 in cont.find_all('h3', id=True):
        name = h3['id'].replace(
                '-their-', '-'
        ).replace(
                '-the-', '-'
        ).replace(
                '-a-', '-'
        ).replace(
                '-of-', '-'
        ).replace(
                '-', '_'
        ).replace('returns_', '')
        target[name] = {}
        try:
            base = h3.find_next('code')
            m, url = base.string.split(' ')
            target[name].update({'url': url,
                                 'method': m,
                                 'required': [],
                                 'options': []}
                                )
            ulist = h3.find_next('ul')
            last = ''
            for s in ulist.strings:
                print(s)
                if '(required):' in s:
                    target[name]['required'].append(last.replace('-', '_'))
                elif ':' in s:
                    target[name]['options'].append(last.replace('-', '_'))
                last = s
        except:
            pass
    return target

def parse():
    docs_dir = Path('../arango_docs/HTTP')
    config = {}
    for in_file in docs_dir.glob('**/*.html'):
        if in_file.parent.name not in config.keys():
            config[in_file.parent.name] = {}
        with in_file.open('r') as docs:
            config[in_file.parent.name][in_file.name.split('.')[0]] = serialize(docs.read())
    pprint(config)
    with open('url_conf.yaml', 'w') as conf:
        yaml.dump(config, conf)

if __name__ == '__main__':
    parse()
