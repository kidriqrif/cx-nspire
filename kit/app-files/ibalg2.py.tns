from ibcore import*
TITLE='Logs/binom/parfrac'
def _isint(r):
 return isnum(r)and '/'not in r and('.'not in r)
def _par(u):
 for c in u:
  if c not in LET and c not in DIG and(c!='.'):
   return '('+u+')'
 return u
def _pe(u):
 return u if u.isdigit()or u.isalpha()else '('+u+')'
def _nd(v):
 n=G('numer('+v+')')
 d=G('denom('+v+')')
 if d=='1':
  return n
 return(n if len(split_terms(n))<2 else '('+n+')')+'/'+_par(d)
def _fn(g):
 k=g.find('(')
 a=g[k:]
 if k>0 and unwrap(a)!=a and(not[c for c in g[:k]if c not in LET+DIG]):
  return[g[:k],g[k+1:-1]]
_B=['e']
def _lgb(s):
 _B[0]='e'
 o=''
 i=0
 n=len(s)
 for z in range(30):
  k=s.find('log',i)
  if k<0:
   break
  j=k+3
  if j<n and s[j]=='_':
   j+=1
  m=j
  while m<n and s[m]in DIG:
   m+=1
  if m==j and j>k+3 and(m<n)and(s[m]in LET):
   m+=1
  if m==j or m>=n or s[m]!='(':
   o+=s[i:k+3]
   i=k+3
   continue
  d=0
  e=m
  while e<n:
   if s[e]=='(':
    d+=1
   elif s[e]==')':
    d-=1
    if d==0:
     break
   e+=1
  o+=s[i:k]+'logb('+s[m+1:e]+','+s[j:m]+')'
  if s[j]in DIG:
   _B[0]=s[j:m]
  i=e+1
 return o+s[i:]
def _co(c):
 return ''if c=='1'else '-'if c=='-1'else pp(c)
def _px(s):
 return ps(s).replace(')*x',')x')
def _lg(b,u):
 if b=='e':
  return 'ln('+pp(u)+')'
 return('log('if b=='10'else 'log_'+b+'(')+pp(u)+')'
def _o(s,m):
 if m and len(s)+len(m)+4>max(8,CFG['w']):
  out(s)
  out('  ('+m+')')
 else:
  out(s+('  ('+m+')'if m else ''))
def _roots(eq):
 R=GL('solve('+eq+',x)')
 if not R:
  out('No real solution')
 for r in R:
  r=S(r)
  if 'LambertW'in r or bad(r):
   out('ANS: x = '+sf3(F(r))+' (GDC)')
  else:
   ans('x',r)
def _pw(b,p):
 q=1
 for m in range(1,40):
  q*=p
  if q==b:
   return m
  if q>b:
   return 0
 return 0
def _bp(s):
 s=unwrap(s)
 if _isint(s)and int(s)>1:
  return[int(s),'1']
 t=split_top(s,'^')
 if len(t)==2 and _isint(t[0])and(int(t[0])>1):
  return[int(t[0]),unwrap(t[1])]
 return None
