import csv

columns = [
  ('INSTNM','hd2016.csv','Name'),
  ('UNITID','hd2016.csv','ID'),
  ('C15BASIC','hd2016.csv','Carnegie Classification'),
  ('CONTROL','hd2016.csv','Public/Non-profit/For-profit'),
  ('STABBR','hd2016.csv','State'),
  ('ZIP','hd2016.csv','Zip Code'),
  ('FTEUG','efia{y}.csv','Undergraduate FTE'),
  ('FTEGD','efia{y}.csv','Graduate FTE'),
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

years = [str(2000 + i) for i in range(5,17)]
academic_years = ['0506', '0607', '0708', '0809', '0910', '1011', '1112', '1213', '1314', '1415', '1516']

schools = {}

final_columns = []

# Create all school dicts
for y in years:
  with open('data/hd%s.csv' % y, encoding = 'cp1252') as f:
    for r in csv.DictReader(f):
      try:
        schools[r['UNITID']] = {}
      except:
        schools[r['unitid']] = {}

def append_column(filename, col, by=None):
  out_col = col if not by else col + '-' + by
  print(out_col)
  final_columns.append(out_col)

  try:
    f = open('data/' + filename.replace('.csv','_rv.csv'), encoding = 'cp1252')
  except:
    f = open('data/' + filename, encoding = 'cp1252')

  missing = 0

  for r in csv.DictReader(f):
    try:
      schools[r['UNITID']][out_col] = r[col]
    except KeyError:
      missing += 1
      try:
        schools[r['UNITID']][out_col] = ''
      except KeyError:
        # School didn't exist in imported list
        pass

  if missing:
    print("%d missing values for %s" % (missing, out_col))

  f.close()

args = []

for c in columns:
  if '{y}' in c[1]:
    for y in years:
      args.append((c[1].replace('{y}',y),c[0],y))
  elif '{ay}' in c[1]:
    for ay in academic_years:
      args.append((c[1].replace('{ay}',ay),c[0],ay))
  else:
    args.append((c[1],c[0]))

for a in args:
  append_column(*a)

with open('data/comparison.tsv', 'w') as f:
  writer = csv.DictWriter(f, dialect='excel-tab', fieldnames=final_columns)
  writer.writeheader()
  for s in schools.values():
    writer.writerow(s)

with open('data/comparison-public.tsv', 'w') as f:
  writer = csv.DictWriter(f, dialect='excel-tab', fieldnames=final_columns)
  writer.writeheader()
  for s in schools.values():
    if s.get('CONTROL') == '1':
      writer.writerow(s)

with open('data/comparison-private-non-profit.tsv', 'w') as f:
  writer = csv.DictWriter(f, dialect='excel-tab', fieldnames=final_columns)
  writer.writeheader()
  for s in schools.values():
    if s.get('CONTROL') == '2':
      writer.writerow(s)

with open('data/comparison-ny-pa-oh-bacc-ma.tsv', 'w') as f:
  writer = csv.DictWriter(f, dialect='excel-tab', fieldnames=final_columns)
  writer.writeheader()
  for s in schools.values():
    MA = ['18','19','20']
    BAC_AS = '21'
    BAC_DIV = '22'
    if s.get('CONTROL') == '2' and s.get('C15BASIC') in MA+[BAC_AS,BAC_DIV] and s.get('STABBR') in ['NY','PA', 'OH']:
      writer.writerow(s)
