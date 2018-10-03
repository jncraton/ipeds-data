import csv

columns = [
  ('SCUGRAD','sfa{ay}.csv','Total Undergraduates'),
  ('SCUGFFN','sfa{ay}.csv','Total First-time, First-year Undergraduates'),
  ('UAGRNTA','sfa{ay}.csv','Average Total Aid'),
  ('UPGRNTA','sfa{ay}.csv','Average Pell Grant Aid'),
  ('IGRNT_A','sfa{ay}.csv','Average Institutional Grant Aid'),
]

schools = {}

final_columns = ['INSTNM','UNITID','C15BASIC','CONTROL','STABBR','ZIP']

for y in [2000 + i for i in range(10,18)]:
  with open('data/hd%s.csv' % y, encoding = 'cp1252') as f:
    for r in csv.DictReader(f):
      schools[r['UNITID']] = {}
      for c in final_columns:
        try:
          schools[r['UNITID']][c] = r[c]
        except KeyError:
          schools[r['UNITID']][c] = ''

for c in columns:
  for y in [2000 + i for i in range(10,18)]:
    if '{y}' in c[1]:
      print(c[0] + y)
      final_columns.append(c[0] + y)
      with open('data/hd%s.csv' % str(y), encoding = 'cp1252') as f:
        for r in csv.DictReader(f):
          schools[r['UNITID']][c[0] + y] = r[c[0]]

for c in columns:
  for ay in ['0708', '0809', '0910', '1011', '1112', '1213', '1314', '1415', '1516']:
    if '{ay}' in c[1]:
      print(c[0] + ay)
      final_columns.append(c[0] + ay)
      with open('data/' + c[1].replace('{ay}',ay)) as d:
        for r in csv.DictReader(d):
          try:
            schools[r['UNITID']][c[0] + ay] = r[c[0]]
          except KeyError:
            try:
              schools[r['UNITID']][c[0] + ay] = ''            
            except KeyError:
              # School didn't exist in imported list
              pass

with open('data/comparison.tsv', 'w') as f:
  writer = csv.DictWriter(f, dialect='excel-tab', fieldnames=final_columns)
  writer.writeheader()
  for s in schools.values():
    writer.writerow(s)

with open('data/comparison-public.tsv', 'w') as f:
  writer = csv.DictWriter(f, dialect='excel-tab', fieldnames=final_columns)
  writer.writeheader()
  for s in schools.values():
    if s['CONTROL'] == '1':
      writer.writerow(s)

with open('data/comparison-private-non-profit.tsv', 'w') as f:
  writer = csv.DictWriter(f, dialect='excel-tab', fieldnames=final_columns)
  writer.writeheader()
  for s in schools.values():
    if s['CONTROL'] == '2':
      writer.writerow(s)

with open('data/comparison-ny-pa-21.tsv', 'w') as f:
  writer = csv.DictWriter(f, dialect='excel-tab', fieldnames=final_columns)
  writer.writeheader()
  for s in schools.values():
    BAC_AS = 21
    BAC_DIV = 22
    if s['CONTROL'] == '2' and s['C15BASIC'] in [BAC_AS,BAC_DIV] and s['STABBR'] in ['NY','PA']:
      writer.writerow(s)