def _logeq(L,R):
 T=[]
 K=[]
 for side,sg in((L,0),(R,1)):
  for t in split_terms(side):
   neg,fs=split_factors(t)
   if sg:
    neg=not neg
   c='-1'if neg else '1'
   lg=None
   for f in fs:
    h=_fn(f[1])
    if f[0]=='*'and lg is None and h and(h[0]in('ln','log10','logb')):
     lg=h
    else:
     c+=f[0]+'('+f[1]+')'
   if has(c,'x'):
    return 0
   if lg is None:
    K.append('-('+c+')')
    continue
   if lg[0]=='logb':
    u,b=split_top(lg[1],',')
   else:
    u,b=(lg[1],'e'if lg[0]=='ln'else '10')
   if has(b,'x'):
    return 0
   T.append([S(c),b,u])
 if not T:
  return 0
 B=T[0][1]
 for t in T:
  if B!='e'and t[1]!='e'and(float(t[1])<float(B)):
   B=t[1]
 k=S('+'.join(K))if K else '0'
 for t in T:
  if t[1]!=B:
   f=S('ln('+t[1]+')/ln('+B+')')
   _o(_lg(t[1],t[2])+' = '+_lg(B,t[2])+'/'+(pp(f)if isnum(f)else _lg(B,t[1])),'change of base')
   t[0]=S('('+t[0]+')/('+f+')')
 m=G('lcm('+','.join(['denom('+t[0]+')'for t in T])+')')
 if m!='1'and isnum(m):
  for t in T:
   t[0]=S(m+'*('+t[0]+')')
  k=S(m+'*('+k+')')
  out(join_signed([_co(t[0])+_lg(B,t[2])for t in T])+' = '+pp(k))
 num=[]
 den=[]
 pw=0
 for t in T:
  neg,c=sign_body(t[0])
  if c!='1':
   pw=1
  u=t[2]if c=='1'else _par(t[2])+'^'+(c if _isint(c)else '('+c+')')
  (den if neg else num).append(u)
 if pw:
  _o(join_signed([_lg(B,a)for a in num]+['-'+_lg(B,a)for a in den])+' = '+pp(k),'power law')
 U=S('*'.join(['('+a+')'for a in num])if num else '1')
 lw='log laws'if len(num)+len(den)>1 else ''
 w=''
 if k=='0'and den and num:
  V=S('*'.join(['('+a+')'for a in den]))
  if len(num)>1 or len(den)>1:
   _o(_lg(B,U)+' = '+_lg(B,V),lw)
 else:
  if den:
   U=G('('+U+')/('+'*'.join(['('+a+')'for a in den])+')')
  if lw or(not pw and(len(split_terms(L))>1 or k!=R)):
   _o(_lg(B,U)+' = '+pp(k),lw)
  V=S(('exp('if B=='e'else B+'^(')+k+')')
  if B!='e'and k!='1':
   w=B+'^'+_pe(pp(k))
   if w==pp(V):
    w=''
 if U!='x'or has(V,'x'):
  out(pp(U)+' = '+(w+' = 'if w else '')+pp(V))
 elif w:
  out('x = '+w)
 P=G('numer(normal('+U+'-('+V+')))')
 if Gs('is_polynomial('+P+',x)')=='true'and _dg(P)>1:
  P=G('expand('+P+')')
  if P[0]=='-':
   P=G('expand(-('+P+'))')
  if len(split_terms(P))>2:
   out(ps(P)+' = 0')
 R=GL('solve('+P+'=0,x)')
 n=0
 for r in R:
  bad1=[t[2]for t in T if has(t[2],'x')and F('subst('+t[2]+',x='+r+')')<=0]
  if bad1:
   out('x = '+pp(r)+' rejected: '+pp(bad1[0])+' <= 0')
  else:
   ans('x',S(r))
   n+=1
 if not n:
  out('No valid solution')
 return 1
