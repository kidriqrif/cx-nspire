from ibcore import*
TITLE='Trig values/ident'
SG={'sin':'++--','cos':'+--+','tan':'+-+-'}
BS={'sec':'cos','csc':'sin','cot':'tan'}
INV={'asin':'sin','acos':'cos','atan':'tan'}
TF=('sin','cos','tan','sec','csc','cot')
NM={'s':'sin','c':'cos','t':'tan'}
RC={'sec':'1/cosA','csc':'1/sinA','cot':'cosA/sinA','tan':'sinA/cosA'}
def _isx(r):
 for k in('sin(','cos(','tan(','.'):
  if k in r:
   return False
 return True
def _S(e):
 r=S(e)
 if has_var(r):
  return r
 if not _isx(r):
  t=Gs('normal(texpand('+r+'))')
  if t and _isx(t):
   r=t
 if '+'in r[1:]or '-'in r[1:]:
  f=Gs('factor('+r+')')
  if f and len(f)<len(r):
   r=f
 return r
def _q(r):
 if _isx(r)and len(r)<24:
  return ps(r)
 v=F(r)
 return pp(r)if v is None else sf3(v)
def _sh(l,e,p=1):
 r=_S(e)
 if p:
  out(l+' = '+_q(r))
 return r
def _pr(v):
 return v if isnum(v)and '/'not in v and(v[0]!='-')else '('+v+')'
def _pv(v):
 return pp(_pr(v))
def _bx(v,y=0):
 c=_fn(v)
 if c and c[0]in TF or(y and v[0]!='-'):
  return pp(v)
 return '('+ps(v)+')'
def _pf(p,q):
 if has(p)and(not has(q)):
  p,q=(q,p)
 if p=='1'and has(q):
  return _bx(q)
 return _bx(p)+_bx(q)
def _fa(n,X):
 return n+(' '+X if X in('A','B')else '('+pp(X)+')')
def _fn(g):
 k=g.find('(')
 if k<=0 or g[-1]!=')':
  return None
 d=0
 for j in range(k,len(g)):
  if g[j]in OPN:
   d+=1
  elif g[j]in CLS:
   d-=1
   if d==0 and j<len(g)-1:
    return None
 return[g[:k],g[k+1:-1]]
def _dv(a,b):
 if F(b)==0:
  return 'undefined'
 return _S('normal(('+a+')/('+b+'))')
def _calls(s):
 r=[]
 i=0
 n=len(s)
 while i<n-3:
  w=s[i:i+3]
  if w in TF and s[i+3]=='('and(i==0 or s[i-1]not in LET):
   d=0
   j=i+3
   while j<n:
    if s[j]=='(':
     d+=1
    elif s[j]==')':
     d-=1
     if d==0:
      break
    j+=1
   r.append([w,s[i+4:j],i,j+1])
   i=j+1
  else:
   i+=1
 return r
def _rt(l,c2,g,o,q):
 r=_S('normal('+g+'sqrt('+c2+'))')
 s=pp(g.strip('+')+'sqrt('+c2+')')
 t=l+' = '+s
 if _q(r)!=s:
  t+=' = '+_q(r)
 out(t+'  (Q'+str(q)+': '+o+(' > 0)'if g=='+'else ' < 0)'))
 return r
def _rat(f,v,q,x='x',w='sct'):
 if f in BS:
  b=BS[f]
  v=_sh(b+' '+x+' = 1/'+f.replace('csc','cosec')+' '+x,'1/('+v+')')
  f=b
 y=F(v)
 if y is None:
  out('Bad value')
  return None
 if f!='tan'and abs(y)>1+1e-12:
  out('|'+f+' '+x+'| > 1: impossible')
  return None
 if y!=0 and(y>0)!=(SG[f][q-1]=='+'):
  out('Wrong sign for Q'+str(q))
  return None
 r={f[0]:v}
 if f=='tan':
  s2=_sh('sec^2 '+x+' = 1 + tan^2 '+x+' = 1 + '+_pv(v)+'^2','1+('+v+')^2')
  sc=_rt('sec '+x,s2,SG['cos'][q-1],'cos',q)
  r['c']=_sh('cos '+x+' = 1/sec '+x,'normal(1/('+sc+'))')
  r['s']=_sh('sin '+x+' = tan '+x+' cos '+x+(''if v in('0','1')else ' = '+_pv(v)+'('+pp(r['c'])+')'),'normal(('+v+')*('+r['c']+'))')
 else:
  o='cos'if f=='sin'else 'sin'
  c2=_sh(o+'^2 '+x+' = 1 - '+f+'^2 '+x+' = 1 - '+_pv(v)+'^2','1-('+v+')^2')
  r[o[0]]=_rt(o+' '+x,c2,SG[o][q-1],o,q)
  r['t']=_dv(r['s'],r['c'])
  if 't'in w:
   out('tan '+x+' = sin '+x+'/cos '+x+' = '+_q(r['t']))
 if w=='sct':
  out('sec '+x+' = '+_q(_dv('1',r['c']))+', cosec '+x+' = '+_q(_dv('1',r['s']))+', cot '+x+' = '+_q(_dv(r['c'],r['s'])))
 return r
