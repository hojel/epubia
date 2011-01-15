from distutils.core import setup
import py2exe

import sys
sys.path.append('c:/Program Files/Microsoft Visual Studio 9.0/VC/redist/x86/Microsoft.VC90.CRT')
 
includes = []
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter']
packages = ['Cheetah', 'markdown',
	    'reportlab', 'html5lib']
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                'tk84.dll']
 
setup(
    #console=['ptxt2epub/ptxt2epub.py'],
    windows=['epubia.py'],
    data_files=[("target", ["target/None.css", "target/Embed.css",
			    "target/NookColor.css",
                            "target/Nuut.css", "target/SonyReader.css",
                            ]),
                ("template", ["template/content.opf",
                              "template/toc.ncx",
                              "template/coverpage.xhtml",
                              "template/titlepage.xhtml",
                              "template/chapter.xhtml",
                              "template/generic.css",
                              "template/xhtml2pdf.css",
                              "template/pdf_coverpage.html",
                             ]),
                ("fonts", ["fonts/SeoulHangang.ttf",
                           ]),
                #("", []),
            ],
    options = {"py2exe": {"compressed": 2,
                          "optimize": 2,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 3,
                          "dist_dir": "dist",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": '',
                         }
              }
)
#vim:ts=4:sw=4:et
