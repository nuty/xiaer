# -*- coding: utf-8 -*-
from xiaer import db
from pyquery import PyQuery as pq
import requests

from xiaer.collection.models import User, Entry, Song

routes = {
    'album': 'http://www.xiami.com/space/charts/u/{uid}/c/album/t/all/page/',
    'song': 'http://www.xiami.com/space/charts/u/{uid}/c/song/t/all/page/',
    'artist': 'http://www.xiami.com/space/charts/u/{uid}/c/artist/t/all/page/'
}

user_uri = 'http://www.xiami.com/u/{uid}/'


headers= {
        'Accept':'image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip,deflate,sdch',
        'Accept-Language':'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection':'keep-alive',
        'Referer':'http://www.xiami.com/u/2145456',
        'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/31.0.1650.63 Chrome/31.0.1650.63 Safari/537.36'
 }


class Spider(object):

    def __init__(self,uid):
        self.user_uri = user_uri
        self.uid = str(uid)
        self.routes = routes
        self.urls = self.make_urls()
        self.get = requests.get
        self.headers = headers
        
    def make_urls(self):
        urls = []
        for url in self.routes.values():
            u = url.format(uid=self.uid)
            urls.append(u)
        urls.reverse()
        return urls



    def format_uri(self,url,page=None):
        if page:
            rv = ''.join([url, str(page),'/']).strip()
        else:
            rv = url.format(uid=self.uid)
        return rv

    def init_user(self):
        user = User()
        html = self.make_html(self.format_uri(self.user_uri))
        user.uid = self.uid
        user.username = html('.p_name').find('a').eq(0).text()
        user.desc = html('#p_infoCount').find('p').eq(0).text()
        user.avatar = html('#p_buddy').find('img').eq(1).attr('src')
        self.save(user)
        return user

    def make_html(self, url):
        data = self.get(url,headers=self.headers)
        if data.ok:
            html = pq(data.content)
        else:
            html = None
        return html

    def loop(self):
        user = self.init_user()
        for url in self.make_urls():
            self.process(url,user)

    def process(self,url,user):
        start = 1
        end = 5
        for page in range(start, end):
            html = self.make_html(self.format_uri(url, page))
            if html:
                self.save_model(url, html, user)
        print 'done'

    def save(self,model):
        db.session.add(model)
        db.session.commit()
        return model

    def save_model(self,url, html,user):
        if 'song' in url:
            rv = self.save_song(html,user)
        elif 'artist' in url:
            rv = self.save_artist(html,user)
        else:
            rv = self.save_album(html,user)

        return rv

    def save_song(self, html,user):
        trs = html('.track_list').find('tr')
        for tr in trs.items():
            song = Song()
            song.name = tr('.song_name').find('a').eq(0).text()
            song.artist = tr('.song_name').find('a').eq(1).text()
            song.hits = tr('.song_hot').text()
            song.user_id = user.id
            song = self.save(song)
            print song._json()

    def save_artist(self, html,user):
        lis = html('.chart_artsit').find('li')
        for li in lis.items():
            artist = Entry()
            artist.name = li('.ico_radio').text()
            artist.hits = li('.playcounts').text()
            artist.state = 1
            artist.user_id = user.id
            artist = self.save(artist)
            print artist._json()


    def save_album(self, html,user):
        lis = html('.chart_album').find('li')
        for li in lis.items():
            album = Entry()
            album.name = li('.name').find('a').eq(0).text()
            album.hits = li('.playcounts').text()
            album.state = 2
            album.user_id = user.id
            album = self.save(album)
            print album._json()

 