def _cmp(f,g,va,vb,nm,p=1,an=None,lb=''):
 h='-'if g=='+'else '+'
 A,B=an or('A','B')
 z=''if an else ' '
 if an:
  nm=pp(A)+' '+g+' '+pp(B)
 if f=='tan':
  a,b=(va['t'],vb['t'])
  y=has(a)or has(b)
  ta,tb=(_fa('tan',A),_fa('tan',B))
  d='('+ta+' '+g+' '+tb+')/(1 '+h+' '+ta+z+tb+')'
  e='(('+a+')'+g+'('+b+'))/(1'+h+'('+a+')*('+b+'))'
  w='('+_bx(a,y)+' '+g+' '+_bx(b,y)+')/(1 '+h+' '+_pf(a,b)+')'
 else:
  k='sccs'if f=='sin'else 'ccss'
  j=g if f=='sin'else h
  d=_fa(NM[k[0]],A)+z+_fa(NM[k[1]],B)+' '+j+' '+_fa(NM[k[2]],A)+z+_fa(NM[k[3]],B)
  e='('+va[k[0]]+')*('+vb[k[1]]+')'+j+'('+va[k[2]]+')*('+vb[k[3]]+')'
  w=_pf(va[k[0]],vb[k[1]])+' '+j+' '+_pf(va[k[2]],vb[k[3]])
 r=_sh('',e,0)
 out(f+'('+nm+') = '+d+('  (compound angle)'if an else ''))
 if p or ps(r).replace(' ','')!=w.replace(' ',''):
  out(' = '+w+lb)
 if p:
  out(' = '+_q(r))
 return r
