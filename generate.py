#!/usr/bin/env python

"""
Planeteria rewrite.
Copyright James Vasile 2011
Released under the GNU Affero General Public License, version 3 or later.
"""

"""
Back End
  generates the various pages

Front End
  admin to various pages
"""

import os, sys
from optparse import OptionParser
import config
from config import *
from galaxy import Galaxy
from planet import Planet

if not os.path.exists(DATA_DIR):
   os.mkdir(DATA_DIR)

   


"""
   &quot; 	&#34;
&amp; 	&#38;
&lt; 	&#60;
&gt; 	&#62;
&nbsp; 	&#160;
&iexcl; 	&#161;
&cent; 	&#162;
&pound; 	&#163;
&curren; 	&#164;
&yen; 	&#165;
&brvbar; 	&#166;
&sect; 	&#167;
&uml; 	&#168;
&copy; 	&#169;
&ordf; 	&#170;
&laquo; 	&#171;
&not; 	&#172;
&shy; 	&#173;
&reg; 	&#174;
&macr; 	&#175;
&deg; 	&#176;
&plusmn; 	&#177;
&sup2; 	&#178;
&sup3; 	&#179;
&acute; 	&#180;
&micro; 	&#181;
&para; 	&#182;
&middot; 	&#183;
&cedil; 	&#184;
&sup1; 	&#185;
&ordm; 	&#186;
&raquo; 	&#187;
&frac14; 	&#188;
&frac12; 	&#189;
&frac34; 	&#190;
&iquest; 	&#191;
&Agrave; 	&#192;
&Aacute; 	&#193;
&Acirc; 	&#194;
&Atilde; 	&#195;
&Auml; 	&#196;
&Aring; 	&#197;
&AElig; 	&#198;
&Ccedil; 	&#199;
&Egrave; 	&#200;
&Eacute; 	&#201;
&Ecirc; 	&#202;
&Euml; 	&#203;
&Igrave; 	&#204;
&Iacute; 	&#205;
&Icirc; 	&#206;
&Iuml; 	&#207;
&ETH; 	&#208;
&Ntilde; 	&#209;
&Ograve; 	&#210;
&Oacute; 	&#211;
&Ocirc; 	&#212;
&Otilde; 	&#213;
&Ouml; 	&#214;
&times; 	&#215;
&Oslash; 	&#216;
&Ugrave; 	&#217;
&Uacute; 	&#218;
&Ucirc; 	&#219;
&Uuml; 	&#220;
&Yacute; 	&#221;
&THORN; 	&#222;
&szlig; 	&#223;
&agrave; 	&#224;
&aacute; 	&#225;
&acirc; 	&#226;
&atilde; 	&#227;
&auml; 	&#228;
&aring; 	&#229;
&aelig; 	&#230;
&ccedil; 	&#231;
&egrave; 	&#232;
&eacute; 	&#233;
&ecirc; 	&#234;
&euml; 	&#235;
&igrave; 	&#236;
&iacute; 	&#237;
&icirc; 	&#238;
&iuml; 	&#239;
&eth; 	&#240;
&ntilde; 	&#241;
&ograve; 	&#242;
&oacute; 	&#243;
&ocirc; 	&#244;
&otilde; 	&#245;
&ouml; 	&#246;
&divide; 	&#247;
&oslash; 	&#248;
&ugrave; 	&#249;
&uacute; 	&#250;
&ucirc; 	&#251;
&uuml; 	&#252;
&yacute; 	&#253;
&thorn; 	&#254;
&yuml; 	&#255;
&euro; 	&#8364;
"""



planets = []

def parse_options():
   parser = OptionParser()
   parser.add_option("", "--force", action="store_true", dest="force_update", help="force update of feeds", default=False),
   (options, args) = parser.parse_args()

   opt['force_check'] = options.force_update

   if len(args) >= 1:
      global planets
      planets.extend(args)

if __name__ == "__main__":

   parse_options()

   import templates
   for p,t in {'copyright':'Code and Copyright',
               'contact':'Contact Us',
               'thanks':'Thanks!',
               'tos':'Terms of Service',
               'index':'Welcome to Planeteria',
               }.items():
      opt['title'] = t
      eval('templates.%s(opt).write(OUTPUT_DIR, "%s.html")' % (p.capitalize(), p))
   opt['title']='Planeteria'

   galaxy = Galaxy(planets)
   galaxy.load()
   #galaxy.dump()
   galaxy.update()
   galaxy.generate()

