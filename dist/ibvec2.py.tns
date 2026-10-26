from ibcore import*
TITLE='Lines/planes'
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
 if len(v)!=3 or ''in v:
  raise ValueError('Bad 3D vector')
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
def _pn(c):
 return '('+ps(c)+')'if c[:1]=='-'or '/'in c or len(split_terms(c))>1 else pp(c)
def _pw(c):
 return pp(c)if c.isdigit()or c.isalpha()else '('+ps(c)+')'
def _f(a,b):
 return _pn(a)+'('+ps(b)+')'
def _add(a,b,k='1'):
 return[S('('+a[i]+')+('+k+')*('+b[i]+')')for i in range(3)]
def _df(l,P,Q,pre=''):
 R=_add(P,Q,'-1')
 out(l+' = '+pre+'('+', '.join([ps(P[i])+' - '+_pn(Q[i])for i in range(3)])+') = '+_vs(R))
 return R
def _lin(a,b,p='t'):
 return join_signed([pp(a),pp(S('('+b+')*'+p))])
def _z(v):
 return not[c for c in v if c!='0']
def _dot(u,v,l='',z=0):
 r=S('+'.join(['('+u[i]+')*('+v[i]+')'for i in range(3)]))
 if l:
  out(l+' = '+' + '.join([_f(u[i],v[i])for i in range(3)])+' = '+ps(r)+(' => perpendicular'if z and r=='0'else ''))
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
def _cross(u,v,l=''):
 t=[]
 w=[]
 for i,j in((1,2),(2,0),(0,1)):
  t.append(_f(u[i],v[j])+' - '+_f(u[j],v[i]))
  w.append(S('('+u[i]+')*('+v[j]+')-('+u[j]+')*('+v[i]+')'))
 if l:
  out(l+' = ('+', '.join(t)+')')
  out(' = '+_vs(w))
 return w
def _ang(c,f):
 r=S(f+'('+c+')')
 e='acos'not in r and 'asin'not in r and('.'not in r)
 t=_th()
 if not e or isnum(r):
  out(t+' = arc'+f[1:]+'('+pp(c)+')')
 d=F(r+'*180/pi')
 out('ANS: '+t+' = '+(pp(r)+' = 'if e and(not isnum(r))else '')+sf3(F(r))+' rad = '+(str(int(round(d)))if abs(d-round(d))<1e-09 else sf3(d))+' deg')
def _cart(s,k=''):
 ch=split_top(norm(s),',')
 q=split_top(ch[0],'=')
 fx={}
 for c in ch[1:]:
  z=split_top(c,'=')
  if len(z)==2:
   fx[z[0].strip()]=z[1]
 a=[]
 b=[]
 for w in X:
  p=[z for z in q if has(z,w)]
  if p:
   a.append(GL('solve('+p[0]+'=0,'+w+')')[0])
   b.append(N('1/('+D(p[0],w)+')'))
  else:
   a.append(S(fx[w]if w in fx else askn(w+' =')))
   b.append('0')
 out('a'+k+' = '+_vs(a)+', b'+k+' = '+_vs(b))
 return(a,b)
def _line(n='L',k=''):
 m=ask(n+': 1)a+tb 2)2 points 3)Cartesian','1',0)
 if m=='3':
  a,b=_cart(ask(n+' e.g. (x-1)/2=y/3=z','',n),k)
 else:
  p=m!='2'
  a=_v(n+(' point a'if p else ' point A'),('a'if p else 'A')+k)
  b=_v(' direction b'if p else ' point B',('b'if p else 'B')+k)
  if not p:
   b=_df('b'+k,b,a,'AB = ')
 if _z(b):
  raise ValueError('Bad line')
 return(a,b)
