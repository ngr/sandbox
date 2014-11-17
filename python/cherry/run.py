#!/usr/local/bin/python3.4
import os, random, string
import cherrypy

class fc_gimel_be(object):
    def index(self):
        return "<h1>Hello world!</h1> Index page of <i>fc_gimel_be</i>"

#    @cherrypy.expose
    def gen(self, length=8):
        return ''.join(random.sample(string.hexdigits, int(length)))

    index.exposed = True
    gen.exposed = True

if __name__ == '__main__':
# Assumes the config file is in the directory as the source.
    conf_path = os.path.dirname(os.path.abspath(__file__))
    conf_path = os.path.join(conf_path, "cherry.conf")
    cherrypy.config.update(conf_path)

    cherrypy.quickstart(fc_gimel_be())
