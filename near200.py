#!/usr/bin/env python


import urllib2

class http_code:

    def append_http(self, url):
        url = url + '/../..'
        self.error(url)

    def error(self, url):
        code = str(self.urlOpen(url))
        print url, code
        client_error = set(['401', '403', '404', '405']) #add as much as you like
        if code in client_error:
            self.append_http(url)
    
    def urlOpen(self, url):
        try:
            request = urllib2.Request(url)
            read_url = urllib2.urlopen(request)
            return read_url.code
        except urllib2.HTTPError, show:
            return show.code


     

httpCode = http_code()

uri = ["https://www.digitalocean.com/community/tutorials/how-to-import-and-export-databases-in-mysql-or-mariadb/lkajsklas/90/laksjkjas/alsjhkahskjas/asjhakjshkjas/aslkjakslj"]
for i in uri:
    httpCode.error(i)
    print '\n'


	