from ibcore import*
import math
TITLE='Curves/kinematics'
ALL=[[None,'-inf'],[None,'inf']]
def _fl(r):
 x=F(r)
 if x is None or x!=x or abs(x)>1e+300:
  return None
 return x
def _t(r):
 r=r.replace('exp(1)','e')
 k=r.find('*')
 j=r.find('/')
 if 0<j<k and isnum(r[:k])and('/'not in r[k:])and(len(split_terms(r[k+1:]))==1):
  n=r[:j]
  r=(n[:-1]if n in('1','-1')else n+'*')+r[k+1:]+r[j:k]
 return r
def _pf(r):
 T=split_terms(r)
 P=[t for t in T if t[0]!='-']
 return join_signed(P+[t for t in T if t[0]=='-']if r[:1]=='-'else T)
def _d(r):
 if '.'in r:
  x=_fl(r)
  if x is not None:
   return sf3(x)
 return ps(_pf(_t(r)))
def _tk(e):
 T=[]
 i=0
 n=len(e)
 while i<n:
  j=i+1
  if e[i]in LET:
   while j<n and e[j]in LET:
    j+=1
  T.append(e[i:j])
  i=j
 return T
def _getf(p,dv):
 f=norm(rhs(ask(p,'',0)))
 vs=[]
 T=_tk(f)
 for k in range(len(T)):
  w=T[k]
  if w[0]in LET and(k+1==len(T)or T[k+1]!='(')and(w not in('pi','e','i'))and(w not in vs):
   vs.append(w)
 v=vs[0]if len(vs)==1 else dv
 out(p[0]+'('+v+') = '+ps(f))
 return(f,v)
def _sub(e,v,a):
 return 'subst('+e+','+v+'=('+a+'))'
def _rep(e,v,a):
 pl=True
 for c in a:
  if c not in LET and c not in DIG and(c!='.'):
   pl=False
 T=_tk(e.replace(' ',''))
 for k in range(len(T)):
  if T[k]==v:
   p=T[k-1]if k else ''
   q=T[k+1]if k+1<len(T)else ''
   n=T[k+2]if k+2<len(T)else ''
   if not(p+q=='()'or(p in('(','')and q in('+','-',')',''))or(pl and(not(p=='*'and a[:1].isdigit()or(q=='*'and n.isdigit()))))):
    T[k]='('+a+')'
   else:
    T[k]=a
 return ''.join(T)
def _ev(nm,e,v,a,q=0):
 r=S(_sub(e,v,a))
 x=_fl(r)
 w=ps(_rep(e,v,_t(a)))
 d=_d(r)if x is not None else 'undefined'
 if q and x is not None:
  d+=' < 0, so max'if x<-1e-09 else ' > 0, so min'if x>1e-09 else ', inconclusive'
 sh=w!=_d(r)and '.'not in a and(len(w)<40)
 out(nm+'('+_d(a)+') = '+(w+(' = 'if x is not None else ' ')if sh else '')+d)
 return r
def _D(f,v):
 d='diff('+f+','+v+')'
 r=S(d)
 b=Gs('expand(normal('+d+'))')
 if b and len(b)<=len(r):
  r=b
 b=Gs('regroup('+d+')')
 return b if b and len(b)<len(r)else r
def _dv(f,v,nm):
 r=_D(f,v)
 out(nm+'('+v+') = '+ps(r))
 return r
def _bd(s):
 s=s.strip()
 if s in('inf','-inf','+inf'):
  return s.replace('+','')
 return norm(s)
def _dom(f,v,p='Domain',dft=''):
 s=ask(p+' a,b (blank=all)',dft,0).strip('[]() ')
 if not s:
  return ALL
 L=[_bd(a)for a in split_top(s,',')]
 D=[[_fl(L[0]),L[0]],[_fl(L[1]),L[1]]]
 le=' ≤ 'if CFG['uni']else ' <= '
 o=[(le if _fl(_sub(f,v,L[k]))is not None else ' < ')if D[k][0]is not None else ''for k in(0,1)]
 if o[0]and o[1]:
  out(_d(L[0])+o[0]+v+o[1]+_d(L[1]))
 elif o[0]:
  out(v+o[0].replace('<','>').replace('≤','≥')+_d(L[0]))
 elif o[1]:
  out(v+o[1]+_d(L[1]))
 return D
def _in(x,dom,eps):
 return(dom[0][0]is None or x>dom[0][0]-eps)and(dom[1][0]is None or x<dom[1][0]+eps)
def _uniq(P):
 P.sort(key=lambda p:p[0])
 Q=[]
 for p in P:
  if not Q or p[0]-Q[-1][0]>1e-09:
   Q.append(p)
 return Q
