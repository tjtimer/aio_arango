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
    def get_name(method, url):
        parts = [p for p in url.split('/')
                 if not any([sym in p for sym in ['_', '{']])]
        return parts[0] + '_'.join(parts[1:]) + f"_{method.lower()}"
    target = {}
    cont = BeautifulSoup(content, 'lxml-xml')
    for h3 in cont.find_all('h3', id=True):
        desc = h3['id']
        try:
            base = h3.find_next('code')
            m, url = base.string.split(' ')
            name = get_name(m, url)
            print(name)
            target[name] = {
                'url': url,
                'method': m,
                'required': [],
                'options': [],
                'desc': desc
            }
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
            config[in_file.parent.name].update(**serialize(docs.read()))
    pprint(config)
    with open('url_conf.yaml', 'w') as conf:
        yaml.dump(config, conf)

if __name__ == '__main__':
    parse()