def _expeq(L,R):
 if len(split_terms(L))==1 and(not has(R,'x')):
  c=S('('+L+')/(1'+''.join([z[0]+'('+z[1]+')'for z in split_factors(L)[1]if has(z[1],'x')])+')')
  if c!='1'and(not has(c,'x')):
   L=S('('+L+')/('+c+')')
   R=S('('+R+')/('+c+')')
   out(pp(L)+' = '+pp(R))
 if len(split_terms(L))==1 and len(split_terms(R))==1:
  a=_bp(L)
  b=_bp(R)
  if a and b:
   for p in range(2,min(a[0],b[0])+1):
    m1=_pw(a[0],p)
    m2=_pw(b[0],p)
    if m1 and m2:
     l=S('expand(%d*(%s))'%(m1,a[1]))
     r=S('expand(%d*(%s))'%(m2,b[1]))
     out('%d^%s = %d^%s'%(p,_pe(pp(l)),p,_pe(pp(r))))
     if l!='x':
      out(ps(l)+' = '+ps(r))
     _roots(l+'='+r)
     return
  for s in(L,R):
   if not has(s,'x')and(F(s)or 1)<=0:
    out('No solution: a^x > 0')
    return
  l=G('lnexpand(ln('+L+'))')
  r=G('lnexpand(ln('+R+'))')
  t0=_px(l)+' = '+_px(r)
  E=G('expand(('+l+')-('+r+'))')
  a=S('diff('+E+',x)')
  if has(a,'x')or a=='0':
   _o(t0,'take ln')
   _roots(l+'='+r)
   return
  b=S('-('+G('subst('+E+',x=0)')+')')
  t=(_px(a+'*x')if len(split_terms(a))<2 else 'x('+_px(a)+')')+' = '+_px(b)
  x=(b if len(split_terms(b))<2 else '('+b+')')+'/'+(a if isnum(a)else '('+a+')')
  y=S(x)
  y=y if len(y)<=len(x)else x
  if l!='x':
   _o(t0,'take ln')
  elif 'ln('+pp(R)+')'!=pp(y):
   out('x = ln('+pp(R)+')')
  if t!=t0 and a not in('1','-1'):
   out(t)
  ans('x',y)
  return
 E='('+L+')-('+R+')'
 p=''
 if 'e^'in E or 'exp('in E:
  p='e'
 else:
  bs=[]
  for j in range(1,len(E)):
   if E[j]=='^'and E[j-1]in DIG:
    i=j-1
    while i>0 and E[i-1]in DIG:
     i-=1
    bs.append(int(E[i:j]))
  if bs:
   for c in range(2,min(bs)+1):
    if not[b for b in bs if not _pw(b,c)]:
     p=str(c)
     break
 Q=''
 if p:
  X=',x=ln(u)'+(''if p=='e'else '/ln('+p+')')+'))))'
  Q=Gs('numer(normal(simplify(subst(pow2exp('+E+')'+X)or Gs('numer(normal(simplify(subst('+E+X)
 if not Q or has(Q,'x')or Gs('is_polynomial('+Q+',u)')!='true':
  _roots(L+'='+R)
  return
 _us(Q,p+'^x','ln(U)'+(''if p=='e'else '/ln('+p+')'),1)
def _us(Q,lb,iv,pos):
 out('Let u = '+lb+('  (u > 0)'if pos else ''))
 out(ps(Q)+' = 0')
 n=0
 for r in GL('solve('+Q+'=0,u)'):
  if pos and F(r)<=0:
   out('u = '+pp(r)+' rejected (u > 0)')
   continue
  x=S(iv.replace('U','('+r+')'))
  out(lb+' = '+pp(r))
  ans('x',x)
  n+=1
 if not n:
  out('No solution')
def _lsub(s,E):
 b='e'if 'ln('in s else '10'if 'log10('in s else _B[0]
 Q=Gs('numer(normal(lnexpand(subst('+E+',x='+('exp(u)'if b=='e'else b+'^u')+'))))')
 if not Q or has(Q,'x')or Gs('is_polynomial('+Q+',u)')!='true'or(not has(Q,'u')):
  return 0
 _us(Q,_lg(b,'x'),'exp(U)'if b=='e'else b+'^U',0)
 return 1
def explog():
 hdr('Exp/log equation')
 q=ask('Equation in x','',0)
 s=norm(_lgb(q))
 o=''
 t=''
 for c in s+' ':
  if c in DIG or c=='.':
   t+=c
  else:
   o+=('('+G('exact('+t+')')+')'if '.'in t else t)+c
   t=''
 s=o[:-1]
 k=s.find('=')
 L=s[:k]if k>=0 else s
 R=s[k+1:]if k>=0 else '0'
 out(q if '*'not in q or 'log'in q else ps(L)+' = '+ps(R))
 if not has(L,'x'):
  L,R=(R,L)
 if 'ln('in s or 'log10('in s or 'logb('in s:
  if not _logeq(L,R)and(not _lsub(s,'('+L+')-('+R+')')):
   _roots(L+'='+R)
 else:
  _expeq(L,R)
 wait()
def _pa(a):
 return '('+pp(a)+')'if '/'in a or a[0]=='-'or len(split_terms(a))>1 else pp(a)