def _roots(e,v,dom):
 c=e+'=0'
 rg=''
 for k in(0,1):
  if dom[k][0]is not None:
   c+=' and '+v+('>='if k==0 else '<=')+dom[k][1]
 if dom[0][0]is not None and dom[1][0]is not None:
  rg='='+dom[0][1]+'..'+dom[1][1]
 L=parse_list(Gs('solve('+c+','+v+')'))
 if L==['']or[r for r in L if bad(r)]:
  L=parse_list(Gs('fsolve('+e+'=0,'+v+rg+')'))
 P=[]
 for r in L:
  x=_fl(r)
  if x is not None and _in(x,dom,1e-09):
   if '.'in r and abs(x)<1e-09:
    r='0'
    x=0.0
   if '.'in r or _fl(_sub(e,v,r))is not None:
    P.append([x,r])
 return _uniq(P)
def _sing(e,v,dom):
 P=[]
 for r in parse_list(Gs('singular('+e+','+v+')')):
  x=_fl(r)if r else None
  if x is not None and _in(x,dom,-1e-09):
   P.append([x,r])
 return P
def _lst(P,v,no='no real solution'):
 if not P:
  return no
 s=v+' = '+', '.join([_d(p[1])for p in P])
 return s+(' (GDC)'if[p for p in P if '.'in p[1]]else '')
def _ne():
 return ' ≠ 'if CFG['uni']else ' != '
def _solve0(e,v,dom,nm=''):
 if e=='0':
  out(' true for all '+v)
  return[]
 if isnum(e):
  out(' '+(nm+' = 'if nm else '')+_d(e)+_ne()+'0')
  return[]
 nu=e
 if has(Gs('denom('+e+')'),v):
  nu=G('numer('+e+')')
  if isnum(nu):
   out(' '+(nm or ps(e))+_ne()+'0')
   return[]
 out(' '+ps(nu)+' = 0')
 fa=Gs('factor('+nu+')')
 if fa!=nu and(')*'in fa or '*('in fa)and('/'not in fa)and(len(split_terms(fa))==1):
  out(' '+pp(fa)+' = 0')
 P=_roots(e,v,dom)
 Q=_roots(e,v,ALL)if not P and dom!=ALL else[]
 out(' '+_lst(Q or P,v)+(' not in domain'if Q else ''))
 return P
def _okf(P,f,v):
 Q=[]
 for p in P:
  if _fl(_sub(f,v,p[1]))is None:
   out(' '+v+' = '+_d(p[1])+' not in domain')
  else:
   Q.append(p)
 return Q
def _tp(u,w):
 if u is None:
  return 0 if w is None else math.ceil(w)-1
 if w is None:
  return math.floor(u)+1
 m=(u+w)/2
 for k in(1,2,4,10,100):
  t=round(m*k)/k
  if u<t<w:
   return t
 return m
def _rows(P,dom,es,v,f):
 pts=[dom[0]]+[p for p in _uniq(P)if _in(p[0],dom,-1e-09)]+[dom[1]]
 R=[]
 for i in range(len(pts)-1):
  t=_tp(pts[i][0],pts[i+1][0])
  t=str(int(t))if t==int(t)else '%g'%t
  W=[]
  if _fl(_sub(f,v,t))is not None:
   for e in es:
    r=Gs('normal('+_sub(e,v,t)+')')
    x=_fl(r)
    if x is None:
     W.append(['undef',0])
    else:
     if not isnum(r)or '.'in r:
      r=sf3(x)
      if '.'in r and ' 'not in r:
       r=r.rstrip('0').rstrip('.')
     W.append([r,0 if abs(x)<1e-12 else 1 if x>0 else-1])
  R.append([pts[i],pts[i+1],t,W])
 return R
def _iv(r,v):
 lo=r[0]
 hi=r[1]
 if lo[0]is None and hi[0]is None:
  return 'all '+v
 if lo[0]is None:
  return v+' < '+_d(hi[1])
 if hi[0]is None:
  return v+' > '+_d(lo[1])
 return _d(lo[1])+' < '+v+' < '+_d(hi[1])
def _gt(s):
 return ' > 0'if s>0 else ' < 0'if s<0 else ' = 0'
def _prow(R,v,nms,tag):
 for r in R:
  s=_iv(r,v)+': '
  if not r[3]:
   s+='not in domain'
  else:
   s+=', '.join([nms[k]+'('+r[2]+') = '+r[3][k][0]+(_gt(r[3][k][1])if r[3][k][0]!='0'else '')for k in range(len(nms))])
   t=tag(r[3])
   s+=', '+t if t else ''
  out(s)
def _ivs(R,v,ok):
 s=[_iv(r,v)for r in R if r[3]and ok(r[3])]
 return ', '.join(s)if s else 'none'
def _side(R,x):
 a=b=None
 for r in R:
  if r[1][0]is not None and abs(r[1][0]-x)<1e-09:
   a=r
  if r[0][0]is not None and abs(r[0][0]-x)<1e-09:
   b=r
 return(a,b)
def _sg(r,k=0):
 return r[3][k][1]if r and r[3]else 0
def _ptans(lbl,x,y):
 out('ANS: '+lbl+' ('+_d(x)+', '+_d(y)+')')
 if not(isnum(x)and isnum(y))and '.'not in x+y:
  a=_fl(x)
  b=_fl(y)
  if a is not None and b is not None:
   out('     ~ ('+(x if isnum(x)and '/'not in x else sf3(a))+', '+(y if isnum(y)and '/'not in y else sf3(b))+')')
