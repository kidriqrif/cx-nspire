from ibcore import*
import math
TITLE='Algebra'
def _isint(r):
 return isnum(r)and '/'not in r and('.'not in r)
def _v(x):
 return '%.5g'%float(x)if '.'in x and isnum(x)else pp(x)
def _w(x,s=0):
 t=_v(x)
 if len(split_terms(x))>1 or t[:1]=='-'or(not s and[c for c in x if c in '/*']):
  t='('+t+')'
 return t
def _sf(f):
 t=sf3(f)
 if abs(f-round(f))>1e-09 and abs(float(t.split(' ')[0])-round(f))<1e-09:
  t=sf3(f,4)
 return t
def _q(s):
 f=split_top(s,'*')
 if 'u1'in f and len(f)>1 and(len(split_terms(s))<2):
  return 'u1 '+pp('*'.join([g for g in f if g!='u1']))
 return ps(s)
def _poly(P,v):
 P=G('numer(normal('+P+'))')
 c=Gs('content('+P+','+v+')')
 if c and c not in('0','1')and isnum(c):
  P=G('normal(('+P+')/('+c+'))')
 if Gs('lcoeff('+P+','+v+')')[:1]=='-':
  P=G('normal(-('+P+'))')
 return P
def _rs(eq,v):
 R=GL('solve('+eq+','+v+')')
 if[x for x in R if bad(x)or has(x,'i')]:
  R=[x for x in GL('fsolve('+eq+','+v+')')if not has(x,'i')]
  out('(GDC) '+v+' = '+', '.join([sf3(float(x),5)for x in R]))
 return R
def _r6(x):
 f=F(x)if '.'in x else None
 return x if f is None else '%.6g'%f
def _fl(o,c):
 return{'<':'>','>':'<','<=':'>=','>=':'<='}.get(o,o)if(c or 1)<0 else o
def _nck(e,C):
 o,h,X=C
 f=F(e)
 iq=o!='='
 r=''
 if f is None or f<=0:
  if not iq:
   out('No positive n')
   return
  f=0
 else:
  r=S(e)
  r=_sf(f)if '.'in r else ps(r)+(''if _isint(r)else ' = '+_sf(f))
 c=int(math.ceil(f-1e-09))
 if not iq:
  if abs(f-c)<1e-09:
   ans('n',str(c))
  else:
   out('n = '+r)
   out('n not an integer')
   ans('least n',str(c))
  return
 ok=[]
 for k in range(max(1,c-2),c+3):
  v=F('subst('+h+',n='+str(k)+')-('+X+')')
  if v is not None and('>'in o and v>1e-09 or('<'in o and v<-1e-09)or('='in o and abs(v)<=1e-09)):
   ok.append(k)
 if not ok:
  out('No n')
  return
 n0=ok[-1]
 lb='greatest n'
 if n0==c+2:
  lb='least n'
  while n0-1 in ok:
   n0-=1
 if r:
  out('n '+('>'if lb[0]=='l'else '<')+o[1:]+' '+r)
 ans(lb,str(n0))
def _fact(g,k):
 f=ask('Fact %d (u5=17, S10=40%s)'%(k,', Sinf=9'if g else ''),'',0)
 f=f.replace(' ','').replace('_','')
 j=f.find('=')
 if j<2:
  return None
 t=f[0].lower()
 p=f[1:j].lower()
 if t=='s'and p[:1]=='i':
  t='i'
 if t not in 'usi'or(t=='i'and(not g))or(t!='i'and(not(_isint(p)and int(p)>0))):
  return None
 return[t,p,norm(f[j+1:])]
