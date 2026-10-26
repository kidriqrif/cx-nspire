from ibcore import*
TITLE='Probability'
_M={'d':0}
def _q(s):
 o=''
 i=0
 n=len(s)
 while i<n:
  j=i
  while j<n and(s[j]in DIG or s[j]=='.'):
   j+=1
  if j==i:
   o+=s[i]
   i+=1
   continue
  t=s[i:j]
  if '.'in t and(i==0 or s[i-1]not in LET):
   a=t.split('.')
   t='('+str(int(a[0]+a[1]or '0'))+'/1'+'0'*len(a[1])+')'
   _M['d']=1
  o+=t
  i=j
 return o
def _e(s):
 s=norm(s)
 return S(_q(s))if s else ''
def _s3(v):
 return sf3(float('%.2e'%v))
def _cl(d):
 o=''
 i=0
 n=len(d)
 while i<n:
  if d[i]=='.'and d[i+1:i+2]=='0'and(i+2>=n or d[i+2]not in DIG):
   i+=2
   continue
  o+=d[i]
  i+=1
 j=o.find('.')
 while j>=0:
  e=j+1
  while e<len(o)and o[e]in DIG:
   e+=1
  if e-j>6:
   return ''
  j=o.find('.',e)
 return o
def _xv(r):
 if _M['d']and '/'in r and('/('not in r):
  d=Gs('evalf('+r+')')
  d=d and 'e'not in d and _cl(d)
  if d:
   r=d
 return ps(r)
def _I():
 return '∩'if CFG['uni']else 'n'
def _ne():
 return ' ≠ 'if CFG['uni']else ' != '
def _X():
 return '×'if CFG['uni']else 'x'
def _br(s):
 return s if len(s)==1 and s in LET else '('+s+')'
def _sm(L):
 return ps('+'.join([_g(z)for z in L]))
def _f(r):
 r=str(r)
 s=pp(r)
 v=F(r)
 if v is None or has_var(r):
  return _xv(r)
 t=_s3(v)
 if '.'in r:
  return t
 if isnum(r):
  if '/'not in r:
   return s
  q=int(r.split('/')[1])
  for k in range(80):
   if q%2==0:
    q//=2
   elif q%5==0:
    q//=5
  if q==1:
   if not _M['d']:
    return s
   d=G('evalf('+r+')')
   if len(d)<10 and 'e'not in d:
    return d
 return s+' ('+t+')'if len(s)<18 else t
def _g(r):
 return _f(r).split(' (')[0]
def _j(L):
 return '+'.join(['('+z+')'for z in L])or '0'
def _sx(V):
 for k in VS:
  V[k]=V[k]and S('subst('+V[k]+',x='+V['x']+')')
def _in01(r):
 v=F(r)
 return v is not None and-1e-12<=v<=1+1e-12
LB={'a':'P(A)','b':'P(B)','c':'P(AnB)','u':'P(AuB)','g':'P(A|B)','h':'P(B|A)','w':"P(A'nB')",'x':'x'}
VS='abcughw'
def _lb(k):
 s=LB[k]
 if CFG['uni']:
  s=s.replace('n','∩').replace('u','∪')
 return s
def _sub(t,V,lab):
 o=''
 for j in range(len(t)):
  ch=t[j]
  if ch in VS:
   v=V[ch]
   if v==''or lab:
    o+=_lb(ch)
   else:
    s=_g(v)
    n=(t[j-1]if j else '')+(t[j+1]if j+1<len(t)else '')
    if '*'in n or('/'in n and '/'in s):
     s='('+s+')'
    o+=s
  else:
   o+={'=':' = ','+':' + ','-':' - ','*':''}.get(ch,ch)
 for z in(' - 0',' + 0'):
  if o[-4:]==z and(not lab):
   o=o[:-4]
 return o
def _eq(t,V):
 o=''
 for ch in t:
  o+=('('+V[ch]+')'if V[ch]else ch)if ch in VS else ch
 return o
def _un(t,V):
 return[ch for ch in t if ch in VS and V[ch]=='']
