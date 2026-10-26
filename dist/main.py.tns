import sys
import gc
from ibcore import*
GROUPS=[('Number & algebra',[('Sequences/finance','ibalg'),('Logs/binom/parfrac','ibalg2'),('Complex/systems','ibcpx')]),('Functions',[('Roots/quadratics','ibfun'),('Lines/comp/rational','ibfun2'),('Inequal./modulus','ibfun3')]),('Trig & geometry',[('Triangles/solids','ibtrig'),('Trig values/ident','ibtrig2'),('Trig eq/graphs','ibtrig3'),('Vectors','ibvec'),('Lines/planes','ibvec2')]),('Stats & probability',[('Data/regression','ibstat'),('Binomial/normal','ibdist'),('Probability/Bayes','ibprob'),('Random variables','ibrv')]),('Calculus',[('Differentiation','ibdiff'),('Tangents/optimise','ibapp'),('Curves/kinematics','ibcurve'),('Integration','ibint'),('Areas/volumes','ibarea'),('Limits/series','iblim'),('Diff. equations','ibode')])]
IDX=[]
def settings():
 hdr('Settings')
 CFG['w']=int(ask('Chars per line',str(CFG['w'])))
 CFG['pg']=int(ask('Lines per page',str(CFG['pg'])))
 CFG['uni']=1 if yes('Unicode symbols','y'if CFG['uni']else 'n')else 0
 CFG['pause']=1 if yes('Pause each page','y'if CFG['pause']else 'n')else 0
def topic(name,first=-1,code=''):
 gc.collect()
 try:
  m=__import__(name)
 except ImportError:
  print('Missing '+name+'.py.tns')
  return
 except MemoryError:
  gc.collect()
  print('Out of memory: restart KhiCAS')
  return
 try:
  if 0<=first<len(m.ITEMS):
   go(m.ITEMS,first,code)
  menu(m.TITLE,m.ITEMS,code)
 finally:
  del m
  if name in sys.modules:
   del sys.modules[name]
  gc.collect()
def pick(title,labels,top=0):
 while True:
  ST['ln']=0
  print('== '+title+' ==')
  for k in range(len(labels)):
   print(str(k+1)+' '+labels[k])
  print('0 Quit'if top else '0 Back')
  if top:
   print('or code (511) or word')
  c=input('Choice: ').strip()
  if c=='0'or c=='':
   return-1
  if len(c)>1 or c not in DIG:
   return c
  k=int(c)-1
  if 0<=k<len(labels):
   return k
def _labels(s):
 r=[]
 i=s.find('ITEMS')
 while 0<=i<len(s)and s[i]!=']':
  q=s[i]
  if q in '\'"':
   j=i+1
   while j<len(s)and s[j]!=q:
    j+=2 if s[j]=='\\'else 1
   r.append(s[i+1:j])
   i=j
  i+=1
 return r
def index():
 if IDX:
  return IDX
 for g in range(len(GROUPS)):
  for m in range(len(GROUPS[g][1])):
   lab,name=GROUPS[g][1][m]
   s=''
   for p in list(sys.path)+['','/documents/Xcas']:
    try:
     f=open((p+'/'if p else '')+name+'.py')
     s=f.read()
     f.close()
     break
    except OSError:
     pass
   k=0
   for t in _labels(s):
    k+=1
    IDX.append((t,lab,str(g+1)+str(m+1)+str(k)))
   s=None
   gc.collect()
 return IDX
def jump(c,g=-1):
 for ch in c:
  if ch not in DIG:
   return search(c)
 if g>=0:
  c=str(g+1)+c
 d=[int(ch)-1 for ch in c]
 if len(d)<2 or not 0<=d[0]<len(GROUPS):
  return
 mods=GROUPS[d[0]][1]
 if 0<=d[1]<len(mods):
  topic(mods[d[1]][1],d[2]if len(d)>2 else-1,c[:2])
def search(w):
 w=w.lower()
 hits=[x for x in index()if w in x[0].lower()or w in x[1].lower()]
 if not hits:
  print('No match: '+w)
  return
 if len(hits)>9:
  print('%d matches, first 9'%len(hits))
  hits=hits[:9]
 k=pick('Find: '+w,[x[0]+' ['+x[2]+']'for x in hits])
 if isinstance(k,str):
  jump(k)
 elif k>=0:
  jump(hits[k][2])
def main():
 init()
 while True:
  g=pick('IB AA HL Solver',[x[0]for x in GROUPS]+['Settings'],1)
  if isinstance(g,str):
   jump(g)
   continue
  if g<0:
   return
  if g==len(GROUPS):
   ST['code']=''
   run(settings)
   continue
  mods=GROUPS[g][1]
  while True:
   k=pick(GROUPS[g][0],[x[0]for x in mods])
   if isinstance(k,str):
    jump(k,g)
    continue
   if k<0:
    break
   topic(mods[k][1],-1,str(g+1)+str(k+1))
main()
