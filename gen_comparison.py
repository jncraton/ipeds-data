import csv

columns = [
  ('SCUGRAD','sfa{ay}.csv','Total Undergraduates'),
  ('SCUGFFN','sfa{ay}.csv','Total First-time, First-year Undergraduates'),
  ('UAGRNTA','sfa{ay}.csv','Average Total Aid'),
  ('UPGRNTA','sfa{ay}.csv','Average Pell Grant Aid'),
  ('IGRNT_A','sfa{ay}.csv','Average Institutional Grant Aid'),
  ('F2A02','f{ay}_f2.csv','Total Assets'),
  ('F2A03','f{ay}_f2.csv','Total Liabilities'),
  ('F2A03A','f{ay}_f2.csv','Debt related to Property, Plant, and Equipment'),
  ('F2A17','f{ay}_f2.csv','Total Plant, Property, and Equipment'),
  ('F2A18','f{ay}_f2.csv','Accumulated Depreciation'),
  ('F2B01','f{ay}_f2.csv','Total Revenue'),
  ('F2B02','f{ay}_f2.csv','Total Expenses'),
  ('F2B04','f{ay}_f2.csv','Total change in net assets'),
  ('F2C05','f{ay}_f2.csv','Institutional Grants (funded)'),
  ('F2C06','f{ay}_f2.csv','Institutional Grants (unfunded)'),
  ('F2C07','f{ay}_f2.csv','Total Student Grants'),
  ('F2C10','f{ay}_f2.csv','Total Allowances and Discounts'),
  ('F2D01','f{ay}_f2.csv','Total Tuition and Fees'),
  ('F2D08','f{ay}_f2.csv','Private gifts and grants'),
  ('F2D10','f{ay}_f2.csv','Investment return'),
  ('F2D16','f{ay}_f2.csv','Total Revenue and Investment return'),
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

def append_column(filename, col, ver, desc):
  name = "%s %s (%s)" % (col, ver, desc)
  print(name)
  final_columns.append(name)
  with open('data/' + filename, encoding = 'cp1252') as f:
    for r in csv.DictReader(f):
      try:
        schools[r['UNITID']][name] = r[col]
      except KeyError:
        try:
          schools[r['UNITID']][name] = ''
        except KeyError:
          # School didn't exist in imported list
          pass

for c in columns:
  if '{y}' in c[1]:
    for y in [2000 + i for i in range(10,18)]:
      append_column(c[1].replace('{y}',y),c[0],y,c[2])
  elif '{ay}' in c[1]:
    for ay in ['0708', '0809', '0910', '1011', '1112', '1213', '1314', '1415', '1516']:
      append_column(c[1].replace('{ay}',ay),c[0],ay,c[2])
  else:
    append_column(c[1],c[0],'latest',c[2])

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

with open('data/comparison-ny-pa-bacc-ma.tsv', 'w') as f:
  writer = csv.DictWriter(f, dialect='excel-tab', fieldnames=final_columns)
  writer.writeheader()
  for s in schools.values():
    MA = ['18','19','20']
    BAC_AS = '21'
    BAC_DIV = '22'
    if s['CONTROL'] == '2' and s['C15BASIC'] in MA+[BAC_AS,BAC_DIV] and s['STABBR'] in ['NY','PA']:
      writer.writerow(s)