def _two():
 V={}
 for k in VS:
  V[k]=_e(ask(_lb(k)+' (blank=?)','',_lb(k)))
 rel=ask('Given 0=none 1=indep 2=mut.excl','0',0)
 R=['u=a+b-c','g=c/b','h=c/a','w=1-u']
 if rel=='1':
  R.append('c=a*b')
 if rel=='2':
  R.append('c=0')
 unk=[k for k in VS if V[k]=='']+['x']
 for ps in range(3):
  for it in range(8):
   go=0
   for t in R:
    u=_un(t,V)
    e=_eq(t,V)
    h=has(e,'x')
    if h and(not u):
     u=['x']
    if len(u)!=1 or(h and u[0]!='x'):
     continue
    lab=_sub(t,V,1)
    val=_sub(t,V,0)
    lf=t[0]==u[0]
    last=lab[lab.find(' = ')+3:]
    out(lab)
    if lf:
     val=val[val.find(' = ')+3:]
     if val!=last:
      out('  = '+val)
      last=val
    elif val!=lab:
     out(val)
    rs=[r for r in GL('solve('+e+','+u[0]+')')if _in01(r)]
    if not rs:
     out('Inconsistent data')
     return
    V[u[0]]=rs[0]
    if not lf:
     out(_lb(u[0])+' = '+_f(rs[0]))
    elif _g(rs[0])!=last:
     out('  = '+_f(rs[0]))
    if h:
     _sx(V)
    go=1
   if not go:
    break
  U=[k for k in 'abcu'if V[k]=='']
  if not U or ps==2:
   break
  E=[t for t in R if _un(t,V)and(not[k for k in _un(t,V)if k not in 'abcu'])]
  hx=has(_j([V[k]for k in VS]),'x')
  U+=['x']*hx
  if len(E)<len(U):
   break
  out('(simultaneous equations)')
  for t in E:
   out(_sub(t,V,0))
  sol=[]
  for r in GL('solve(['+','.join([_eq(t,V)for t in E])+'],['+','.join(U)+'])'):
   r=parse_list(r)
   ok=len(r)==len(U)
   for x in r:
    ok=ok and _in01(x)
   if ok:
    sol.append(r)
  if not sol:
   out('No valid solution')
   return
  for j in range(len(U)):
   V[U[j]]=sol[0][j]
  if hx:
   _sx(V)
  out(', '.join([_lb(U[j])+' = '+_g(sol[0][j])for j in range(len(U))]))
  if len(sol)>1:
   out('or '+', '.join([_lb(U[j])+' = '+_g(sol[1][j])for j in range(len(U))]))
 if[k for k in 'abcu'if V[k]=='']:
  out('Not enough information')
  return
 a=F(V['a'])
 b=F(V['b'])
 c=F(V['c'])
 u=F(V['u'])
 if c>min(a,b)+1e-12 or u<max(a,b)-1e-12 or u>1+1e-12:
  out('Inconsistent data')
  return
 for k in 'ab':
  out(k.upper()+' only = '+_lb(k)+' - '+_lb('c')+' = '+_g(S(V[k]+'-('+V['c']+')')))
 if rel=='0':
  ab=S('('+V['a']+')*('+V['b']+')')
  out(_lb('a')+_lb('b')+' = ('+_g(V['a'])+')('+_g(V['b'])+') = '+_g(ab))
  if G('simplify('+V['c']+'-('+ab+'))')=='0':
   out(_lb('c')+' = '+_lb('a')+_lb('b')+' => independent')
  else:
   out(_lb('c')+_ne()+_lb('a')+_lb('b')+' => not independent')
  out(_lb('c')+(' = 0 => mutually exclusive'if c==0 else _ne()+'0 => not mut. exclusive'))
 x=ask("Extra 1=P(A|B') 2=P(B|A') 0=none",'0',0)
 if x in('1','2'):
  p,o=('a','b')if x=='1'else('b','a')
  L="P(A|B')"if x=='1'else "P(B|A')"
  r=S('('+V[p]+'-('+V['c']+'))/(1-('+V[o]+'))')
  out(L+' = ('+_lb(p)+' - '+_lb('c')+')/(1 - '+_lb(o)+')')
  out('  = ('+_g(V[p])+' - '+_g(V['c'])+')/(1 - '+_g(V[o])+')')
  out('ANS: '+L+' = '+_f(r))
 if unk:
  out('ANS: '+', '.join([_lb(k)+' = '+_g(V[k])for k in unk if V.get(k)]))