def _pl(s):
 s=s.replace(' ','')
 if s[:2]=='r.':
  q=split_top(s[2:],'=')
  return(_vp(q[0]),S(norm(q[1])))
 s=norm(s)
 if '='not in s:
  raise ValueError('Bad plane')
 E=lhs0(s)
 n=[S(D(E,w))for w in X]
 d=S('-('+G('subst('+E+',[x,y,z],[0,0,0])')+')')
 if[c for c in n if has(c,'x')or has(c,'y')or has(c,'z')]or _z(n):
  raise ValueError('Bad plane')
 return(n,d)
def _ce(n,d,k=-1):
 return join_signed([pp(S('('+n[i]+')*'+X[i]))for i in range(3)if i!=k])+' = '+pp(d)
def _eq(n,d,k=-1):
 return '+'.join(['('+n[i]+')*'+X[i]for i in range(3)if i!=k])+'='+d
def _peq(a,n,ds,pts):
 if not[c for c in n if not isnum(c)or '/'in c]:
  g=int(G('gcd('+n[0]+',gcd('+n[1]+','+n[2]+'))'))
  if[c for c in n if c!='0'][0][0]=='-':
   g=-g
  if g!=1:
   n=[S('('+c+')/('+str(g)+')')for c in n]
   out('n parallel to '+_vs(n))
 d=_dot(a,n,'r.n = a.n')
 out('r.'+_vs(n)+' = '+pp(d))
 if ds:
  out('r = '+_vs(a)+' + s'+_vs(ds[0])+' + t'+_vs(ds[1]))
 for P in pts:
  if S(_dot(P,n)+'-('+d+')')!='0':
   raise ValueError('check failed')
 out('ANS: '+_ce(n,d))
def plane_eq():
 hdr('Plane equation')
 o=ask('1)3 points 2)pt+normal 3)pt+2 dirs 4)line+pt 5)2 lines 6)Cartesian','1',0)
 ds=[]
 pts=[]
 if o=='6':
  n,d=_pl(ask('Plane ax+by+cz=d or r.n=d','',''))
  out('n = '+_vs(n))
  k=[i for i in range(3)if n[i]!='0'][0]
  a=['0']*3
  a[k]=S('('+d+')/('+n[k]+')')
  out('a = '+_vs(a)+'  ('+', '.join([X[i]+' = 0'for i in range(3)if i!=k])+')')
  E=[['1','0','0'],['0','1','0'],['0','0','1']]
  j=[i for i in range(3)if not _z(_cross(n,E[i]))][:2]
  ds=[_cross(n,E[i])for i in j]
  out('b = n'+_xs()+'ijk'[j[0]]+' = '+_vs(ds[0])+', c = n'+_xs()+'ijk'[j[1]]+' = '+_vs(ds[1]))
  out('ANS: r = '+_vs(a)+' + s'+_vs(ds[0])+' + t'+_vs(ds[1]))
  P=_v('test point P (blank=none)','P',1)
  if P:
   L=_dot(P,n,'n.P')
   k=S('('+L+')-('+d+')')=='0'
   out('ANS: '+pp(L)+(' = 'if k else ' != ')+pp(d)+' => P '+('on'if k else 'not on')+' plane')
  wait()
  return
 if o=='1':
  a=_v('A','A')
  B=_v('B','B')
  C=_v('C','C')
  pts=[a,B,C]
  ds=[_df('AB',B,a),_df('AC',C,a)]
  n=_cross(ds[0],ds[1],'n = AB'+_xs()+'AC')
 elif o=='2':
  a=_v('point a','a')
  n=_v('normal n','n')
 elif o=='3':
  a=_v('point a','a')
  ds=[_v('direction b','b'),_v('direction c','c')]
  n=_cross(ds[0],ds[1],'n = b'+_xs()+'c')
 elif o=='4':
  a,b=_line()
  P=_v('point P','P')
  pts=[a,P]
  ds=[b,_df('AP',P,a,'P - a = ')]
  n=_cross(b,ds[1],'n = b'+_xs()+'AP')
  if _z(n):
   out('P on line: plane not unique')
 else:
  a,b=_line('L1','1')
  c,d=_line('L2','2')
  pts=[a,c]
  n=_cross(b,d,'n = b1'+_xs()+'b2')
  ds=[b,d]
  if _z(n):
   out('b1'+_xs()+'b2 = 0: lines parallel')
   ds=[b,_add(c,a,'-1')]
   n=_cross(b,ds[1],'n = b1'+_xs()+'(a2 - a1)')
   if _z(n):
    out('lines coincide: plane not unique')
  elif _dot(_add(c,a,'-1'),n,'(a2 - a1).n')!='0':
   out('(a2 - a1).n != 0 => skew')
   n=['0']*3
 if _z(n):
  out('ANS: no unique plane')
 else:
  _peq(a,n,ds,pts)
 wait()
