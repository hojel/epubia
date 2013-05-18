#!/usr/bin/env python
#  Korean Text to ePUB Converter
#
#  For more detail info, visit http://code.google.com/p/epubia 
__program__ = 'epubia'
__version__ = '0.3.3'
__config__  = 'config.xml'

# load config file
import config_file
config = config_file.load(__config__)

# start GUI
import gui
gui.gui( config )

# save config file
config_file.save(__config__, config)

# vim:ts=4:sw=4:et