def _regions():
 rg=[_e(r)for r in askv('Region values (may use x)','',0)]
 T=_e(ask('Total (1 or N)','1',0))
 sm=N(_j(rg))
 e=has(sm,'x')or abs(F(sm+'-'+T))<1e-12
 out(' + '.join([_g(r)for r in rg])+(' = 'if e else _ne())+_g(T))
 if not e:
  return
 if has(sm,'x'):
  out(_g(sm)+' = '+_g(T))
  ok=[]
  for r in GL('solve('+sm+'='+T+',x)'):
   vals=[S('subst('+z+',x='+r+')')for z in rg]
   good=1
   for z in vals:
    good=good and(F(z)or 0)>=-1e-12
   if good:
    ok.append([r,vals])
  if not ok:
   out('No valid x')
   return
  out('ANS: x = '+_f(ok[0][0]))
  rg=ok[0][1]
  out('Regions: '+', '.join([_g(r)for r in rg]))
 for it in range(6):
  W=ask('Wanted regions e.g. 1,3 (blank=end)','',0)
  if not W:
   break
  Gv=ask('Given regions (blank=none)','',0)
  W=[int(z)for z in split_top(W,',')]
  if Gv:
   Gv=[int(z)for z in split_top(Gv,',')]
   I_=[k for k in W if k in Gv]
   n=S(_j([rg[k-1]for k in I_]))
   d=S(_j([rg[k-1]for k in Gv]))
   r=S('('+n+')/('+d+')')
   lb='P('+','.join([str(z)for z in W])+'|'+','.join([str(z)for z in Gv])+')'
   tm=_g(n)+'/'+_g(d)
   if tm!=_g(r):
    out(lb+' = '+tm)
  else:
   n=S(_j([rg[k-1]for k in W]))
   r=S('('+n+')/('+T+')')
   lb='P('+','.join([str(z)for z in W])+')'
   tm=' + '.join([_g(rg[k-1])for k in W])
   if len(W)>1 and T!='1':
    tm='('+tm+')'
   tm+=''if T=='1'else '/'+_g(T)
   if(len(W)>1 or T!='1')and tm!=_g(r):
    out(lb+' = '+tm)
  out('ANS: '+lb+' = '+_f(r))
def _cells(a,R):
 k=int(a[1:])-1
 return set([(i,j)for i in range(len(R))for j in range(len(R[0]))if(i,j)[a[0]=='c']==k])
def _evt(e,R):
 for op in 'nu':
  if op in e[1:]:
   x,y=e.split(op)
   A=_cells(x,R)
   B=_cells(y,R)
   return A&B if op=='n'else A|B
 return _cells(e,R)
def _table():
 R=[]
 for i in range(3):
  r=askv('Row '+str(i+1)+' counts'+(' (blank=end)'if i>1 else ''),'','r'+str(i+1))
  if r==['']or not r:
   break
  R.append([int(z)for z in r])
 rt=[sum(r)for r in R]
 ct=[sum([r[j]for r in R])for j in range(len(R[0]))]
 N_=sum(rt)
 out('Row totals: '+', '.join([str(z)for z in rt]))
 out('Col totals: '+', '.join([str(z)for z in ct]))
 out('N = '+str(N_))
 for it in range(6):
  qy=ask('Query e.g. r1|c2, r1nc2, c1 (blank=end)','',0).lower().replace(' ','')
  if not qy:
   break
  p=split_top(qy,'|')
  E=_evt(p[0],R)
  if len(p)>1:
   Gs_=_evt(p[1],R)
   E=E&Gs_
   d=sum([R[c[0]][c[1]]for c in Gs_])
   dl='n('+p[1]+')'
   nl='n('+(p[0]+'n'+p[1]if p[0]!=p[1]else p[0])+')'
  else:
   d=N_
   dl='N'
   nl='n('+p[0]+')'
  n=sum([R[c[0]][c[1]]for c in E])
  r=G(str(n)+'/'+str(d))
  out('P('+qy+') = '+nl+'/'+dl+' = '+str(n)+'/'+str(d))
  out('ANS: P('+qy+') = '+_f(r))