def _val(e,dg):
 c=_fn(e)
 if not c or not(c[0]in SG or c[0]in BS):
  out('Use f(angle)')
  return
 f,t=c
 if F(t)is None:
  out('Bad angle')
  return
 fd='cosec'if f=='csc'else f
 k=t[:2]=='2*'
 a=_fn(t[2:]if k else t)
 if a and a[0]in INV:
  q=1 if F(a[1])>=0 else 2 if a[0]=='acos'else 4
  b=INV[a[0]]
  out('Let x = '+pp(a[0]+'('+a[1]+')')+': '+b+' x = '+pp(a[1])+', Q'+str(q))
  w=BS.get(f,f)[0]
  r=_rat(b,a[1],q,'x','sc'if k else w)
  if r:
   if k:
    r=_d2(r,b,w)
   b=BS.get(f,f)
   v=r[b[0]]if f==b else _dv('1',r[b[0]])
   ans(pp(e),_js(v))
  return
 P2,HP,U=('360','180','*pi/180')if dg else('2*pi','pi','')
 n=int((F(t)/F(P2)+1e-12)//1)
 t0=t
 if n:
  t0=_S(t+'-('+str(n)+')*'+P2)
  out(fd+'('+pp(t)+') = '+fd+'('+pp(t0)+')  (period)')
 m=2*F(t0)/F(HP)
 k=int(round(m))
 if abs(m-k)<1e-09:
  X,Y=[('1','0'),('0','1'),('-1','0'),('0','-1')][k%4]
  out(pp(t0)+': (cos, sin) = ('+X+', '+Y+')')
  b=BS.get(f,f)
  n,d={'sin':(Y,'1'),'cos':(X,'1'),'tan':(Y,X)}[b]
  ans(pp(e),_dv(n,d)if f==b else _dv(d,n))
  return
 q=int(m)+1
 al=_S([t0,HP+'-('+t0+')','('+t0+')-'+HP,P2+'-('+t0+')'][q-1])
 b=BS.get(f,f)
 g=SG[b][q-1]
 if q>1:
  out(pp(t0)+' in Q'+str(q)+', ref angle '+pp(al))
  out(b+(' > 0'if g=='+'else ' < 0')+' in Q'+str(q))
  out(fd+'('+pp(t0)+') = '+g.strip('+')+fd+'('+pp(al)+')')
 z='('+al+')'+U
 v=_S(g.strip('+')+('normal(1/'+b+'('+z+'))'if f!=b else f+'('+z+')'))
 ans(pp(e),_js(v)if _isx(v)else sf3(F(v)))
def _js(r):
 t=split_terms(str(r))
 if len(t)==2 and t[0][0]=='-'and(t[1][0]!='-'):
  t.reverse()
 return join_signed(t)
def _inv(e,dg):
 c=_fn(e)
 if not c or c[0]not in INV:
  out('Use arcsin(v) etc')
  return
 f,v=c
 b=INV[f]
 x=F(v)
 if x is None:
  out('Bad value')
  return
 if b!='tan'and abs(x)>1:
  out('|v| > 1: undefined')
  return
 q=''if b=='tan'else '='
 lo,hi=('0','pi')if b=='cos'else('-pi/2','pi/2')
 if dg:
  lo,hi=[z.replace('pi/2','90').replace('pi','180')for z in(lo,hi)]
 out('y = '+pp(e)+': '+b+' y = '+pp(v)+', '+pp(lo)+' <'+q+' y <'+q+' '+pp(hi))
 D='*180/pi'if dg else ''
 al=_S(f+'(abs('+v+'))'+D)
 r=al
 if x<0:
  out('ref angle = arc'+b+'('+pp(_S('abs('+v+')'))+') = '+_q(al))
  h=('180'if dg else 'pi')if b=='cos'else ''
  r=_S(h+'-('+al+')')
  out('y = '+(pp(h)+' - 'if h else '-')+_q(al))
 ans(pp(e),sf3(F(r))if '.'in r or(x>=0 and(not _isx(r)))else _js(r))
def _gr(n):
 s=norm(ask(n+' e.g. sin('+n+')=3/5','',0))
 k=s.find('=')
 c=_fn(s[:k])
 f=c[0]if c else s[:k]
 q=int(ask('Quadrant of '+n+' (1-4)','1',0))
 if k<0 or(f not in SG and f not in BS)or q<1 or(q>4):
  out('Bad input')
  return(None,f,q)
 out(pp(s[:k])+' = '+pp(s[k+1:])+', '+n+' in Q'+str(q))
 return(_rat(f,s[k+1:],q,n),f,q)
def _d2(r,b,w='sct'):
 s,c=(r['s'],r['c'])
 t='t'in w
 s2=_sh('sin 2x = 2 sin x cos x = 2('+pp(s)+')('+pp(c)+')','2*('+s+')*('+c+')','s'in w or t)
 l={'sin':'1 - 2sin^2 x','cos':'2cos^2 x - 1'}.get(b,'cos^2 x - sin^2 x')
 y=l.replace('sin^2 x',_pr(s)+'^2').replace('cos^2 x',_pr(c)+'^2')
 c2=_sh('cos 2x = '+l+' = '+ps(y),norm(y),'c'in w or t)
 t2=_dv(s2,c2)
 if t:
  out('tan 2x = sin 2x/cos 2x = ('+pp(s2)+')/('+pp(c2)+') = '+_q(t2))
 return{'s':s2,'c':c2,'t':t2}
def _given():
 r,f,q=_gr('x')
 if not r:
  return
 c=r['c']
 d=_d2(r,BS.get(f,f))
 for z,h,v in(('ANS: ',' x',r),('  ',' 2x',d)):
  out(z+', '.join([NM[w]+h+' = '+pp(v[w])for w in 'sct']))
 if yes('Half angle','n'):
  g='-'*(q>2)
  out('x/2 in Q'+str(1+(q>2))+'  (0 <= x < 2pi)')
  _sh('sin(x/2) = sqrt((1 - '+_pv(c)+')/2)','sqrt((1-('+c+'))/2)')
  _sh('cos(x/2) = '+g+'sqrt((1 + '+_pv(c)+')/2)',g+'sqrt((1+('+c+'))/2)')
def _sum():
 a=_gr('A')[0]
 if not a:
  return
 b=_gr('B')[0]
 if not b:
  return
 g='-'if ask('A+B or A-B (+/-)','+',0)=='-'else '+'
 nm='A'+g+'B'
 u='('+nm+')'
 s=_cmp('sin',g,a,b,nm)
 c=_cmp('cos',g,a,b,nm)
 if a['t']=='undefined'or b['t']=='undefined':
  t=_dv(s,c)
  out('tan'+u+' = sin'+u+'/cos'+u+' = '+_q(t))
 else:
  t=_cmp('tan',g,a,b,nm)
 out('ANS: sin'+u+' = '+pp(s)+', cos'+u+' = '+pp(c)+', tan'+u+' = '+pp(t))
def trig_values():
 hdr('Trig values')
 o=ask('1)f(angle) 2)inverse 3)ratio 4)A+-B','1',0)
 if o=='3':
  _given()
 elif o=='4':
  _sum()
 else:
  dg=ask('Deg or rad (d/r)','r',0).lower()[:1]=='d'
  e=norm(ask('e.g. '+('arccos(-1/2)'if o=='2'else 'cos(7pi/6)'),'',0 if o=='2'else ''))
  if o=='2':
   _inv(e,dg)
  else:
   _val(e,dg)
 wait()
def _rcp(s):
 for k in range(20):
  c=[z for z in _calls(s)if z[0]in 'seccsccottan']
  if not c:
   break
  n,a,i,j=c[0]
  r=RC[n].replace('A','('+a+')')
  s=s[:i]+'('+r+')'+s[j:]
 return s
def _dbl(s,fm):
 for k in range(20):
  hit=0
  for n,a,i,j in _calls(s):
   if n in SG and has(a,'x'):
    A=S('('+a+')/2')
    if '/'not in A:
     hit=1
     break
  if not hit:
   break
  r={'sin':'2*sin(A)*cos(A)','tan':'2*tan(A)/(1-tan(A)^2)','cos':{'1':'cos(A)^2-sin(A)^2','3':'1-2*sin(A)^2'}.get(fm,'2*cos(A)^2-1')}[n].replace('A',A)
  s=s[:i]+'('+r+')'+s[j:]
 return s
def _py(e):
 best=e
 nu=Gs('numer('+e+')')
 de=Gs('denom('+e+')')
 if not nu or not de:
  return e
 for f in('trigsin(','trigcos('):
  for a,b in((Gs(f+nu+')'),de),(nu,Gs(f+de+')'))):
   r=Gs('normal(('+a+')/('+b+'))')
   if r and len(r)<len(best):
    best=r
 return best
def _chain(X,fm):
 st=[[X,'']]
 s=_rcp(X)
 if s!=X:
  n=[k+' = '+RC[k].replace('A','')for k in RC if k in str(_calls(X))]
  st.append([s,'('+', '.join(n).replace('csc','cosec')+')'])
 t=_dbl(s,fm)
 if t!=s:
  st.append([t,'(double angle)'])
 if[c for c in _calls(t)if c[1]!='x']:
  t=G('texpand('+t+')')
  st.append([t,'(compound angle)'])
 n=Gs('normal('+t+')')
 if n and n!=t:
  st.append([n,''])
  t=n
 f=Gs('factor('+t+')')
 if 'cos(x)^2+sin(x)^2'in f and 'cos(x)^2+sin(x)^2'not in t:
  st.append([f,'(factorise)'])
 p=_py(t)
 if p!=t:
  st.append([p,'(sin^2 x + cos^2 x = 1)'])
  t=p
 p=Gs('normal(sin2costan('+t+'))')
 if 'sin('in t and 'cos('in t and p and('sin('not in p)and('cos('not in p):
  st.append([p.replace('1/tan','cot')if p[:5]=='1/tan'else p,'(tan = sin/cos)'])
 return st
def _ch(X,fm):
 b=_chain(X,fm)
 for f in '13'if fm=='0'and '(double angle)'in str(b)else '':
  c=_chain(X,f)
  if len(c[-1][0])<len(b[-1][0]):
   b=c
 return b
def _ex(s):
 o=[]
 for t in split_terms(unwrap(s)):
  n,b=sign_body(t)
  u=unwrap(b)
  o.append(('-'if n else '')+(u if len(split_terms(u))==1 else b))
 return join_signed([pp(t)for t in o])
def _ln(z):
 return ' = '+_ex(z[0])+('  '+z[1]if z[1]else '')
def _tv(A):
 return{z:_S(NM[z]+'('+A+')')for z in 'sct'}
def _expand(e,fm):
 c=_fn(e)
 if not c or c[0]not in SG:
  out('Use sin/cos/tan(..)')
  return
 f,a=c
 ts=split_terms(a)
 if len(ts)>1:
  A=ts[0].lstrip('+')
  if len(ts)==2 and ts[1][0]=='-':
   g='-'
   B=ts[1][1:]
  else:
   g='+'
   B=join_signed(ts[1:]).replace(' ','')
  r=_cmp(f,g,_tv(A),_tv(B),'',0,(A,B))
 else:
  k=S('diff('+a+',x)')
  if k not in('2','3','4')or S('('+a+')-'+k+'*x')!='0':
   out('Use kx (k=2,3,4) or A+B')
   return
  if k=='3':
   d={z:unwrap(_dbl(NM[z]+'(2*x)',fm))for z in 'sct'}
   r=_cmp(f,'+',d,_tv('x'),'',0,('2x','x'),'  (double angle)')
  else:
   r=unwrap(_dbl(e,fm))
   if k=='4':
    out(pp(e)+' = '+ps(r)+'  (double angle)')
    r=G('expand('+r+')')
  r=_S(r)
 return r
def _ito(r,w):
 if w in('1','2'):
  r=G('normal('+('trigsin('if w=='1'else 'trigcos(')+r+'))')
 return r
def trig_ident():
 hdr('Trig identities')
 o=ask('1)expand 2)simplify 3)verify','1',0)
 fm=ask('cos2A 1)c^2-s^2 2)2c^2-1 3)1-2s^2 0)auto','0',0)
 if o=='1':
  e=norm(ask('f(x) e.g. sin(x+pi/3)','',''))
  r=_expand(e,fm)
  if r:
   r2=_ito(r,ask('In terms of 0)any 1)sin 2)cos','0',0))
   if ps(r2)!=ps(r):
    out(' = '+ps(r))
   ans(pp(e),_js(r2))
 elif o=='2':
  e=norm(ask('Expression in x','','E'))
  st=_ch(e,fm)
  p=Gs('tcollect('+st[-1][0]+')')
  if 'pi'not in p and 0<len(p)<min(len(e),len(st[-1][0])):
   st+=[[p,'(double angle)']]
  for z in st[1:-1]:
   out(_ln(z))
  if st[-1][1]:
   out('ANS: '+_ex(st[-1][0])+'  '+st[-1][1])
  else:
   ans('',_ex(st[-1][0]))
 else:
  L=norm(ask('LHS','',0))
  R=norm(ask('RHS','',0))
  a=_ch(L,fm)
  b=_ch(R,fm)
  out('LHS = '+_ex(L))
  I=J=-1
  for i in range(len(a)):
   for j in range(len(b)):
    if I<0 and unwrap(a[i][0])==unwrap(b[j][0]):
     I,J=(i,j)
  if I<0 and Gs('normal(('+a[-1][0]+')-('+b[-1][0]+'))')=='0':
   I,J=(len(a)-1,len(b)-1)
  for z in a[1:I+1 if I>=0 else len(a)]:
   out(_ln(z))
  if I>=0:
   z=a[I][0]
   for k in range(J-1,-1,-1):
    if unwrap(b[k][0])!=unwrap(z):
     z=b[k][0]
     out(_ln([z,'']))
   out('ANS: LHS = RHS')
  else:
   out('RHS = '+_ex(R))
   if Gs('simplify(texpand(('+L+')-('+R+')))')=='0':
    out('ANS: LHS = RHS  (LHS - RHS = 0)')
   else:
    m='ANS: LHS = RHS  (numeric check)'
    for x0 in('pi/6','7/10'):
     l,r=[Gs('simplify(subst('+z+',x='+x0+'))')for z in(L,R)]
     u,v=(F(l),F(r))
     if u is not None and v is not None and(abs(u-v)>1e-09):
      out('x = '+pp(x0)+': LHS = '+_q(l)+', RHS = '+_q(r))
      m='ANS: not an identity'
      break
    out(m)
 wait()
ITEMS=[('Trig values',trig_values),('Trig identities',trig_ident)]