def _xp(a):
 return S('normal(x*diff('+a+',x)/('+a+'))')if has(a,'x')else '0'
def binom():
 hdr('Binomial expansion')
 s=norm(ask('(a+b)^n =','',''))
 sg=s[:2]=='1/'
 if sg:
  s=s[2:]
 h=_fn(s)
 if h and h[0]=='sqrt':
  s='('+h[1]+')^(1/2)'
 p=split_top(s,'^')+['1']
 t=split_terms(unwrap(p[0]))if len(p)<4 else[]
 if sg:
  p[1]='-('+p[1]+')'
 if len(t)!=2:
  out('Enter as (a+b)^n')
  wait()
  return
 A,B=t
 B=B.lstrip('+')
 n=S(unwrap(p[1]))
 if _isint(n)and int(n)>=0:
  M=int(n)
  Tg=lambda r:'comb(%d,%d)*(%s)^%d*(%s)^%d'%(M,r,A,M-r,B,r)
  a=''if A=='1'else _pe(pp(A))
  b=_pe(pp(B))
  fx=lambda s,e:''if not s or e==0 else ' '+s+('^%d'%e if e>1 else '')
  Tp=lambda r:'%dC%d'%(M,r)+fx(a,M-r)+fx(b,r)
  out('T(r+1) = %dCr'%M+(' '+a+'^(%d-r)'%M if a else '')+' '+b+'^r')
  P=S('expand('+_xp(A)+'*('+n+'-r)+('+_xp(B)+')*r)')
  t=split_terms(P)
  Ps=join_signed([pp(z)for z in t if z[0]!='-']+[pp(z)for z in t if z[0]=='-'])
  if has(P,'r'):
   out('Power of x: '+Ps)
  k=ask('Coeff of x^k: k = (blank=all)','',0)
  t=[A,B]
  if k=='':
   for r in range(min(M,12)+1):
    v=_nd(Tg(r))
    out(Tp(r)+' = '+pp(v))
    t.append(v)
   ans('',join_signed(t[2:])+(' + ...'if M>12 else ''))
  else:
   k=norm(k)
   rr=GL('solve('+P+'='+k+',r)')if has(P,'r')else[]
   r=rr[0]if rr else ''
   if P!='r':
    out(Ps+' = '+pp(k)+' => r = '+pp(r))
   if not(_isint(r)and 0<=int(r)<=M):
    out('r not in 0..%d: no x^%s term'%(M,k))
    ans('coeff','0')
   else:
    r=int(r)
    out('T%d = '%(r+1)+Tp(r))
    v=N(Tg(r))
    c=S('('+v+')/x^('+k+')')
    if c!=v:
     out(' = '+pp(v))
    ans('constant term'if k=='0'else 'coeff of x^'+k,c)
  wait()
  return
 if has(A,'x'):
  A,B=(B,A)
 fa=F(A)
 if has(A,'x')or not has(B,'x')or fa is None or(fa==0)or(fa<0 and(not _isint(n))):
  out('Need (a + bx)^n, a > 0 constant')
  wait()
  return
 y=S('('+B+')/('+A+')')
 an=N('('+A+')^('+n+')')
 if '/-'in an:
  an=N('-('+an.replace('/-','/')+')')
 if A!='1':
  out('= '+('('+pp(A)+')'if A[0]=='-'else pp(A))+'^('+pp(n)+')('+join_signed(['1',pp(y)])+')^('+pp(n)+')')
  out('= '+_pa(an)+'('+join_signed(['1',pp(y)])+')^('+pp(n)+')')
 K=int(ask('Terms','4',0))
 c='1'
 fl=''
 T=[]
 for j in range(min(K,8)):
  if j:
   m=S(n+'-'+str(j-1))
   fl+='('+pp(m)+')'
   c=S('('+c+')*('+m+')/'+str(j))
  v=_nd('('+c+')*('+y+')^'+str(j))
  if j:
   out(fl+('/%d! '%j if j>1 else '')+_pe(pp(y))+('^%d'%j if j>1 else '')+' = '+pp(v))
  T.append(v)
 if an!='1':
  out('= '+_pa(an)+'('+join_signed([pp(v)for v in T])+' + ...)')
  T=[_nd('('+an+')*('+v+')')for v in T]
 ans('',join_signed(T)+' + ...')
 out('Valid for |'+pp(sign_body(y)[1])+'| < 1')
 v=Gs('solve(abs('+y+')<1,x)')
 for ch in '()[]':
  v=v.replace(ch,'')
 w=v.split(' and ')
 if len(w)==2 and w[0][:2]=='x>'and(w[1][:2]=='x<'):
  v=pp(w[0][2:])+' < x < '+pp(w[1][2:])
 out('=> '+v)
 wait()
