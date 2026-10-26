from ibcore import*
TITLE='Vectors'
X='xyz'
def _s(a,b):
 return a if CFG['uni']else b
def _th():
 return _s('θ','theta')
def _xs():
 return _s(' × ',' x ')
def _rt(t):
 return _s('√','sqrt')+'('+t+')'
def _vp(s):
 s=s.strip()
 if s[:1]in LET and s[1:2]=='(':
  s=s[1:]
 if s[:1]in '(['and s[-1:]in ')]':
  s=s[1:-1]
 v=[norm(c)for c in split_top(s,',')]
 if len(v)<2 or len(v)>3 or ''in v:
  raise ValueError('Bad vector')
 return[S(c)for c in v]
def _vs(v):
 return '('+', '.join([ps(c)for c in v])+')'
def _v(p,l='',o=0):
 s=ask(p,'',0).strip()
 if not s and o:
  return None
 v=_vp(s)
 if l:
  out(l+' = '+_vs(v))
 return v
def _ec(L,V):
 for i in range(len(L)):
  out(L[i]+' = '+_vs(V[i]))
def _pn(c):
 return '('+ps(c)+')'if c[:1]=='-'or '/'in c or len(split_terms(c))>1 else pp(c)
def _pw(c):
 return pp(c)if c.isdigit()or c.isalpha()else '('+ps(c)+')'
def _f(a,b):
 return _pn(a)+'('+ps(b)+')'
def _kv(k,w):
 if k in('1','-1'):
  return k[:-1]+w
 t=pp(k)
 return(t if isnum(k)and '/'not in t else '('+t+')')+w
def _add(a,b,k='1'):
 if len(a)!=len(b):
  raise ValueError('2D/3D mix')
 return[S('('+a[i]+')+('+k+')*('+b[i]+')')for i in range(len(a))]
def _df(l,P,Q,pre='',e=1):
 R=_add(P,Q,'-1')
 out(l+' = '+pre+'('+', '.join([ps(P[i])+' - '+_pn(Q[i])for i in range(len(P))])+')'+(' = '+_vs(R)if e else ''))
 return R
def _lin(a,b,p='t'):
 return join_signed([pp(a),pp(S('('+b+')*'+p))])
def _isx(r):
 return 'acos'not in r and 'asin'not in r and('.'not in r)
def _dt(u,v):
 return ' + '.join([_f(u[i],v[i])for i in range(len(u))])
def _dot(u,v,l='u.v',z=0):
 if len(u)!=len(v):
  raise ValueError('2D/3D mix')
 r=N('+'.join(['('+u[i]+')*('+v[i]+')'for i in range(len(u))]))
 if l:
  out(l+' = '+_dt(u,v)+' = '+ps(r)+(' => perpendicular'if z and r=='0'else ''))
 return r
def _mag(u,l='',e=1):
 s=S('+'.join(['('+c+')^2'for c in u]))
 m=S('sqrt('+s+')')
 if l:
  t=[_rt(' + '.join([_pw(c)+'^2'for c in u])),_rt(pp(s)),pp(m)]
  if t[2]==t[1]:
   t.pop()
  elif s in('0','1'):
   t.pop(1)
  if not e:
   t.pop()
  out(l+' = '+' = '.join(t))
 return m
def _cross(u,v,l='',f=0):
 u=u+['0']*(3-len(u))
 v=v+['0']*(3-len(v))
 t=[]
 w=[]
 for i,j in((1,2),(2,0),(0,1)):
  t.append(_f(u[i],v[j])+' - '+_f(u[j],v[i]))
  w.append(S('('+u[i]+')*('+v[j]+')-('+u[j]+')*('+v[i]+')'))
 if l:
  out(l+' = ('+', '.join(t)+')')
  out(('ANS: '+l+' = 'if f else ' = ')+_vs(w))
 return w
def _par(u,v):
 if len(u)!=len(v):
  raise ValueError('2D/3D mix')
 k=[N('('+v[i]+')/('+u[i]+')')for i in range(len(u))if u[i]!='0'][0]
 for i in range(len(u)):
  if S('('+v[i]+')-('+k+')*('+u[i]+')')!='0':
   return None
 return k
