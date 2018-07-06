# aio_arango docs_to_urls
# created: 05.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com
import io
import os
import re
import ssl
import string
import tarfile
from asyncio import Protocol
from urllib.request import urlopen

import yaml
from pathlib import Path
from pprint import pprint
from string import Formatter
from bs4 import BeautifulSoup
import requests

class URLConfig:
    re_method = re.compile(r'[GOSUPCLTHEAD]+')
    re_upper = re.compile(r'([A-Z])')
    re_tags = re.compile(r'<[^>]*>')
    re_required_data = re.compile(r'EOF(?P<dstr>.+)EOF', re.MULTILINE)
    re_required_url_vars = re.compile(r'{(?P<uvar>[^}]+)}')
    re_name_from_doc = re.compile(
            ("(?P<url_end>add|all|change|configure|create|"
             "execute|find|list|modify|next|prolong|replace|set)"), re.MULTILINE)

    def __init__(self):
        self._conf = {}
        self._docs_dir = Path(__file__).parent.parent / 'arango-api-docs'
        self._conf_file = self._docs_dir / 'client.conf.yaml'
        if not self._conf_file.exists():
            if not self._docs_dir.exists():
                self.download()
            self.parse()
        else:
            f = self._conf_file.open()
            self.serialize(f)
            f.close()

    def __getitem__(self, item):
        return self._conf[item]

    def snake_case(self, word):
        for u in self.re_upper.findall(word.replace('-', '_')):
            word = word.replace(u, f'_{u.lower()}')
        return word

    def get_name(self, method, url, doc):
        name = '_'.join(
                [self.snake_case(p) for p in url.split('/') if
                 not any([sym in p for sym in ['_', '{']])
                 and p not in [None, '']]
        )
        name = name.replace('-', '_').replace('#', '_')
        if name in self._conf.keys():
            if method == self._conf[name]['method']:
                return name
            else:
                end = self.re_name_from_doc.search(doc)
                if end is None:
                    return f"{name}_{method.lower()}".replace('patch', 'update')
                return f"{name}_{end.group('url_end')}".replace('modify', 'update')
        return name

    def serialize(self, content: str):
        doc = BeautifulSoup(content, 'lxml-xml')
        for h3 in doc.find_all('h3', id=True):
            _doc = h3['id']
            required = False
            try:
                base = h3.find_next('code')
                m, url = base.string.split(' ')
                name = self.get_name(m, url, _doc)
                self._conf[name] = {
                    'url': url,
                    'method': m,
                    'required': [*self.re_required_url_vars.findall(url.replace('-', '_'))],
                    'options': [],
                    '__doc__': f"{' '.join(_doc.split('-'))}."
                }
                # print(self, h3)
                # print(base)
                ulist = h3.find_next('ul')
                last = ''
                subtitle = ''.join(ulist.find_previous('p').strings)
                print(subtitle)
                # print(ulist)
                required = 'required' in subtitle
                print(required)
                for s in ulist.strings:
                    if (required and ':' in s) or '(required):' in s:
                        self._conf[name]['required'].append(last.replace('-', '_'))
                        self._conf[name]['__doc__'].append(f"""{last}{s}""")
                    elif ':' in s and not last.isnumeric():
                        self._conf[name]['options'].append(f"""{last}{s}""")
                    last = s.replace('-', '_')
                print('looking for pre')
                pre = h3.find_next('pre')
                pre_str = ''.join(pre.strings)
                jstr = self.re_required_data.search(pre_str)
                print(jstr)

                # print(self.re_tags.sub('', pre_str))
                # print(pre_str)
                if jstr:
                    self._conf[name]['__doc__'] += (
                        f" Request body => {jstr.group(1)}".replace('  ', '')
                    )
            except (AttributeError, ValueError):
                pass
        return self._conf

    def parse(self):
        for in_file in self._docs_dir.glob('**/HTTP/**/*.html'):
            with in_file.open('r') as docs:
                self._conf.update(**self.serialize(docs.read()))
        with open(self._conf_file, 'w') as conf:
            yaml.dump(self._conf, conf)

    def download(self):
        archive = requests.get(
                'https://download.arangodb.com/arangodb33/doc/ArangoDB-3.3.11.tar.gz',
                verify=False).content
        arc_file = 'ara-docs.tar.gz'
        with open(arc_file, 'wb') as tar:
            tar.write(archive)
        arc = tarfile.open(arc_file, 'r:*')
        arc.extractall(path=self._docs_dir)
        arc.close()
        os.remove(arc_file)

if __name__ == '__main__':
    URLConfig().parse()