def _lp(a,b,n,d):
 p=[]
 for i in range(3):
  if n[i]!='0':
   e=_lin(a[i],b[i])
   c=''if n[i]=='1'else '-'if n[i]=='-1'else pp(n[i])
   c='('+c+')'if '/'in c else c
   m=' + 'in e or ' - 'in e
   p.append(c+(e if not m and(c==''or(e[:1]!='-'and(c=='-'or e[:1]in LET)))else '('+e+')'))
 out(join_signed(p)+' = '+pp(d))
 k=_dot(b,n)
 c=_dot(a,n)
 h=join_signed([pp(S('('+k+')*t')),pp(c)])+' = '+pp(d)
 if k=='0':
  out(h)
  out('ANS: '+('line lies in the plane'if c==d else 'line parallel to plane: no intersection'))
  return None
 t=N('(('+d+')-('+c+'))/('+k+')')
 out(h+' => t = '+pp(t))
 return t
def _rows(M):
 for r in M:
  out('['+', '.join([pp(c)for c in r[:3]])+' | '+pp(r[3])+']')
def _ro(q,f,r):
 g=f[1:]if f[:1]=='-'else f
 g=''if g=='1'else g if g.isdigit()else '('+pp(g)+')'
 return 'R%d -> R%d %s %sR%d'%(q+1,q+1,'+'if f[:1]=='-'else '-',g,r+1)
def _3pl():
 M=[]
 for i in range(3):
  n,d=_pl(ask('Plane '+str(i+1),'',''))
  M.append(n+[d])
 N0=[m[:3]for m in M]
 D_=S('det(['+','.join(['['+','.join(r[:3])+']'for r in M])+'])')
 k=GL('lname('+D_+')')
 out('det = '+pp(D_)+(''if D_=='0'or k else ' != 0 => unique point'))
 if k:
  k=k[0]
  ks=', '.join([pp(z)for z in GL('solve('+D_+'=0,'+k+')')])
  out('det = 0 => '+k+' = '+ks)
  return 'unique point if '+k+' != '+ks+' (re-enter with '+k+' value)'
 _rows(M)
 r=0
 for c in range(3):
  p=[q for q in range(r,3)if M[q][c]!='0']
  if not p:
   continue
  if p[0]!=r:
   M[r],M[p[0]]=(M[p[0]],M[r])
   out('R%d <-> R%d'%(r+1,p[0]+1))
   _rows(M)
  for q in range(r+1,3):
   f=N('('+M[q][c]+')/('+M[r][c]+')')
   if f!='0':
    M[q]=[S('('+M[q][j]+')-('+f+')*('+M[r][j]+')')for j in range(4)]
    out(_ro(q,f,r))
    _rows([M[q]])
  r+=1
 zr=[m for m in M if _z(m[:3])]
 if[m for m in zr if m[3]!='0']:
  out('0 = '+pp([m for m in zr if m[3]!='0'][0][3])+': inconsistent')
  pr=[1 for i,j in((0,1),(0,2),(1,2))if _z(_cross(N0[i],N0[j]))]
  return 'no common point ('+('parallel planes'if pr else 'triangular prism')+')'
 s=GL('linsolve(['+','.join([_eq(m[:3],m[3])for m in M if not _z(m[:3])])+'],[x,y,z])')
 if len(zr)==0:
  out('z = '+pp(s[2])+', y = '+pp(s[1])+', x = '+pp(s[0]))
  return 'point '+_vs(s)
 if len(zr)==2:
  return 'planes coincide (one plane)'
 w=[X[i]for i in range(3)if s[i]==X[i]][0]
 a=[S('subst('+c+','+w+'=0)')for c in s]
 b=[S('diff('+c+','+w+')')for c in s]
 out('0 = 0: let '+w+' = t')
 out(', '.join([X[i]+' = '+_lin(a[i],b[i])for i in range(3)]))
 return 'line r = '+_vs(a)+' + t'+_vs(b)
