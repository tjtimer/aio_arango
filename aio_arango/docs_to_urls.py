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
upper_re = re.compile(r'([A-Z])')
req_re = re.compile(r'http://localhost:8529(?P<jstr>.+)EOF')
def snake_case(word):
    nw = upper_re.sub("_{\1}".lower(), word)
    return nw

def serialize(content: str):
    def get_name(method, url):
        parts = [snake_case(p) for p in url.split('/')
                 if not any([sym in p for sym in ['_', '{']])]
        return parts + f"_{method.lower()}"
    target = {}
    cont = BeautifulSoup(content, 'lxml-xml')
    for h3 in cont.find_all('h3', id=True):
        desc = h3['id']
        try:
            base = h3.find_next('code')
            m, url = base.string.split(' ')
            name = get_name(m, url).replace('_get', '')
            target[name] = {
                'url': url.replace('-', '_'),
                'method': m,
                'required': [],
                'options': [],
                'desc': f"""{' '.join(desc.split('-'))}"""
            }
            ulist = h3.find_next('ul')
            last = ''
            for s in ulist.strings:
                if '(required):' in s:
                    target[name]['required'].append(last.replace('-', '_'))
                elif ':' in s and not last.isnumeric():
                    target[name]['options'].append(last.replace('-', '_'))
                last = s
            pre = h3.find_next('pre')
            jstr = req_re.search(f"""{''.join(pre.strings)}""".replace('\n', ''))
            if jstr:
                target[name]['desc'] += f""", {jstr.group('jstr').replace('EOF', ' => ')}"""
        except:
            pass
    return target

def parse():
    docs_dir = Path(__file__).parent.parent / 'arango-http-docs'
    config = {}
    for in_file in docs_dir.glob('**/*.html'):
        with in_file.open('r') as docs:
            config.update(**serialize(docs.read()))
    with open('url_conf.yaml', 'w') as conf:
        yaml.dump(config, conf)

if __name__ == '__main__':
    parse()