def _dg(r):
 d=F(r+'*180/pi')
 return str(int(round(d)))if abs(d-round(d))<1e-09 else sf3(d)
def _ang(c):
 r=S('acos('+c+')')
 e=_isx(r)
 t=_th()
 if not e or isnum(r):
  out(t+' = arccos('+pp(c)+')')
 out('ANS: '+t+' = '+(pp(r)+' = 'if e and(not isnum(r))else '')+sf3(F(r))+' rad = '+_dg(r)+' deg')
def _uv(k):
 u=_v('u or A (x,y,z)')
 v=_v('v or B')
 C=_v('C (blank=none)','',1)
 n=['u','v']
 if C:
  _ec(['A','B','C'],[u,v,C])
  P=v if k else u
  n=['BA','BC']if k else['AB','AC']
  u,v=(_df(n[0],u if k else v,P),_df(n[1],C,P))
 else:
  _ec(n,[u,v])
 return(u,v,n)
def _ks(e,rs):
 if not has(e,'k'):
  return rs if e=='0'else[]
 r=[z for z in GL('solve('+e+'=0,k)')if F(z)is not None]
 if rs is None:
  return r
 return[z for z in rs if[y for y in r if abs(F(y)-F(z))<1e-09]]
def vec_ops():
 hdr('Vectors')
 o=ask('1)AB,|v| 2)parallel 3)angle 4)cross/area 5)find k','1',0)
 if o=='1':
  A=_v('A or v (x,y,z)')
  B=_v('B (blank=none)','',1)
  u=A
  n='v'
  if B:
   _ec(['A','B'],[A,B])
   n='AB'
   u=_df('AB',B,A,'OB - OA = ',0)
   out('ANS: AB = '+_vs(u))
  else:
   out('v = '+_vs(A))
  m=_mag(u,'|'+n+'|',0)
  ans('|'+n+'|',m)
  e=[]
  if m!='0':
   e=[N('('+c+')/('+m+')')for c in u]
   out('unit = (1/'+_pn(m)+')'+_vs(u)+' = '+_vs(e))
  if B:
   out('M = ('+', '.join(['('+ps(A[i])+' + '+_pn(B[i])+')/2'for i in range(len(A))])+') = '+_vs([S('(('+A[i]+')+('+B[i]+'))/2')for i in range(len(A))]))
  L=askn('Length L (blank=none)','','L')
  if L and e:
   out(pp(L)+_xs()+'unit = '+_pn(L)+_vs(e))
   out('ANS: '+pp(L)+_xs()+'unit = '+_vs([N('('+L+')*('+c+')')for c in e]))
 elif o=='2':
  u=_v('u','u')
  v=_v('v','v')
  if len(u)!=len(v):
   raise ValueError('2D/3D mix')
  out('u = kv')
  rs=[]
  ok=True
  for i in range(len(u)):
   h=pp(u[i])+' = '+pp(S('('+v[i]+')*k'))
   if v[i]=='0':
    z=u[i]=='0'
    ok=ok and z
    out(h+(' true'if z else ' false'))
   else:
    rs.append(N('('+u[i]+')/('+v[i]+')'))
    out(h+' => k = '+pp(rs[-1]))
  for r in rs:
   ok=ok and S('('+r+')-('+rs[0]+')')=='0'
  if ok and rs:
   out('ANS: u = '+_kv(rs[0],'v')+' => parallel')
  else:
   out('ANS: not parallel')
 elif o=='3':
  u,v,n=_uv(1)
  d=_dot(u,v,n[0]+'.'+n[1],1)
  if d=='0':
   out('ANS: '+_th()+' = '+pp('pi/2')+' = 90 deg')
  else:
   mu=_mag(u,'|'+n[0]+'|')
   mv=_mag(v,'|'+n[1]+'|')
   c=N('('+d+')/(('+mu+')*('+mv+'))')
   out('cos '+_th()+' = '+pp(d)+'/('+pp(mu)+_xs()+pp(mv)+') = '+pp(c))
   _ang(c)
 elif o=='4':
  u,v,n=_uv(0)
  w=n[0]+_xs()+n[1]
  c=_cross(u,v,w,1)
  m=_mag(c,'|'+w+'|',0)
  ans('parallelogram area',m)
  ans('triangle area = |'+w+'|/2',S('('+m+')/2'))
 else:
  c=ask('1)perp 2)parallel 3)|u| = m','1',0)
  u=_v('u (with k)','u')
  v=_v('v','v')if c!='3'else u
  if c=='2':
   rs=None
   u=u+['0']*(3-len(u))
   v=v+['0']*(3-len(v))
   out('u'+_xs()+'v = 0')
   for i,j in((0,1),(0,2),(1,2)):
    e=N('('+u[i]+')*('+v[j]+')-('+u[j]+')*('+v[i]+')')
    if e!='0':
     out(_f(u[i],v[j])+' - '+_f(u[j],v[i])+' = 0 => '+ps(e)+' = 0')
     rs=_ks(e,rs)
  elif c=='3':
   m=askn('|u| =','','|u|')
   q=' + '.join([_pw(z)+'^2'for z in u])
   e=S('+'.join(['('+z+')^2'for z in u])+'-('+m+')^2')
   out(_rt(q)+' = '+pp(m))
   out(q+' = '+_pw(m)+'^2')
   out(ps(e)+' = 0')
   rs=_ks(e,None)
  else:
   out('u.v = '+_dt(u,v)+' = 0')
   e=_dot(u,v,'')
   out(ps(e)+' = 0')
   rs=_ks(e,None)
  out('ANS: '+('k = '+' or '.join([pp(z)for z in rs])if rs else 'no value of k'))
 wait()
