#!/usr/bin/python
"""
Planeteria admin interface
Copyright 2009 James Vasile <james@hackervisions.org>
Released under AGPL, version 3 or later <http://www.fsf.org/licensing/licenses/agpl-3.0.html>

Utility functions
"""

import os, sys, dbm, time, shelve
import htmltmpl # Debian package python-htmltmpl
import config as cfg
from config import opt
import logging
log = logging.getLogger('planeteria')
import dateutil.parser
import withsqlite

try:
   import tidy
except KeyError:
   if not 'PATH' in os.environ:
      os.environ['PATH'] = ''
      import tidy

generated=[]

def pretty_print_dict (d, indent=0):
   for key, value in d.iteritems():
      print '\t' * indent + str(key)
      if isinstance(value, dict):
         pretty_print_dict(value, indent+1)
      else:
         print '\t' * (indent+1) + str(value)

def html2xml(ins):
   'replace all the html entities with xml equivs'
   ins = str(ins).replace("&nbsp;", "&#160;")
   return ins

def parse_updated_time(entry):
   return str(entry['updated'])
   
def just_body(xhtml):
   #print xhtml
   #sys.exit()
   try:
      return str(xhtml).split(' <body>')[1].split(' </body>')[0]
   except IndexError:
      return ''

class sqlite_db(withsqlite.sqlite_db):
   def __init__(self, fname):
      withsqlite.sqlite_db.__init__(self, os.path.join(cfg.data_dir, fname))

class shelve_db:
   def __init__(self, fname):
      self.fname = fname + ".shelf"
   def __enter__(self):
      self.db = shelve.open(os.path.join(cfg.data_dir, self.fname), 'c', writeback=False)
      return self.db
   def __exit__(self, type, value, traceback):
      self.db.close()

class our_db(sqlite_db):
   pass

class berkeley_db:
   def __init__(self, fname):
      self.fname = fname
   def __enter__(self):
      self.db = dbm.open(os.path.join(cfg.data_dir, self.fname), 'c')
      return self.db
   def __exit__(self, type, value, traceback):
      self.db.close()


def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
   """From django, mildly modified. TODO: check license"""
   """Returns a bytestring version of 's', encoded as specified in 'encoding'.

   If strings_only is True, don't convert (some) non-string-like objects. 
   """
   if not isinstance(s, basestring):
      try:
         return str(s)
      except UnicodeEncodeError: 
         return unicode(s).encode(encoding, errors)
   elif isinstance(s, unicode):
      return s.encode(encoding, errors)
   elif s and encoding != 'utf-8': 
      return s.decode('utf-8', errors).encode(encoding, errors) 
   else: 
      return s 

def merge_dict(a, b):
   """Return a hash containing all the keys and vals of a and all
   those of b that don't clash with a.  Modifies a in place and also
   returns a"""
   for k in b.keys():
      if a.has_key(k): continue
      else: a[k] = b[k]
   return a

def dict_val(dict, key):
   "Returns dict[key], but if key isn't present, returns a blank string"
   try:
      return dict[key]
   except KeyError:
      return ''

def write_file(dir, fname, string):
   "Opens a fname in dir for writing, writes string, closes fname"
   with open(os.path.join(dir, fname),"w") as FILE:
      FILE.write(string)

def write_add(output_dir, output_fname, contents):
   """Do a write_file and add to list of generated files"""
   write_file(output_dir, output_fname, contents)
   generated.append(os.path.join(output_dir, output_fname))

def interpolate(template, vals):
   "apply the keys and values in vals to template, return filled-in template"
   try:
      print template_vars['base_href']
   except:
      pass

   manager = htmltmpl.TemplateManager()
   template = manager.prepare(template)
   tp = htmltmpl.TemplateProcessor(html_escape=0)
   for key in vals:
      try:
         if isinstance(vals[key], basestring):
            tp.set(key, smart_str(vals[key], encoding='ascii', errors='ignore'))
         elif vals[key]:
            tp.set(key, vals[key])

      except:
         pass
   return tp.process(template)


def lxml_tidy(instr):
   from lxml import etree
   tree   = etree.HTML(instr.replace('\r', ''))
   if tree is None: #not tree:
      return ''
   output_text = '\n'.join([ etree.tostring(stree, pretty_print=True, method="xml") 
                             for stree in tree ])
   return str(output_text)

def soup_tidy(instr):
   from BeautifulSoup import BeautifulSoup
   tree = BeautifulSoup(instr)
   good_html = tree.prettify()
   return str(good_html)

def html_tidy(instr):
   options = dict(output_xhtml=1,
                  add_xml_decl=0,
                  indent=1,
                  show_body_only=1,
                  )
   tidied = tidy.parseString(instr, **options)
   return str(tidied)

def tidy2xhtml(instr):
   if not instr:
      return lxml_tidy(html_tidy(instr))
   return lxml_tidy(instr) #html_tidy(instr))
   return soup_tidy(lxml_tidy(html_tidy(instr)))


class Msg:
   """Rudimentary class to store a message object that can save
   messages and then return them as html or text."""
   txt=[]
   web = False
   def __init__(self, web=web):
      self.txt = []
      self.web = web
   def add(self, text):
      self.txt.append(text)
      if not self.web:
         print text
   def out(self):
      if web:
         self.html()
      else:
         self.text()
   def html(self):
      return "<br />\n".join(self.txt)
   def text(self):
      return "\n".join(self.txt)
   def para(status="start"):
      if para == "start":
         self.add("<p>")
      else:
         self.add("</p>")
