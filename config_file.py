# -*- coding: utf-8 -*-
# load/save config file in XML

import os

class MyConfig:
    def __init__(self):
        self.config = {
                    'Scraper' : 'Daum',
                    'DaumAPIKey': 'DAUM_SEARCH_DEMO_APIKEY',
                    'NaverAPIKey': '',
                    #'GenericCSS': 'generic.css',
                    'TargetCSS': 'None',
                    'UseDestDir': False,
                    'DestDir': os.curdir,
                    'UseTitleInOutputFile': False,
                    }
        self.boolkey = [ 'UseDestDir', 'UseTitleInOutputFile' ]

    def load(self, cfgfile):
        try:
            from xml.dom.minidom import parse
            dom = parse(cfgfile)
            for item in dom.getElementsByTagName('property'):
                key = item.getAttribute('name')
                if item.hasChildNodes():
                    value = item.firstChild.data
                    if key in self.boolkey:
                        value = bool(int(value))
                else:
                    value = ''
                self.config[ key ] = value
        except:
            pass
        return self.config

    def save(self, config, cfgfile):
        self.config = config
        lines = []
        lines.append('<configuration>')
        for key, value in self.config.items():
            if key in self.boolkey:
                lines.append('  <property name="%s">%d</property>' % (key, int(value)) )
            else:
                lines.append('  <property name="%s">%s</property>' % (key, str(value)) )
        lines.append('</configuration>')

        try:
            f = open(cfgfile,'w')
            f.write( '\n'.join(lines) )
            f.close()
        except:
            pass

if __name__ == "__main__":
    file_name = 'config.xml'
    config = MyConfig().load(file_name)
    for key, val in config.items():
        print "%s = %s" % (key, val)
    MyConfig().save(config, file_name)

# vim:ts=4:sw=4:et
