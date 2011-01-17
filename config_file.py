# -*- coding: utf-8 -*-
# load/save config file in XML

import os

default_config = {
            'Scraper' : 'Daum',
            'DaumAPIKey': 'DAUM_SEARCH_DEMO_APIKEY',
            'NaverAPIKey': '',
            #'GenericCSS': 'generic.css',
            'TargetCSS': 'Embed',
            'UseDestDir': False,
            'DestDir': os.curdir,
            'FontFile': 'SeoulHangang.ttf',
            'UseTitleInOutputName': False,
            'ReformatText' : True,
            'RemoveUntitledFirstChapter': True,
            'OutputEPub': True,
            'OutputMarkdown': False,
            'OutputPDF': False,
            }
boolkey = [ 'UseDestDir', 'UseTitleInOutputName',
            'ReformatText', 'RemoveUntitledFirstChapter',
            'OutputEPub', 'OutputMarkdown', 'OutputPDF'
          ]

def load(cfgfile):
    config = default_config
    try:
        from xml.dom.minidom import parse
        dom = parse(cfgfile)
        for item in dom.getElementsByTagName('property'):
            key = item.getAttribute('name')
            if item.hasChildNodes():
                value = item.firstChild.data
                if key in boolkey:
                    value = bool(int(value))
            else:
                value = ''
            config[ key ] = value
    except:
        pass
    return config

def save(cfgfile, config):
    lines = []
    lines.append('<configuration>')
    for key, value in config.items():
        if key in boolkey:
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
    config = load(file_name)
    for key, val in config.items():
        print "%s = %s" % (key, val)
    save(config, file_name)

# vim:ts=4:sw=4:et