def _dg(p):
 return int(G('degree('+p+',x)'))
def _par2(p):
 return ps(p)if len(split_terms(p))<2 and '/'not in p else '('+ps(p)+')'
def parfrac():
 hdr('Partial fractions')
 f=norm(rhs(ask('f(x) =','',0)))
 out('f(x) = '+pp(f))
 P=G('numer('+f+')')
 Q=G('denom('+f+')')
 fs=GL('factors('+Q+')')
 L=[fs[j]for j in range(0,len(fs)-1,2)if has(fs[j],'x')]
 d=split_top(f,'/')
 td=unwrap(d[-1])if len(d)==2 else Q
 tl=[unwrap(z[1])for z in split_factors(td)[1]if has(z[1],'x')]
 lin=not[z for z in tl if _dg(z)!=1]
 tf=pp(G('factor('+td+')'))
 h=' = '
 if not lin and tf!=pp(td):
  out(pp(td)+' = '+tf)
  h='f(x) = '
 if len(L)!=2 or _dg(Q)!=2:
  r=ps(G('partfrac('+f+',x)'))
  if r.replace(' ','')==pp(f).replace(' ',''):
   out('Not 2 distinct linear factors')
  else:
   ans('f(x)',r)
  wait()
  return
 if S('('+td+')/('+Q+')')!='1':
  out('f(x) = '+_par2(P)+'/('+pp(G('factor('+Q+')'))+')')
  h=' = '
 if lin and len(tl)==2:
  L=tl
 a,b=L
 q='0'
 if _dg(P)>=2:
  q=G('quo('+P+','+Q+',x)')
  P=G('rem('+P+','+Q+',x)')
  out(h+ps(q)+' + '+_par2(P)+'/('+pp(Q)+')')
  h=' = '
 P=S('('+P+')*('+a+')*('+b+')/('+Q+')')
 out(h+(ps(q)+' + 'if q!='0'else '')+'A/'+_par(pp(a))+' + B/'+_par(pp(b)))
 tn=unwrap(d[0])
 out(ps(tn if len(d)==2 and S(tn+'-('+P+')')=='0'else P)+' = A'+_par(pp(b))+' + B'+_par(pp(a)))
 res=[q]
 for lb,u,w in(('A',a,b),('B',b,a)):
  x0=GL('solve('+u+'=0,x)')[0]
  pv=S('subst('+P+',x='+x0+')')
  wv=S('subst('+w+',x='+x0+')')
  k=S('('+pv+')/('+wv+')')
  out('x = '+pp(x0)+': '+(''if wv=='1'else pp(pv)+' = '+{'-1':'-'}.get(wv,wv if _isint(wv)else _par(pp(wv)))+lb+', ')+lb+' = '+pp(k))
  neg,kk=sign_body(k)
  d=split_top(kk,'/')+['1']
  res.append(('-'if neg else '')+d[0]+'/'+(_par(u)if d[1]=='1'else '('+d[1]+'*'+_par(u)+')'))
 if G('normal('+'+'.join(['('+t+')'for t in res])+'-('+f+'))')!='0':
  raise GErr('check failed')
 ans('f(x)',join_signed(res))
 wait()
ITEMS=[('Exp/log equation',explog),('Binomial',binom),('Partial fractions',parfrac)]