def _seq(g):
 m='r'if g else 'd'
 hdr(('Geometric'if g else 'Arithmetic')+' sequence')
 if g:
  FU={'u':'u1*r^(P-1)','s':'u1*(r^P-1)/(r-1)','i':'u1/(1-r)'}
 else:
  FU={'u':'u1+(P-1)*d','s':'P/2*(2*u1+(P-1)*d)'}
 out('u_n = '+('u1 r^(n-1)'if g else 'u1 + (n-1)d'))
 out('S_n = '+('u1(r^n - 1)/(r - 1)'if g else 'n/2(2u1 + (n-1)d)'))
 if g:
  out('S_inf = u1/(1 - r), |r| < 1')
 a=askn('u1 (blank=unknown)','',0)
 d=askn(m+' (blank=unknown)','',0)
 U=[v for v,w in(('u1',a),(m,d))if w=='']
 T=[]
 for k in range(len(U)):
  f=_fact(g,k+1)
  if not f:
   out('Fact must be like u5=17 or S10=40'+(' or Sinf=9'if g else ''))
   wait()
   return
  t,p,y=f
  L=G(FU[t].replace('P',p))
  if a:
   L=G('subst('+L+',u1='+a+')')
  if d:
   L=G('subst('+L+','+m+'='+d+')')
  out('(%d) %s = %s'%(k+1,_q(L),pp(y)))
  T.append([t,p,y,L])
 if len(T)>1 and T[0][:2]==T[1][:2]:
  out('Need 2 different facts')
  wait()
  return
 if not U:
  sols=[[a,d]]
 elif len(U)==1:
  v=U[0]
  t,p,y,L=T[0]
  if g and v=='r'and(t=='u'):
   out('r^'+str(int(p)-1)+' = '+pp(S('('+y+')/('+a+')')))
  R=_rs(L+'=('+y+')',v)
  sols=[[x,d]if v=='u1'else[a,x]for x in R]
 elif g and T[0][0]=='u'and(T[1][0]=='u'):
  if int(T[1][1])<int(T[0][1]):
   T=[T[1],T[0]]
  p1=int(T[0][1])
  k=int(T[1][1])-p1
  w=S('('+T[1][2]+')/('+T[0][2]+')')
  out('(2)/(1): r^%d = %s'%(k,pp(w)))
  R=_rs('r^%d=%s'%(k,w),'r')
  sols=[[S('('+T[0][2]+')/('+x+')^'+str(p1-1)),x]for x in R]
 else:
  j=0
  for q in(1,0):
   if T[q][0]in('ui'if g else 'u'):
    j=q
  if g and T[1-j][0]=='i':
   j=1-j
  o=1-j
  w=S(GL('solve('+T[j][3]+'=('+T[j][2]+'),u1)')[0])
  out('(%d): u1 = %s'%(j+1,ps(w)))
  e=S('subst('+T[o][3]+',u1='+w+')')
  out('sub in (%d): %s = %s'%(o+1,ps(e),pp(T[o][2])))
  P=_poly('('+e+')-('+T[o][2]+')',m)
  if P=='0':
   out('0 = 0: facts not independent')
   wait()
   return
  if g:
   out(ps(P)+' = 0')
  R=_rs(P+'=0',m)
  sols=[[S('subst('+w+','+m+'='+x+')'),x]for x in R]
 if g:
  ok=[]
  for s in sols:
   if s[1]in('0','1')and[t for t in T if t[0]!='u']:
    out('r = '+s[1]+' rejected')
   elif[t for t in T if t[0]=='i']and F('abs('+s[1]+')')>=1:
    out('r = '+pp(s[1])+' rejected (|r| < 1)')
   else:
    ok.append(s)
  sols=ok
 sols=[[_r6(x)for x in s]for s in sols]
 if not sols:
  out('No solution')
  wait()
  return
 c=0
 if len(sols)>1:
  for k in range(len(sols)):
   out('%d) u1 = %s, %s = %s'%(k+1,_v(sols[k][0]),m,_v(sols[k][1])))
  c=int(ask('Use','1',0))-1
 a,d=sols[c]
 A=_v(a)
 out('u1 = '+A+', '+m+' = '+_v(d))
 GU='('+FU['u'].replace('P','n')+')'
 GS='('+FU['s'].replace('P','n')+')'
 if g:
  k={'1':'','-1':'-'}.get(a,A)
  K='('+k+')'if '/'in k else k
  TU=(K+'('+_v(d)+')'if k else _w(d))+'^(N-1)'
  TS=_w(d)+'^N - 1'
  dn=''if d=='2'else '/('+_v(d)+' - 1)'
  TS=TS if K+dn==''else K+'('+TS+')'+dn
  if d=='1':
   GS,TS,TU=('n*u1',('('+A+')'if '/'in A else A)+'N',A)
 else:
  TU=A+' + (N-1)('+_v(d)+')'
  TS='N/2(2('+A+') + (N-1)('+_v(d)+'))'
 sb=',[u1,'+m+'],['+a+','+d+'])'
 un=S('subst('+GU+sb)
 sn=S('expand(subst('+GS+sb+')')
 out('u_n = '+TU.replace('N','n')+(''if g else ' = '+ps(un)))
 out('S_n = '+TS.replace('N','n')+(''if g else ' = '+ps(sn)))
 if g:
  if F('abs('+d+')')<1:
   out('|r| < 1: S_inf = '+_w(a)+'/(1 - '+_w(d,1)+')')
   ans('S_inf',_r6(S('('+a+')/(1-('+d+'))')))
  else:
   out('|r| >= 1: no sum to infinity')
 n=ask('n (blank=skip)','',0)
 if n:
  n=norm(n)
  nb=',[u1,'+m+',n],['+a+','+d+','+n+'])'
  out('u_'+n+' = '+TU.replace('N',n))
  ans('u_'+n,_r6(S('subst('+GU+nb)))
  out('S_'+n+' = '+TS.replace('N',n))
  ans('S_'+n,_r6(S('subst('+GS+nb)))
 q=ask('Solve u_n=X, S_n>X.. (blank=skip)','',0).replace(' ','').replace('_','')
 if q:
  o='<'if '<'in q else '>'if '>'in q else '='
  if o!='='and '='in q:
   o+='='
  X=norm(q[max(q.rfind('='),q.rfind('<'),q.rfind('>'))+1:])
  su=q[0]in 'uU'
  C=[o,un if su else sn,X]
  L=(TU if su else TS).replace('N','n')+' '+o+' '+pp(X)
  out(L)
  if g:
   if F(d)<=0 or d=='1':
    out('r <= 0 or r = 1: use GDC table')
   else:
    p='(n-1)'if su else 'n'
    w=S('('+X+')/('+a+')'if su else '1+('+X+')*(('+d+')-1)/('+a+')')
    o=_fl(o,F(a if su else '('+a+')/(('+d+')-1)'))
    if L!=_w(d)+'^'+p+' '+o+' '+_v(w):
     out(_w(d)+'^'+p+' '+o+' '+_v(w))
    if(F(w)or 0)<=0:
     out('r^n > 0: no n')
    else:
     if F(d)<1:
      out(p+(''if su else ' ')+'ln('+_v(d)+') '+o+' ln('+_v(w)+')')
     _nck(('1+'if su else '')+'ln('+w+')/ln('+d+')',C)
  elif su:
   if F(d)==0:
    out('d = 0: every term = '+pp(a))
   else:
    w=S('(('+X+')-('+a+'))/('+d+')')
    out('n - 1 '+_fl(o,F(d))+' ('+pp(X)+' - '+_w(a)+')/'+_w(d)+' = '+pp(w))
    _nck('1+'+w,C)
  else:
   P=_poly(sn+'-('+X+')','n')
   out(ps(P)+' '+_fl(o,F('lcoeff('+sn+',n)'))+' 0')
   R=_rs(P+'=0','n')
   out('n = '+' or '.join([pp(x)for x in R]))
   R=[x for x in R if F(x)>0]
   _nck(R[0]if R else '0',C)
 wait()
