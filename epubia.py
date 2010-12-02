#!/usr/bin/env python
#  Korean Text to ePUB Converter
#
#  For more detail info, visit http://code.google.com/p/epubia 
__program__ = 'epubia'
__version__ = '0.1.0'
__config__  = 'config.xml'

# load config file
from config_file import MyConfig
config = MyConfig().load(__config__)

# start GUI
from gui.gui import gui
gui( config )

# save config file
MyConfig().save(config, __config__)

# vim:ts=4:sw=4:et
