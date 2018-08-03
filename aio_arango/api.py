# aio_arango docs_to_urls
# created: 05.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com
import os
import re
import tarfile
from pathlib import Path
from pprint import pprint

import requests
import yaml
from bs4 import BeautifulSoup

from aio_arango.endpoints import Request


class ArangoAPI:
    re_chapter = re.compile(r'<h3 id=')
    re_method = re.compile(r'GET|POST|PATCH|PUT|DELETE|HEAD')
    re_upper = re.compile(r'([A-Z][a-z])')
    re_tags = re.compile(r'<[^>]*>')
    re_required_data = re.compile(r'(http://localhost:8529.+)(EOF)([^\2]+)(\2)')
    re_required_url_vars = re.compile(r'{(?P<uvar>[^}]+)}')
    re_name_from_doc = re.compile(
            ("(?P<url_end>add|all|change|configure|create|"
             "execute|find|list|modify|next|prolong|replace|set)"), re.MULTILINE)

    def __init__(self, client=None):
        self._conf = {}
        self._docs_dir = Path.cwd() / 'arango-api-docs'
        self._conf_file = self._docs_dir / 'client.conf.yaml'
        self.load()
        if client:
            self.apply(client)

    def __getitem__(self, item):
        return self._conf[item]

    def download(self):
        archive = requests.get('https://download.arangodb.com/arangodb33/doc/ArangoDB-3.3.11.tar.gz',
                               verify=False).content
        arc_file = 'ara-docs.tar.gz'
        with open(arc_file, 'wb') as tar:
            tar.write(archive)
        arc = tarfile.open(arc_file, 'r:*')
        arc.extractall(path=self._docs_dir)
        arc.close()
        os.remove(arc_file)

    def snake_case(self, word):
        word = word.replace('-', '_')
        if word == word.upper():
            return word
        nw = word[0]
        nw += self.re_upper.sub(r'_\1', word[1:])
        return nw.lower()

    def name_endpoint(self, method, url, doc):
        name = '_'.join(
                [self.snake_case(p) for p in url.split('/') if
                 not any([sym in p for sym in ['_', '{']])
                 and p not in [None, '']]
        )
        name = name.replace('-', '_').replace('#', '_').replace('gharial', 'graph')
        if name in self._conf.keys():
            try:
                if method == self._conf[name]['method']:
                    return name
            except: pass
            end = self.re_name_from_doc.search(doc)
            if end is None:
                return f"{name}_{method.lower()}".replace('patch', 'update')
            return f"{name}_{end.group('url_end')}".replace('modify', 'update')
        return name

    def serialize(self, stream: str):
        content = self.re_chapter.sub('</chapter><chapter><h3 id=', stream)
        doc = BeautifulSoup(content, 'lxml-xml')
        for chapter in doc.find_all('chapter'):
            try:
                ctitle = chapter.find('h3', id=True)
                if ctitle.string in ['Configuration']:
                    continue
                m, url = ctitle.find_next('code').string.split(' ')
                url = url.replace('-', '_')
                name = self.name_endpoint(m, url, ctitle['id'])
                self._conf[name] = {
                    'url': url,
                    'method': m,
                    'url_vars':  self.re_required_url_vars.findall(url),
                    'required': [],
                    'options': [],
                    'help': f"""\n**{ctitle.string.strip()}**\n"""
                }
                titles_seen = []
                for ul in chapter.find_all('ul'):
                    required = False
                    title = ul.find_previous('p').get_text().strip()
                    if title not in titles_seen:
                        titles_seen.append(title)
                        if not any([w in title.lower() for w in ['example', 'return', 'response']]):
                            if 'required' in title.lower():
                                required = True
                            self._conf[name]['help'] += f"""\n#### {title.replace(':', '')}"""
                            for li in ul.find_all('li'):
                                s = li.get_text().strip()
                                key = s.split(' ')[0].replace(':', '').strip()
                                self._conf[name]['help'] += f"""\n- {key}: {' '.join(s.split(':')[1:])}"""
                                if 'required' in s or required is True:
                                    if key not in self._conf[name]['required']:
                                        self._conf[name]['required'].append(
                                            self.snake_case(key))
                                else:
                                    self._conf[name]['options'].append(
                                        self.snake_case(key))
                g_seen = []
                for example in chapter.find_all('pre'):
                    pre_txt = self.re_required_data.search(example.get_text().strip())
                    if pre_txt:
                        g = pre_txt.groups()
                        g1 = pre_txt.group(1)
                        g2 = pre_txt.group(3).strip()
                        if g not in g_seen:
                            self._conf[name]['help'] += f"""  \n\n**Example:**\n\n  - {g1}"""
                            self._conf[name]['help'] += f"""  \n- data: {g2}"""
                        g_seen.append(g)
            except (AttributeError, ValueError):
                pass
        return self._conf

    def parse(self):
        for in_file in self._docs_dir.glob('**/HTTP/**/*.html'):
            with in_file.open('r') as docs:
                self.serialize(docs.read())

    def load(self):
        if self._conf_file.exists():
            f = self._conf_file.open()
            self._conf.update(**yaml.safe_load(f.read()))
            f.close()
        else:
            if not self._docs_dir.exists():
                self.download()
            self.parse()
            self.save()

    def apply(self, client):
        for k, v in self._conf.items():
            v.pop('url_vars')
            setattr(client, k, Request(client, **v))

    def save(self):
        with self._conf_file.open(mode='w') as conf:
            yaml.dump(self._conf, conf)
        with open(self._docs_dir / 'wiki.md', 'w') as file:
            for k, v in self._conf.items():
                file.write(f"\n\n# {k}\n")
                file.writelines(v['help'])
        with open(self._docs_dir / 'request.py', 'w') as file:
            for k, v in self._conf.items():
                prefix = "{self.client._url_prefix}"
                args_str = ''
                if len(v['url_vars']):
                    args_str = f"{', '.join(v['url_vars'])},"
                file.write(
                    f"""\n\nasync def {k}(self, {args_str}**kwargs):
                    return await self._session.request(
                    \"{v['method']}\", f\"{prefix}{v['url']}\", **kwargs)""")
if __name__ == '__main__':
    uc = ArangoAPI()
    pprint(uc._conf)
