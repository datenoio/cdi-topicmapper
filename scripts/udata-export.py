import sys
import csv
import os
from pymongo import MongoClient
import typer

app = typer.Typer()

def dict2csv(data, headers, filename, limit=None):
  f = open(filename, 'w', encoding='utf8')
  writer = csv.writer(f, delimiter=',')
  output = sorted(data.items(), key=lambda x: x[1], reverse=True)  
  writer.writerows(output)
  f.close()


@app.command()
def run():
  keywords = {}
  topics = {}
  client = MongoClient()
  db = client['udata']
  coll = db['dataset']
  n = 0
  total = coll.count_documents({})
  for record in coll.find():
    record = record['record']    
    n += 1
    if n % 10000 == 0:
      print('Processed %d of %d (%0.2f%%). Topics %d, keywords %d' % (n, total, n * 100.0/total, len(topics), len(keywords)))      
    if not isinstance(record, dict): continue
    if 'tags' in record.keys():
      if isinstance(record['tags'], str):
        k_list = [record['tags']]
      else:
        k_list = record['tags']
      for k in k_list:
        v = keywords.get(k, 0)
        keywords[k] = v + 1

  dict2csv(keywords, ['name', 'value'], '../data/udata_keywords.csv')

if __name__ == "__main__":
  app()