def _cart(s,k=''):
 ch=split_top(norm(s),',')
 ps_=split_top(ch[0],'=')
 fx={}
 for c in ch[1:]:
  q=split_top(c,'=')
  if len(q)==2:
   fx[q[0].strip()]=q[1]
 a=[]
 b=[]
 for w in X:
  p=[z for z in ps_ if has(z,w)]
  if p:
   a.append(GL('solve('+p[0]+'=0,'+w+')')[0])
   b.append(N('1/('+D(p[0],w)+')'))
  elif w in fx or w!='z':
   a.append(S(fx[w]if w in fx else askn(w+' =')))
   b.append('0')
 out('a'+k+' = '+_vs(a)+', b'+k+' = '+_vs(b))
 return(a,b)
def _line(n='L',k=''):
 m=ask(n+': 1)a+tb 2)2 points 3)Cartesian','1',0)
 if m=='3':
  return _cart(ask(n+' e.g. (x-1)/2=y/3=z','',n),k)
 p=m!='2'
 a=_v(n+(' point a'if p else ' point A'),('a'if p else 'A')+k)
 b=_v(' direction b'if p else ' point B',('b'if p else 'B')+k)
 if not p:
  b=_df('b'+k,b,a,'AB = ')
 if len(a)!=len(b)or not[z for z in b if z!='0']:
  raise ValueError('Bad line')
 return(a,b)
def _eqt(a,b,c,d,p='t'):
 if len(a)!=len(c):
  raise ValueError('2D/3D mix')
 ts=[]
 ok=True
 for i in range(len(a)):
  k=S('('+b[i]+')-('+d[i]+')')
  h=_lin(a[i],b[i],p)+' = '+_lin(c[i],d[i],p)
  if k=='0':
   z=S('('+a[i]+')-('+c[i]+')')=='0'
   ok=ok and z
   out(h+(' true'if z else ' false'))
  else:
   ts.append(N('(('+c[i]+')-('+a[i]+'))/('+k+')'))
   out(h+' => '+p+' = '+pp(ts[-1]))
 for t in ts:
  ok=ok and abs(F(t)-F(ts[0]))<1e-09
 return ts[0]if ok and ts else None if ts or not ok else '0'