def arith():
 _seq(0)
def geom():
 _seq(1)
def sigma():
 hdr('Sigma notation')
 e=norm(rhs(ask('Term u_k =','',0)))
 v='k'
 for c in 'krnx':
  if has(e,c):
   v=c
   break
 a=askn('From '+v+' =','1',0)
 b=ask('To '+v+' = (inf ok)','',0)
 inf=b.strip().lower()in('inf','oo','infinity')
 b=''if inf else norm(b)
 u=CFG['uni']
 out(('Σ'if u else 'sum')+'('+ps(e)+'), '+v+' = '+pp(a)+' to '+(('∞'if u else 'inf')if inf else pp(b)))
 t=[_r6(S('subst('+e+','+v+'=('+a+')+'+str(j)+')'))for j in range(3)]
 tl=''
 n=''
 if not inf:
  n=S('('+b+')-('+a+')+1')
  tl=_r6(S('subst('+e+','+v+'='+b+')'))
 out('= '+join_signed([pp(x)for x in t]+['...']+([]if inf else[pp(tl)])))
 x=G('exact('+e+')')if '.'in e else e
 dd=S('diff('+x+','+v+')')
 rr=S('normal(subst('+x+','+v+'='+v+'+1)/('+x+'))')
 if x!=e:
  dd=_r6(G('evalf('+dd+')'))
  rr=_r6(G('evalf('+rr+')'))
 s=''
 if not inf and(not has(dd,v)):
  out('u1 = '+pp(t[0])+', d = '+pp(dd)+' (arithmetic)')
  out('n = '+(''if a=='1'else pp(b)+' - '+_w(a)+' + 1 = ')+n)
  out('S_n = n/2(u1 + u_n)')
  out(' = '+n+'/2('+join_signed([pp(t[0]),pp(tl)])+')')
  s=n+'*(('+t[0]+')+('+tl+'))/2'
 elif not has(rr,v):
  out('u1 = '+pp(t[0])+', r = '+pp(rr)+' (geometric)')
  if inf:
   if F('abs('+rr+')')<1:
    out('|r| < 1: S_inf = u1/(1 - r)')
    out(' = '+_w(t[0])+'/(1 - '+_w(rr,1)+')')
    s='('+t[0]+')/(1-('+rr+'))'
   else:
    out('|r| >= 1: series diverges')
  else:
   out('n = '+n)
   out('S_n = u1(r^n - 1)/(r - 1)')
   out(' = '+(''if t[0]=='1'else _w(t[0]))+'('+_w(rr)+'^'+n+' - 1)/('+pp(rr)+' - 1)')
   s='('+t[0]+')*(('+rr+')^'+n+'-1)/(('+rr+')-1)'
 else:
  out('Not arithmetic/geometric (GDC)')
  s='sum('+e+','+v+','+a+','+('inf'if inf else b)+')'
 if s:
  ans('Sum',_r6(S(s)))
 wait()
