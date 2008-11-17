#!/usr/bin/python
import os, sys

from BeautifulSoup import BeautifulSoup
from urllib import urlopen
import re
from pprint import pformat as p

db = {}

sections = ['overall', 'passing', 'rushing', 'receiving', 'defense', 'punting', 'kicking', 'puntreturning', 'kickoffreturning']

def getStats():
  url = 'http://tsn.ca/cfl/statistics/?season=regular&scope=%(section)s&players=all&page=%(page)s'

  for section in sections:
    print 
    print section,
    sys.stdout.flush()
    index = 0
    while True:
      currentUrl = url % { 'section': section, 'page': index }
      page = urlopen(currentUrl).read()
      soup = BeautifulSoup(page)
      table = soup.findAll('tr')

      keys = []
      for column in table[0].findAll('th')[2:]:
        keys.append(column.findAll(text=re.compile(r'.*'))[0])
    
      for row in table:      
        row = [cell.findAll(text=re.compile(r'.*'))[0] for cell in row.findAll(re.compile('td|th'))]
        position, name, data = row[0], row[1], row[2:]
        
        db.setdefault(name, {})
        
        player = {}
  #      print data
        for key, value in zip(keys, data):
          player[key] = value
        db[name][section] = player
      
      print '.',    
      sys.stdout.flush()
      if 'Next Page' not in page:
        break
      index += 1
    
  print

  return db
  
db = eval(open('output').read())

print p(db)
print >> file('output', 'w'), p(db)

sectionDef = sections
sections = {}

      
for player in db:
  for section in sectionDef:
    if section not in db[player]:
      continue
    if section in sections:
      continue
    
    sections[section] = db[player][section].keys()


output = []
for player in db:
  row = [player]
  for section in sections:
    if section not in db[player]:
      row += ['']*len(sections[section])
      continue
  
    for stat in sections[section]:
      row.append(db[player][section][stat].strip())
  
  output.append(row)
  
f = file('output.csv', 'w')  

headers = []
subheaders = []
for section in sections:  
  subheaders += sections[section]
  sectionHeader = ['']*len(sections[section])
  sectionHeader[0] = section
  headers += sectionHeader
  
print >>f, ',' + ','.join(headers)
print >>f, 'name,' + ','.join(subheaders)

for row in output:
  print >>f, ','.join(row)
      

#http://tsn.ca/cfl/statistics/?season=regular&scope=passing&column=
#http://tsn.ca/cfl/statistics/?season=regular&conf=&scope=overall&players=all&column=Pts&sort=descending&filter=&group=1&page=0
#
#http://tsn.ca/cfl/statistics/?season=regular&scope=passing&column=