def _nat(f,fp,f2,v,dom,P):
 R=None
 for p in P:
  c=p[1]
  y=_ev('f',f,v,c)
  s=_fl(_ev("f''",f2,v,c,1))
  if s is not None and abs(s)>1e-09:
   t='max'if s<0 else 'min'
  else:
   if R is None:
    R=_rows(P+_sing(fp,v,dom),dom,[fp],v,f)
   L,Q=_side(R,p[0])
   out(', '.join(["f'("+r[2]+') = '+r[3][0][0]+_gt(r[3][0][1])for r in(L,Q)if r and r[3]]))
   a=_sg(L)
   b=_sg(Q)
   t='max'if a>0>b else 'min'if a<0<b else 'stationary inflexion'
   out('so '+t)
  _ptans(t+' at',c,y)
def _trig(f,dom):
 if dom[0][0]is None and('sin'in f or 'cos'in f or 'tan'in f):
  out('(periodic: give a domain)')
def stat():
 hdr('Stationary points')
 f,v=_getf('f(x) =','x')
 dom=_dom(f,v)
 _trig(f,dom)
 fp=_dv(f,v,"f'")
 f2=_dv(fp,v,"f''")
 out("f'("+v+') = 0:')
 P=_okf(_solve0(fp,v,dom,"f'("+v+')'),f,v)
 if not P:
  out('No stationary points')
 _nat(f,fp,f2,v,dom,P)
 out("Inflexion: f''("+v+') = 0:')
 Q=_solve0(f2,v,dom,"f''("+v+')')
 R=_rows(Q+_sing(f2,v,dom),dom,[f2],v,f)
 if f2=='0':
  out(' no point of inflexion')
 else:
  _prow(R,v,["f''"],lambda w:'concave '+('up'if w[0][1]>0 else 'down')if w[0][1]else '')
 for p in Q:
  L,U=_side(R,p[0])
  if _sg(L)*_sg(U)<0:
   _ptans('inflexion at',p[1],S(_sub(f,v,p[1])))
  else:
   out(v+' = '+_d(p[1])+": f'' has no sign change, so not an inflexion")
 out('ANS: concave up: '+_ivs(R,v,lambda w:w[0][1]>0))
 out('ANS: concave down: '+_ivs(R,v,lambda w:w[0][1]<0))
 wait()
def incdec():
 hdr('Increasing/decreasing')
 f,v=_getf('f(x) =','x')
 dom=_dom(f,v)
 _trig(f,dom)
 fp=_dv(f,v,"f'")
 out("f'("+v+') = 0:')
 P=_okf(_solve0(fp,v,dom,"f'("+v+')'),f,v)
 B=_uniq(_sing(fp,v,dom))
 if B:
  out("f' undefined: "+_lst(B,v))
 R=_rows(P+B,dom,[fp],v,f)
 _prow(R,v,["f'"],lambda w:'increasing'if w[0][1]>0 else 'decreasing'if w[0][1]else 'constant')
 out('ANS: increasing: '+_ivs(R,v,lambda w:w[0][1]>0))
 out('ANS: decreasing: '+_ivs(R,v,lambda w:w[0][1]<0))
 wait()
def kin():
 hdr('Kinematics s(t)')
 s,t=_getf('s(t) =','t')
 dom=_dom(s,t,t+' range','0,inf')
 v=_D(s,t)
 out('v('+t+') = ds/d'+t+' = '+ps(v))
 a=_D(v,t)
 out('a('+t+') = dv/d'+t+' = '+ps(a))
 out('At rest: v('+t+') = 0')
 P=_solve0(v,t,dom,'v('+t+')')
 t0=ask('At '+t+' = (blank=skip)','',0)
 if t0:
  t0=norm(t0)
  _ev('s',s,t,t0)
  u=_ev('v',v,t,t0)
  _ev('a',a,t,t0)
  ans('speed |v('+_d(t0)+')|',_pf(_t(S('abs('+u+')'))))
 R=_rows(P+_roots(a,t,dom)+_sing(v,t,dom),dom,[v,a],t,s)
 _prow(R,t,['v','a'],lambda w:'speeding up'if w[0][1]*w[1][1]>0 else 'slowing down'if w[0][1]*w[1][1]<0 else 'constant velocity'if w[0][1]else '')
 D=[]
 for p in P:
  L,U=_side(R,p[0])
  if _sg(L)*_sg(U)<0:
   D.append(p)
 out('ANS: at rest: '+_lst(P,t,'never'))
 out('ANS: changes direction: '+_lst(D,t,'never'))
 out('ANS: speeding up: '+_ivs(R,t,lambda w:w[0][1]*w[1][1]>0))
 out('ANS: slowing down: '+_ivs(R,t,lambda w:w[0][1]*w[1][1]<0))
 wait()
ITEMS=[('Stationary points',stat),('Increasing/decr.',incdec),('Kinematics s(t)',kin)]