def _money(lbl,e):
 out('ANS: '+lbl+' = %.2f'%(F(e)+5e-09))
def finance():
 hdr('Compound interest')
 dp=yes('Depreciation','n')
 w=ask('Find FV/PV/n/r','FV',0).lower()
 if w not in('fv','pv','n','r'):
  w='fv'
 out('FV = PV(1 '+('- r/100)^n'if dp else '+ r/(100k))^(kn)'))
 pv=''if w=='pv'else askn('PV','',0)
 r=''if w=='r'else askn('r (% per year)','',0)
 k='1'if dp else askn('k (periods/year)','1',0)
 n=''if w=='n'else askn('n (years)','',0)
 fv=''if w=='fv'else askn('FV','',0)
 sg='-'if dp else '+'
 o=k=='1'
 h=S('100*('+k+')')
 m='1'+sg+'('+r+')/'+h
 kn='('+k+')*('+n+')'
 B='(1 '+sg+' '+(_v(r)if r else 'r')+'/'+('100'if o else '(100('+_v(k)+'))')+')'
 E=(_w(n)if n else 'n')if o else '('+_v(k)+('('+_v(n)+')'if n else 'n')+')'
 if w=='fv':
  out('FV = '+_v(pv)+B+'^'+E)
  _money('FV','('+pv+')*('+m+')^('+kn+')')
 elif w=='pv':
  out('PV = '+_v(fv)+'/'+B+'^'+E)
  _money('PV','('+fv+')/('+m+')^('+kn+')')
 else:
  q=S('('+fv+')/('+pv+')')
  out(_v(pv)+B+'^'+E+' = '+_v(fv))
  if w=='n':
   x=F('ln('+q+')/(('+k+')*ln('+m+'))')
   if x is None or x<=0:
    out('No positive n')
    wait()
    return
   out(E.strip('()')+' = ln('+pp(q)+')/ln'+B+(''if o else ' = '+_sf(x*F(k))))
   ans('n','%.6f'%x)
   out('Whole '+('years: 'if o else 'periods: ')+str(int(math.ceil(x*F(k)-1e-09))))
  else:
   kn=_r6(S(kn))
   out('1 '+sg+' r/'+h+' = '+_w(q)+'^(1/'+kn+')')
   t='('+q+')^(1/('+kn+'))'
   ans('r','%.6f'%F(h+('*(1-'+t+')'if dp else '*('+t+'-1)')))
 wait()