def prob_rules():
 hdr('Prob rules/Venn')
 _M['d']=0
 t=ask('1 two events 2 regions 3 two-way table','1',0)
 if t=='2':
  _regions()
 elif t=='3':
  _table()
 else:
  _two()
 wait()
def _dv(a,b):
 o=[]
 for x in(a,b):
  x=_g(x)
  o.append('('+x+')'if '/'in x or len(split_terms(x))>1 else x)
 return '/'.join(o)
def tree_bayes():
 hdr('Tree/Bayes')
 _M['d']=0
 m=3 if ask('No. of first events (2/3)','2',0)=='3'else 2
 P=[]
 for i in range(m):
  a='P(A'+str(i+1)+')'
  P.append(_e(ask(a+(' (blank=auto)'if i==m-1 else ''),'',a)))
 Q=[_e(ask('P(B|A'+str(i+1)+')','','P(B|A'+str(i+1)+')'))for i in range(m)]
 hx=has(''.join(P+Q),'x')
 if P[-1]=='':
  P[-1]=S('1-('+_j(P[:-1])+')')
  a='1 - '+' - '.join([_g(p)for p in P[:-1]])
  out('P(A'+str(m)+') = '+a+(''if _f(P[-1]).replace(' ','')==a.replace(' ','')else ' = '+_f(P[-1])))
 if not hx and G('simplify('+_j(P)+'-1)')!='0':
  out('Priors must sum to 1')
  wait()
  return
 f=ask("Find 1=P(B) 2=P(Ai|B) 3=P(Ai|B')",'2',0)
 i=int(ask('i','1',0))-1 if f in('2','3')else 0
 k=str(i+1)
 lb=['P(B)','P(A'+k+'|B)','P(A'+k+"|B')"][int(f)-1]
 if hx:
  v=_e(ask('Known value of '+lb,'',lb))
 I=_I()
 r=[]
 for j in range(m):
  z=str(j+1)
  r.append((N if hx else S)('('+P[j]+')*('+Q[j]+')'))
  if j==0:
   out('P(A1'+I+'B) = P(A1)P(B|A1)')
  out(('  = 'if j==0 else 'P(A'+z+I+'B) = ')+_br(_g(P[j]))+_br(_g(Q[j]))+' = '+_f(r[j]))
 PB=(N if hx else S)(_j(r))
 out('P(B) = '+' + '.join(['P(A'+str(j+1)+I+'B)'for j in range(m)]))
 out('  = '+_sm(r)+(''if f=='1'and(not hx)else ' = '+_f(PB)))
 res=PB
 if f=='2':
  res=S('('+r[i]+')/('+PB+')')
  out(lb+' = P(A'+k+I+'B)/P(B)')
  out('  = '+_dv(r[i],PB)+(' = '+_f(res)if hx else ''))
 elif f=='3':
  qc=S('1-('+Q[i]+')')
  rc=S('('+P[i]+')*('+qc+')')
  pc=S('1-('+PB+')')
  res=S('('+rc+')/('+pc+')')
  out("P(B'|A"+k+') = 1 - '+_g(Q[i])+' = '+_g(qc))
  out('P(A'+k+I+"B') = "+_br(_g(P[i]))+_br(_g(qc))+' = '+_g(rc))
  out("P(B') = 1 - "+_g(PB)+' = '+_g(pc))
  out(lb+' = P(A'+k+I+"B')/P(B')")
  out('  = '+_dv(rc,pc)+(' = '+_f(res)if hx else ''))
 if hx:
  out(_g(res)+' = '+_g(v))
  ok=[z for z in GL('solve('+res+'='+v+',x)')if _in01(z)]
  for z in ok:
   out('ANS: x = '+_f(z))
  if not ok:
   out('No x in [0,1]')
 else:
  out('ANS: '+lb+' = '+_f(res))
 wait()
