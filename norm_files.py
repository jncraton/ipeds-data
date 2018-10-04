import os

csvs = ['data/' + f for f in os.listdir('data') if f.endswith('.csv')]

for f in csvs:
  lf = f.lower()

  os.rename(f,lf)
    
  print(lf)
  
  content = ''
  with open(lf,'r',encoding='cp1252') as fr:
    content = fr.read()

  with open(lf,'w',encoding='cp1252') as fw:
    fw.write(content.upper())