def plane_int():
 hdr('Plane intersect')
 o=ask('1)line-plane 2)angle line-plane 3)angle planes 4)2 planes 5)3 planes 6)point-plane','1',0)
 if o=='5':
  out('ANS: '+_3pl())
  wait()
  return
 if o in '12':
  a,b=_line()
 if o=='6':
  P=_v('point P','P')
 n,d=_pl(ask('Plane ax+by+cz=d or r.n=d','',''))
 if o=='1':
  t=_lp(a,b,n,d)
  if t:
   out('ANS: P = '+_vs(_add(a,b,t)))
 elif o=='2':
  k=_dot(b,n,'b.n')
  mb=_mag(b,'|b|')
  mn=_mag(n,'|n|')
  c=N('abs('+k+')/(('+mb+')*('+mn+'))')
  out('sin '+_th()+' = |b.n|/(|b||n|) = '+pp(S('abs('+k+')'))+'/('+pp(mb)+_xs()+pp(mn)+') = '+pp(c))
  _ang(c,'asin')
 elif o=='6':
  out('PF: r = '+_vs(P)+' + t'+_vs(n))
  t=_lp(P,n,n,d)
  if t:
   F_=_add(P,n,t)
   out('ANS: foot F = '+_vs(F_))
   ans('distance |PF|',_mag(_add(F_,P,'-1'),'|PF|',0))
   out("ANS: reflection P' = 2F - P = "+_vs(_add(_add(F_,F_),P,'-1')))
 else:
  m,e=_pl(ask('Plane 2','',''))
  if o=='3':
   k=_dot(n,m,'n1.n2',1)
   if k=='0':
    _ang('0','acos')
   else:
    m1=_mag(n,'|n1|')
    m2=_mag(m,'|n2|')
    c=N('abs('+k+')/(('+m1+')*('+m2+'))')
    out('cos '+_th()+' = |n1.n2|/(|n1||n2|) = '+pp(S('abs('+k+')'))+'/('+pp(m1)+_xs()+pp(m2)+') = '+pp(c))
    _ang(c,'acos')
  else:
   w=_cross(n,m,'direction = n1'+_xs()+'n2')
   if _z(w):
    k=[i for i in range(3)if n[i]!='0'][0]
    f=N('('+m[k]+')/('+n[k]+')')
    out('ANS: planes '+('coincide'if S('('+e+')-('+f+')*('+d+')')=='0'else 'parallel: no intersection'))
   else:
    k=[i for i in(2,1,0)if w[i]!='0'][0]
    s=GL('linsolve(['+_eq(n,d,k)+','+_eq(m,e,k)+'],['+','.join([X[i]for i in range(3)if i!=k])+'])')
    a=['0']*3
    j=0
    for i in range(3):
     if i!=k:
      a[i]=s[j]
      j+=1
    out('let '+X[k]+' = 0: '+_ce(n,d,k)+', '+_ce(m,e,k))
    out(', '.join([X[i]+' = '+pp(a[i])for i in range(3)if i!=k]))
    out('ANS: r = '+_vs(a)+' + t'+_vs(w))
 wait()
ITEMS=[('Plane equation',plane_eq),('Plane intersect',plane_int)]
