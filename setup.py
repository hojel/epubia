from distutils.core import setup
import py2exe

from glob import glob
import sys
#sys.path.append('C:/Program Files (x86)/Common Files/Microsoft Shared/VSTO/10.0')
sys.path.append('./Microsoft.VC90.CRT')
 
includes = ['html5lib', 'lxml.html', 'lxml._elementpath']
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter']
packages = ['markdown', 'Cheetah', 'reportlab']
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                'tk84.dll', 'w9xpopen.exe']
 
setup(
    #console=['ptxt2epub/ptxt2epub.py'],
    windows=['epubia.py', 'tools/tgtxchg/tgtxchg.py'],
    data_files=[("target", ["target/None.css",
                            "target/Default.css",
                            "target/Embed.css",
                            "target/NookAndroid.css",
                            "target/NookExt.css",
                            "target/SonyReaderAndroid.css",
                            "target/SonyReaderExt.css",
                            ]),
                ("template", ["template/content.opf",
                              "template/toc.ncx",
                              "template/coverpage.xhtml",
                              "template/titlepage.xhtml",
                              "template/chapter.xhtml",
                              "template/generic.css",
                              "template/xhtml2pdf.css",
                              "template/pdf_coverpage.html",
                              "template/separator.png",
                             ]),
                ("fonts", ["fonts/SeoulHangang.ttf",
                           ]),
                ("input", ["input/example/example.txt",
                           "input/example/alice02a.gif",
                           ]),
                ("", ["README.txt", "LICENSE.txt"]),
                #("Microsoft.VC90.CRT", glob('C:/Program Files (x86)/Common Files/Microsoft Shared/VSTO/10.0/msvc*.dll')),
                ("Microsoft.VC90.CRT", glob('./Microsoft.VC90.CRT/*.*')),
            ],
    #zipfile=None,
    options = {"py2exe": {"compressed": 2,
                          "optimize": 2,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 1,
                          "dist_dir": "dist",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": '',
                         }
              }
)
#vim:ts=4:sw=4:et
