"""
Normalizes contents for all data files.

- Converts column names to uppercase
- Converts data values to uppercase
- Converts to Unix line endings
- Removes trailing whitespace from all lines

"""

import os

csvs = ['data/' + f for f in os.listdir('data') if f.endswith('.csv')]

for f in csvs:
  lf = f.lower()

  os.rename(f,lf)
    
  print(lf)
  
  content = ''
  with open(lf,'r',encoding='cp1252') as fr:
    content = fr.read()

  content = '\n'.join([l.strip() for l in content.splitlines()])

  with open(lf,'w',encoding='cp1252') as fw:
    fw.write(content.upper())
