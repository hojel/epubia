# -*- coding: utf-8 -*-
# load/save config file in XML

import os

default_config = {
            'Scraper' : 'Aladin',
            'DaumAPIKey': '9125fb6a1c2e7100009b4ad61d6089037386dba6',
            'NaverAPIKey': '6da7207e79464e4c95937b235978d425',
            #'GenericCSS': 'generic.css',
            'TargetCSS': 'Default',
            'UseDestDir': False,
            'DestDir': os.curdir,
            'FontFile': 'SeoulHangang.ttf',
            'OutputEPub': True,
            'OutputMarkdown': False,
            'OutputPDF': False,
            'UseTitleInOutputName': False,
            'ReformatText' : True,
            'CorrectWordBreak' : '',
            'GuessChapter' : True,
            'GuessParaSep' : True,
            'MaxBrowseLevel': 2,
            'SkipToFirstChapter': False,
            'SplitLargeText': True,
            'PreserveUserMeta': False,
            'TryHiresImage': False,
            'GraphicSeparator' : False,
            }

def load(cfgfile):
    config = default_config
    try:
        from xml.dom.minidom import parse
        dom = parse(cfgfile)
        for item in dom.getElementsByTagName('property'):
            key = item.getAttribute('name')
            if item.hasChildNodes():
                value = item.firstChild.data
                if value.lower() in ['true', 'false']:
                    value = bool(value.lower() == 'true')
                elif value.isdigit():
                    value = int(value)
            else:
                value = ''
            config[ key ] = value
    except:
        pass
    return config

def save(cfgfile, config):
    lines = []
    lines.append('<configuration>')
    for key in sorted(config):
        if 'APIKey' in key:
        	continue        # hide API Key
        value = config[key]
        if isinstance(value, bool):
            lines.append('  <property name="%s">%s</property>' % (key, str(value).lower()) )
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