def _foot(a,b,P,k=''):
 if len(a)!=len(P):
  raise ValueError('2D/3D mix')
 f=_add(a,b,'t')
 out('F = '+_vs(f))
 g=[N('('+f[i]+')-('+P[i]+')')for i in range(len(a))]
 out('PF = F - P = '+_vs(g))
 e=_dot(g,b,'')
 t=GL('solve('+e+'=0,t)')[0]
 out('PF.b'+k+' = 0 => '+ps(e)+' = 0 => t = '+pp(t))
 f=_add(a,b,t)
 out('ANS: foot F = '+_vs(f))
 g=_add(f,P,'-1')
 out('PF = '+_vs(g))
 ans('distance |PF|',_mag(g,'|PF|',0))
def line_ops():
 hdr('Lines')
 o=ask('1)equation 2)P on line? 3)angle 4)L1 vs L2 5)foot/distance','1',0)
 k='1'if o in '345'else ''
 a,b=_line('L'+k,k)
 if o=='1':
  out('ANS: r = '+_vs(a)+' + t'+_vs(b))
  out(', '.join([X[i]+' = '+_lin(a[i],b[i])for i in range(len(a))]))
  cs=[]
  fx=[]
  for i in range(len(a)):
   if b[i]=='0':
    fx.append(X[i]+' = '+pp(a[i]))
   else:
    w=join_signed([X[i],pp(S('-('+a[i]+')'))])
    w=w if a[i]=='0'else '('+w+')'
    cs.append(w+(''if b[i]=='1'else '/'+_pn(b[i])))
  out(', '.join(([' = '.join(cs)]if len(cs)>1 else[])+fx))
 elif o=='2':
  P=_v('point P','P')
  t=_eqt(a,b,P,['0']*len(P))
  out('ANS: '+('P on line (t = '+pp(t)+')'if t else 'P not on line'))
 elif o=='3':
  c,d=_line('L2','2')
  m=_dot(b,d,'b1.b2',1)
  if m=='0':
   _ang('0')
  else:
   m1=_mag(b,'|b1|')
   m2=_mag(d,'|b2|')
   r=N('abs('+m+')/(('+m1+')*('+m2+'))')
   out('cos '+_th()+' = |b1.b2|/(|b1||b2|) = '+pp(S('abs('+m+')'))+'/('+pp(m1)+_xs()+pp(m2)+') = '+pp(r))
   _ang(r)
 elif o=='4':
  c,d=_line('L2','2')
  q=_par(b,d)
  if q:
   out('b2 = '+_kv(q,'b1')+' => parallel')
   t=_eqt(a,b,c,['0']*len(c))
   out('ANS: '+('coincident (a2 on L1)'if t else 'parallel, distinct'))
  else:
   n=len(a)
   out('L1 = L2:')
   for i in range(n):
    out(' '+_lin(a[i],b[i])+' = '+_lin(c[i],d[i],'s')+'  ('+'i'*(i+1)+')')
   for i,j,k in((0,1,2),(0,2,1),(1,2,0)):
    if j<n and S('('+b[j]+')*('+d[i]+')-('+b[i]+')*('+d[j]+')')!='0':
     break
   q='('+'i'*(i+1)+'),('+'i'*(j+1)+')'
   e=[a[z]+'+('+b[z]+')*t='+c[z]+'+('+d[z]+')*s'for z in(i,j)]
   t,s=GL('linsolve(['+','.join(e)+'],[t,s])')
   out('from '+q+': t = '+pp(t)+', s = '+pp(s))
   ok=1
   if n==3:
    L=S('('+a[k]+')+('+b[k]+')*('+t+')')
    R=S('('+c[k]+')+('+d[k]+')*('+s+')')
    ok=S('('+L+')-('+R+')')=='0'
    out('('+'i'*(k+1)+'): '+pp(L)+' = '+pp(R)+(' true'if ok else ' false'))
   out('ANS: '+('intersect at '+_vs(_add(a,b,t))if ok else 'skew lines'))
 else:
  P=_v('point P (blank: 2nd line)','P',1)
  if P:
   _foot(a,b,P,'1')
  else:
   c,d=_line('L2','2')
   q=_par(b,d)
   if q:
    out('b2 = '+_kv(q,'b1')+' => parallel')
    out('P = a2 = '+_vs(c))
    _foot(a,b,c,'1')
   else:
    P=_add(a,b,'t')
    Q=_add(c,d,'s')
    out('P = '+_vs(P)+', Q = '+_vs(Q))
    f=[N('('+Q[i]+')-('+P[i]+')')for i in range(len(a))]
    out('PQ = Q - P = '+_vs(f))
    e1=_dot(f,b,'')
    e2=_dot(f,d,'')
    out('PQ.b1 = 0 => '+ps(e1)+' = 0')
    out('PQ.b2 = 0 => '+ps(e2)+' = 0')
    t,s=GL('linsolve(['+e1+'=0,'+e2+'=0],[t,s])')
    out('t = '+pp(t)+', s = '+pp(s))
    P=_add(a,b,t)
    Q=_add(c,d,s)
    out('P = '+_vs(P)+', Q = '+_vs(Q))
    ans('shortest distance |PQ|',_mag(_add(Q,P,'-1'),'|PQ|',0))
 wait()
