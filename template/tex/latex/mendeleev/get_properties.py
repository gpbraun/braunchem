#!/usr/bin/env python3
######################################################
#
#  GET ELEMENT PROPERTIES
#
#  Gabriel Braun, May 2020
#
######################################################

from molmass import ELEMENTS
from molmass  import GROUPS
from datetime import date

######################################################
#
#  TEX FILE DESCRIPTION
#
######################################################

module      = 'elements'
description = 'Element Properties'
version     = 'alpha'

today = date.today().strftime('%Y/%d/%m')

######################################################
#
#  BASIC DEFINITIONS
#
######################################################

def code_section(file,title):
	# Section organization on TeX file
	file.write('\n'+chr(37)*62+'\n'+chr(37)+'\n'+chr(37)+' '*3+title.upper()+'\n'+chr(37)+'\n'+chr(37)*62+'\n\n')

def code_subsection(file,title):
	# Section organization on TeX file
	file.write('\n'+chr(37)+'='*61+'\n'+chr(37)+' '*3+title.upper()+'\n'+chr(37)+'='*61+'\n\n')

######################################################
#
#  FILE INITIALIZATION
#
######################################################

f = open('mendeleev/mendeleev.'+module+'.sty','w+')

code_section(f,'Chemistry File Identification')

f.write( '\\ProvidesExplFile{%s}{%s}{%s}{ %s }\n' % (module,today,version,description) )

######################################################
#
#  ELEMENT LIST
#
######################################################

code_section(f,'Elements')

f.write( '\\clist_const:Nn \\c_elements_clist\n{\n\t%s\n}\n' % ',\t'.join([e.symbol for e in ELEMENTS]) )

######################################################
#
#  GENERAL ELEMENT PROPERTIES
#
######################################################

code_section(f,'Element Properties')

props = (
	'number',
	'symbol',
	'name',
	'mass',
	)

for e in ELEMENTS:
	code_subsection(f,e.name)
	f.write( '\\prop_const_from_keyval:Nn \\c_elements_%s_prop\n{\n' % e.symbol )

	for p in props:
		if p == 'mass':
			f.write( '\t%s = %.2f, \n' % (str(p), round(getattr(e,p),2)) )
		else:
			f.write( '\t%s = %s, \n' % (str(p), getattr(e,p)) )

	f.write( '}\n' )

######################################################
#
#  ADITIONAL ELEMENTS
#
######################################################

code_section(f,'Aditional Elements')

######################################################
#
#  GROUP ACRONYMS
#
######################################################

code_section(f,'Groups')

f.write( '\\prop_const_from_keyval:Nn \\c_groups_prop\n{\n')

for g in GROUPS:
		f.write( '\t%s = %s, \n' % (g, GROUPS[g]) )

f.write( '}\n' )

######################################################
#
#  THE END!!!
#
######################################################

code_section(f,'The End!!!')