def _fac(n):
 p=1
 for j in range(2,n+1):
  p*=j
 return p
def counting():
 hdr('nPr / nCr')
 t=ask('Perm or Comb (p/c)','c',0).lower()[:1]
 n=ask('n (n=unknown)','',0)
 R=int(ask('r =','',0))
 sym='P'if t=='p'else 'C'
 out('nPr = n!/(n-r)!'if t=='p'else 'nCr = n!/(r!(n-r)!)')
 n=n.strip()
 if not _isint(n):
  v=askn('Value','',0)
  e='*'.join(['(n-%d)'%j if j else 'n'for j in range(R)])if R else '1'
  ds=''.join(['(n-%d)'%j if j else 'n'for j in range(R)])if R else '1'
  k=_fac(R)if t=='c'else 1
  out('n'+sym+str(R)+' = '+ds+('/'+str(k)if k>1 else '')+' = '+pp(v))
  if k>1:
   v=S(str(k)+'*('+v+')')
   out(ds+' = '+pp(v))
  P=G('expand('+e+'-('+v+'))')
  out(ps(P)+' = 0')
  rs=_rs(P+'=0','n')
  out('n = '+' or '.join([pp(x)for x in rs]))
  ok=[x for x in rs if _isint(x)and int(x)>=R]
  if ok:
   out('n integer, n >= r')
   ans('n',ok[0])
  else:
   out('No valid n')
  wait()
  return
 N=int(n)
 lbl='%d%s%d'%(N,sym,R)
 if R<0 or R>N:
  out('r < 0 or r > n: no selections')
  ans(lbl,'0')
  wait()
  return
 if t=='p':
  out(lbl+' = %d!/%d!'%(N,N-R))
  s=R
 else:
  out(lbl+' = %d!/(%d!%d!)'%(N,R,N-R))
  s=min(R,N-R)
 if 1<s<=8:
  num='*'.join([str(N-j)for j in range(s)])
  out(' = '+pp(num+(''if t=='p'else '/('+'*'.join([str(s-j)for j in range(s)])+')')))
 ans(lbl,G(('perm'if t=='p'else 'comb')+'(%d,%d)'%(N,R)))
 wait()
ITEMS=[('Arithmetic seq',arith),('Geometric seq',geom),('Sigma sum',sigma),('Compound interest',finance),('nPr / nCr',counting)]