def _rv(l,a,v):
 out(l+' = '+_vs(a)+' + t'+_vs(v))
def kinem():
 hdr('Vector motion')
 o=ask('1)position 2)at P? 3)closest 4)collide 5)v from speed','1',0)
 if o=='5':
  sp=askn('speed','','speed')
  d=_v('direction','d')
  m=_mag(d,'|d|')
  v=[N('('+sp+')*('+z+')/('+m+')')for z in d]
  out('v = ('+pp(sp)+'/'+_pn(m)+')'+_vs(d))
  out('ANS: v = '+_vs(v))
  wait()
  return
 p='A: 'if o>'2'else ''
 a=_v(p+'position at t=0')
 v=_v(p+'velocity')
 _rv('r'+p[:1],a,v)
 if o=='1':
  ans('speed',_mag(v,'speed = |v|',0))
  t=askn('time t (blank=none)','','t')
  if t:
   r=_add(a,v,t)
   out('r('+pp(t)+') = ('+', '.join([ps(a[i])+' + '+(_pn(v[i])if t=='1'else _pn(t)+'('+ps(v[i])+')')for i in range(len(a))])+')')
   out('ANS: r('+pp(t)+') = '+_vs(r))
 elif o=='2':
  t=_eqt(a,v,_v('point P','P'),['0']*len(a))
  out('ANS: '+('at P when t = '+pp(t)if t else 'never at P'))
 else:
  c=_v('B: position at t=0')
  d=_v('B: velocity')
  _rv('rB',c,d)
  if o=='4':
   out('rA = rB')
   t=_eqt(a,v,c,d)
   if t and F(t)>=0:
    out('ANS: collide at t = '+pp(t)+', '+_vs(_add(a,v,t)))
   else:
    out('ANS: no collision')
  else:
   f=[N('('+c[i]+')+('+d[i]+')*t-('+a[i]+')-('+v[i]+')*t')for i in range(len(a))]
   out('rB - rA = '+_vs(f))
   D2=N('+'.join(['('+z+')^2'for z in f]))
   out('D^2 = '+' + '.join([_pw(z)+'^2'for z in f])+' = '+ps(D2))
   if not has(D2,'t'):
    ans('constant distance',S('sqrt('+D2+')'))
   else:
    g=N(D(D2,'t'))
    t=GL('solve('+g+'=0,t)')[0]
    out('d(D^2)/dt = '+ps(g)+' = 0 => t = '+pp(t))
    if F(t)<0:
     out('t < 0: for t >= 0 min at t = 0')
     t='0'
    out('A at '+_vs(_add(a,v,t))+', B at '+_vs(_add(c,d,t)))
    m=N('subst('+D2+',t='+t+')')
    r=S('sqrt('+m+')')
    if r!='sqrt('+m+')':
     out('D = '+_rt(pp(m)))
    ans('D_min',r)
 wait()
ITEMS=[('Vector ops',vec_ops),('Lines',line_ops),('Vector motion',kinem)]