def _seq(cnt,sq,rep):
 c=list(cnt)
 t=sum(c)
 a=1
 b=1
 tx=[]
 for g in sq:
  a*=c[g]
  b*=t
  tx.append(str(c[g])+'/'+str(t))
  if not rep:
   c[g]-=1
   t-=1
 return[a,b,(' '+_X()+' ').join(tx)]
def _ix(lab,s):
 for ch in s:
  if ch not in lab:
   raise ValueError('use labels '+lab)
 return[lab.index(ch)for ch in s]
def _fr(a,b):
 return G(str(a)+'/'+str(b))
def bag_draws():
 hdr('Draws (bag)')
 _M['d']=0
 cs=[int(z)for z in askv('Colour counts e.g. 5,3','',0)]
 lab=ask('Labels','RBGY'[:len(cs)],0).upper()
 d=int(ask('Draws d','2',0))
 rep=yes('Replace?','n')
 N_=sum(cs)
 if len(lab)<len(cs)or d<1 or(not rep and d>N_)or(d>10):
  out('Error: check counts/labels/d')
  wait()
  return
 out('Bag: '+', '.join([str(cs[j])+lab[j]for j in range(len(cs))])+' (total '+str(N_)+')')
 out(str(d)+' draws, '+('with'if rep else 'without')+' replacement')
 ev=ask('1 sequence 2 exactly k 3 at least 1 4 all same 5 at least k','1',0)
 if ev=='1':
  s=ask('Sequence e.g. RRB','',0).upper()
  r=_seq(cs,_ix(lab,s),rep)
  res=_fr(r[0],r[1])
  lb='P('+s+')'
  out(lb+' = '+r[2])
 elif ev=='4':
  ts=[]
  nm=[]
  for g in range(len(cs)):
   r=_seq(cs,[g]*d,rep)
   if r[0]:
    ts.append(_fr(r[0],r[1]))
    nm.append('P('+lab[g]*d+')')
    out(nm[-1]+' = '+r[2])
  res=S(_j(ts))
  lb='P(all same)'
  if len(ts)>1:
   out(lb+' = '+' + '.join(nm))
   out('  = '+' + '.join([_g(z)for z in ts]))
 else:
  C=ask('Colour','',0).upper()
  g=_ix(lab,C or '?')[0]
  two=[cs[g],N_-cs[g]]
  O=lab[1-g]if len(cs)==2 else C+"'"
  if ev=='3':
   r=_seq(two,[1]*d,rep)
   p0=_fr(r[0],r[1])
   res=S('1-'+p0)
   lb='P(at least 1 '+C+')'
   out('P(no '+C+') = '+r[2]+' = '+_g(p0))
   out(lb+' = 1 - P(no '+C+')')
   out('  = 1 - '+_g(p0))
  else:
   k=int(ask('k','',0))
   ks=range(k,d+1)if ev=='5'else[k]
   ts=[]
   for j in ks:
    r=_seq(two,[0]*j+[1]*(d-j),rep)
    nc=int(G('comb('+str(d)+','+str(j)+')'))
    if ev=='2'and 1<nc<=6:
     arr=[]
     for m in range(2**d):
      b=[m>>d-1-z&1 for z in range(d)]
      if sum(b)==j:
       arr.append(''.join([C if z else O for z in b]))
     out('Arrangements: '+', '.join(arr[::-1]))
    p1=_fr(r[0],r[1])
    t=S(str(nc)+'*'+p1)
    ts.append(t)
    lb='P('+str(j)+' '+C+')'
    nx=str(nc)+' '+_X()+' 'if nc>1 else ''
    out(lb+' = '+nx+r[2])
    if nx or(ev=='5'and len(ks)>1):
     out('  = '+nx+_g(p1)+(' = '+_g(t)if nx and ev=='5'else ''))
   res=S(_j(ts))
   if ev=='5':
    lb='P('+C+'>='+str(k)+')'
    if len(ks)>1:
     out(lb+' = '+' + '.join([_g(z)for z in ts]))
 out('ANS: '+lb+' = '+_f(res))
 wait()
ITEMS=[('Prob rules/Venn',prob_rules),('Tree/Bayes',tree_bayes),('Draws (bag)',bag_draws)]
