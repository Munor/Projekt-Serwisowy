import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # Wskazuje na C:\Users\Mikolaj\Documents\GitHub\Projekt-Serwisowy

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
html_theme = 'sphinx_rtd_theme'
html_static_path = []