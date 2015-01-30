from distutils.core import setup
import py2exe

setup(console=['main.py'],
    options={'py2exe':
        {'optimize': 2,
        'ascii': False,
        'compressed': 2,
        'excludes': ['_ssl', 'doctest', 'pdb', 'unittest', 'difflib',
                     'inspect', 'optparse', 'pickle', 'calendar', 'email',
                     'http', 'xml', 'PySide', 'PyQt4', 'PyQt5', 'PyQt',
                     'multiprocessing', 'socket', 'select', 'bz2', 'html',
                     '_bz2'
                     ],
        'dll_excludes': ['pyside-python3.4.dll', 'shiboken-python3.4.dll',
        'QtNetwork4.dll', 'QtGui4.dll', 'QtNetwork4.dll']
        #~ 'excludes': ['PyQt4', 'PyQt5']
        }
    }
)
