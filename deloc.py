import os
import re
import codecs

game='path/to/game/www/folder/here'

eng='path/to/dialogue.csv/here'

with codecs.open(eng, 'r', encoding='utf-8', errors='replace') as f:
  lines=f.readlines()
  
tls=[]
  
for line in lines:
  line=line.strip()

  if not line.__contains__(','):
    continue

  i=line.index(',')
  text=line[i+1:]
  
  text=text.replace('"', '')
  while text.endswith(',') or text.endswith('\n'):
    text=text[:len(text)-1]
  while text.startswith(','):
    text=text[1:]

  d=dict(id=line[:i], text=text)
  tls.append(d)

ntls=[]
pids=[]

for d in tls:
  id=d['id']
  
  if id in pids:
    continue
    
  pids.append(id)
  
  otext=d['text']
  text=otext
  
  for dd in tls:
    if dd['id']==id:
      if dd['text']!=otext:
        if dd['text'].startswith(' '):
          text=text+dd['text']
        else:
          text=text+' '+dd['text']

  ntls.append(d)

tls=ntls

#for d in tls:
#  print(str(d))
  
data='path/to/decrypted/data/folder/here'

_list=os.listdir(data)
maps=[]

for file in _list:
  if file.startswith('Map') and file.endswith('.json'):
    maps.append(file)

#for file in maps:
#  print(file)

for file in maps:
  map_=data+'/'+file
  
  with codecs.open(map_, 'r', encoding='utf-8', errors='replace') as f:
    read=f.read()
    
    for m in re.findall(r'\(label\)\[\w+\]', read):
      id=m[m.index('[')+1:m.rindex(']')]
      
      d=None
      for dd in tls:
        if dd['id']==id:
          d=dd
          
          break

      if d is None:
        continue
        
      text=d['text']
      read=read.replace(m, text.replace('\\', '\\\\'), 1)

  with codecs.open(map_, 'w', encoding='utf-8', errors='replace') as f:
    f.seek(0)
    f.write(read)
    f.flush()

for file in maps:
  map_=data+'/'+file
  
  with open(map_, 'r') as f:
    read=f.read()
    
    for m in re.findall(r'\(lines\)\[\w+\]', read):
      id=m[m.index('[')+1:m.rindex(']')]
      
      d=None
      for dd in tls:
        if dd['id']==id:
          d=dd
          
          break

      if d is None:
        continue
        
      text=d['text']
      text=text.replace(',', ': ', 1)
      read=read.replace(m, text.replace('\\', '\\\\'), 1)

  with open(map_, 'w') as f:
    f.seek(0)
    f.write(read)
    f.flush()



