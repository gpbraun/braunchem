######################################################
#
#  GET ELEMENT PROPERTIES
#
#  Gabriel Braun, May 2020
#
######################################################

import os
import sys
from datetime import date

######################################################
#
#  TEX FILE DESCRIPTION
#
######################################################

def generate_db(db_path):

    module      = 'database'
    description = 'Data Base Problem Paths'
    version     = '1.0'

    today = date.today().strftime('%Y/%d/%m')

    if os.path.isdir(db_path) is False:
        sys.exit(f'Directory {db_path} does not exist!')

    identifier = '\\begin{problem}'

    prop = open( db_path + '/.db-paths.sty', 'w+')

    prop.write( '\\ProvidesExplFile{%s}{%s}{%s}%%\n{ %s }\n\n' % (module,today,version,description) )

    prop.write('\\prop_const_from_keyval:Nn \\l_braun_db_prop\n{\n')

    count = 0

    for root, _, files in os.walk(db_path):
        for file in files:
            if file.endswith('.tex'):
                if identifier in open(os.path.join(root,file),mode='r',encoding='utf-8-sig').read():
                    ID = os.path.splitext(file)[0]
                    path = os.path.relpath(root,db_path).replace('\\', '/').replace(' ','~')
                    prop.write(f'\t{ID} = {path},')
                    count += 1
    prop.write('\n}')

    print('Data Base Generated!')
    print(f'PATH:  {db_path}')
    print(f'COUNT: {count}')

if __name__ == "__main__":
    generate_db("../database")
