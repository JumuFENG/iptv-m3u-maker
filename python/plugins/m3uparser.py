# -*- coding: utf-8 -*-

import os
import re

class M3uParser(object):
    """the parser for m3u file"""
    def __init__(self):
        # self.T = tools.Tools()
        # self.now = int(time.time() * 1000)
        self.items = []

    def _extract_re_group1(self, r):
    	if r is None:
    		return ''
    	return r.group(1).strip()

    def write_to_file(self, file):
        with open(file, 'w', encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for it in self.items:
                if len(it['name']) == 0 or len(it['url']) == 0:
                    continue
                ext_line = '#EXTINF:-1'
                if 'title' in it and it['title'] is not None and len(it['title']) > 0:
                    ext_line += ' group-title=\"%s\"' % it['title']
                if 'tvgname' in it and it['tvgname'] is not None and len(it['tvgname']) > 0:
                    ext_line += ' tvg-name=\"%s\"' % it['tvgname']
                if 'logo' in it and it['logo'] is not None and len(it['logo']) > 0:
                    ext_line += ' tvg-logo=\"%s\"' % it['logo']
                if 'tvgid' in it and it['tvgid'] is not None and len(it['tvgid']) > 0:
                    ext_line += ' tvg-id=\"%s\"' % it['tvgid']
                ext_line += ', ' + it['name']
                f.write(ext_line + '\n')
                f.write(it['url'] + '\n')
        self.items = []

    def get_ext_title(self, ext_line):
    	title = re.search(r"group-title=\"(.*?)\"", ext_line)
    	return self._extract_re_group1(title)

    def get_ext_logo(self, ext_line):
    	logo = re.search(r"tvg-logo=\"(.*?)\"", ext_line)
    	return self._extract_re_group1(logo)

    def get_ext_id(self, ext_line):
    	tvid = re.search(r"tvg-id=\"(.*?)\"",ext_line)
    	return self._extract_re_group1(tvid)

    def get_ext_tvg_name(self, ext_line):
    	tvgname = re.search(r"tvg-name=\"(.*?)\"",ext_line)
    	return self._extract_re_group1(tvgname)

    def get_ext_name(self, ext_line):
    	name = re.search(r".+,(.*?)$", ext_line)
    	return self._extract_re_group1(name)

    def get_url(self, url_line):
    	if 'http' in url_line:
    		return url_line
    	return ''

    def decode_m3u(self, file):
    	with open(file, 'r', encoding="utf-8", errors='ignore') as f:
    		lines = f.readlines()
    		for i in range(0, len(lines)):
    			l = lines[i].strip('\n')
    			if not '#EXTINF:' in l:
    				continue
    			i += 1
    			l2 = lines[i].strip('\n')
    			title = self.get_ext_title(l)
    			gname = self.get_ext_tvg_name(l)
    			name = self.get_ext_name(l)
    			logo = self.get_ext_logo(l)
    			tvid = self.get_ext_id(l)
    			url = self.get_url(l2)
    			if len(url) == 0 or len(name) == 0:
    				continue
    			self.items.append({'url':url, 'name':name, 'title': title, 'tvgname': gname, 'logo': logo, 'tvgid': tvid})

    def decode_comma_seperated_TL(self, file):
    	with open(file, 'r', encoding="utf-8", errors='ignore') as f:
    		lines = f.readlines()
    		for i in range(0, len(lines)):
    			l = lines[i].strip('\n')
    			if len(l) == 0 or not ',' in l:
    				continue
    			tl = l.split(',')
    			self.items.append({'url':tl[1].strip(), 'name':tl[0].strip()})

    def decode_daum_play_list(self, file):
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for i in range(0, len(lines)):
                line = lines[i].strip('\n')
                if 'file' in line:
                    linef = line.split('*')
                    if len(linef) != 3:
                        continue
                    linef = linef[2]
                    i += 1
                    line2 = lines[i].strip('\n')
                    if 'title' in line2:
                        linet = line2.split('*')
                        if len(linet) != 3:
                            continue
                        linet = linet[2]
                        if len(linet) == 0 or len(linef) == 0:
                            continue
                        self.items.append({'url':linef.strip(), 'name':linet.strip()})

    def decode_by_file_ext(self, file):
        file_ext = re.search(r".*\.(.*)$", file)
        file_ext = self._extract_re_group1(file_ext)
        if file_ext == 'm3u' or file_ext == 'M3U':
            self.decode_m3u(file)
        elif file_ext == 'dpl' or file_ext == 'DPL':
            self.decode_daum_play_list(file)
        else:
            print('unknown file!', file)

    def decode_play_list(self, file):
        first_line = ''
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            l = f.readline()
            first_line = l.strip('\n')

        if first_line == '#EXTM3U':
            self.decode_m3u(file)
        elif first_line == 'DAUMPLAYLIST':
            self.decode_daum_play_list(file)
        elif ',' in first_line:
            self.decode_comma_seperated_TL(file)
        else:
            self.decode_by_file_ext(file)

    def decode_all_play_lists(self, dir):
        for parent, dirs, files in os.walk(dir):
            for f in files:
                self.decode_play_list(parent + os.sep + f)


# if __name__ == '__main__':
# 	m = M3uParser()
# 	ms = m.decode_all_play_lists('playlists')
# 	m.write_to_file('dot.m3u')
