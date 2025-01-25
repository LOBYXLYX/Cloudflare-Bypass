
def analyze_response(c):
    functions = []

    for i,v in enumerate(c.split('400')):
        if '304' in v[:700] and '200' in v[:700] and (
            "'v_'" in v[:1200] and "'+'" in v[:1200] and "'='" in v[:900]
        ):
            o = v[:1400].split("'='")[0]


    p = o.split('new eM[')
    for pw in p:
        ow = pw.split(':')[0][:30]
        print(ow)
        if ow[:1] == '(' and (
                ow.split(')](')[1].count(')') in [1, 2] and ow.split(')](')[1].count('(') in [1, 2]
        ):
            v1 = ow.split(')](')[1].split(')')[0]

    v1_ts = [f'({v1})', f',{v1})', f'({v1},']

    for tv1 in v1_ts:
        for i,v in enumerate(o.split(tv1)):
            q = len(v)
        
            if v[q - 2:q].isalpha() or (
                v[q - 2:q][:1].isalpha() and v[q - 2:q][1:].isnumeric()
            ) and (v[q - 3:q][:1] == '=' or v[q - 4:q][:2] == ']('):
                v2 = v[q - 2:q]

    v3_fncs = []
    v4_ts_ts = []
    v2_ts = [f'function {v2}(', f'{v2}=function(']

    print(v2_ts)
    for tv2 in v2_ts:
        for i,v in enumerate(c.split(tv2)):
            if 'new' in v[:400] and 'return' in v[:400]:
                this = v.split('}function')[0]
                functions.append('function notdecrypted(' + this + '}')
                this_ts = ['(new ', ',new ']

    for this_t in this_ts:
        for i,v in enumerate(this.split(this_t)):
            if this_t in this:
                if 'return ' in v:
                    v3_fncs.append(v[len(v) - 2:len(v)])
                else:
                    v3_fncs.append(v.split('(')[0])
    l = 0
    print(v3_fncs)

    for v3 in v3_fncs:
        fn = c.split(f'function {v3}(')[1].split('}function ')[0] + '}'
        print(fn, '\n\n')
        functions.append(f'function {v3}(' + fn)

        if fn.count('this.') > 20: # formating 15+ functions
            thisthis = fn.split(']=')

            for i,v in enumerate(thisthis):
                if v[:2].isalpha() or (v[:1].isalpha() and v[1:2].isnumeric()) and (v[2:3] == ',' or v[2:3] == '}'):
                    tosp = v[2:3]
                    v4 = v.split(tosp)[0]
                    print(v4)

                    v4_ts = [f'function {v4}(', f'{v4}=function(', f'{v4}=']
                    for tv4 in v4_ts:
                        for i,v in enumerate(c.split(tv4)):
                            if '(0,eval)' in v[:10]:
                                functions.append(f'{tv4}' + v.split('),')[0] + ')')
                                continue
                            if 'atob(' in v[:6]:
                                functions.append(f'{tv4}' + v.split('),')[0] + ')')
                                continue
                            if '[]' in v[:3]:
                                functions.append(f'{tv4}' + v[:5].split(',')[0])
                                print(v[:100])
                                continue

                            if not v[:100].startswith('window._cf_chl_opt'):
                                l += 1
                                j = v[:5500].split('}function')[0]
                                functions.append(f'{tv4}' + j + '}')
                                continue

            r = fn.split('=[0,')[1][:2]
            x = c.split(f'{r}=')[1]

            if 'atob' in x[:5]:
                print(x.split('),')[0])
                functions.append(f'{r}=' + x.split('),')[0] + ')')
                continue

    h = c.split('0;256>')[0]
    functions.append(h[len(h) - 9:len(h)][:2] + '=[]')


    def ull(func):
        o = None
        f = func[:80]
        print(f)
        m = ['){e=(', '){i=(']

        if '){for(' in f and f.split('){for(')[1][2:3] == '=' and f.split('){for(')[1][5:6] == ',':
            print('lalalla')
            o = f.split('){for(')[1]
        elif '){' in f and f.split('){')[1][2:3] == '=' and f.split('){')[1][5:6] == ',':
            print('lol')
            o = f.split('){')[1]
        elif '){if(' in f and f.split('){if(')[1][2:3] == '=' and f.split('){')[1][5:6] == ',':
            o = f.split('){if(')[1]
        elif 'return ' in f and f.split('return ')[1][2:3] == '=' and f.split('){')[1][5:6] == ',':
            o = f.split('return ')[1]
        elif 'throw ' in f and f.split('throw ')[1][2:3] == '=' and f.split('){')[1][5:6] == ',':
            o = f.split('throw ')[1]
        
        if o is None:
            for n in m:
                if n in f and f.split(n)[1][2:3] == '=':
                    o = f.split(n)[1]
                    break

        if o is None or not len(f) > 20:
            return func

        print(o)

        g, y = o.split(',')[0].split('=')
        repl = ' = (number) => b(number),console.log(this.h)'

        f = func.replace(f'={y}', repl).replace('}()}', '')
        return f

    def fll():
        _funcs = []
    
        for i,v in enumerate(c.split('function')):
            if v[:1] == ' ' and v.split('(')[1][:20].count(',') >= 3 and v[2:3] != '(':
                _funcs.append(v[1:3])
            
        for fn in _funcs:
            z = c.split(f'function {fn}(')[1].split('}function ')[0]
            yield f'function {fn}(' + z + '}'
    
    fll()

    new_functions = []
    new_functions.append('function eS(){return}')

    for func in functions:
        z = ull(func)
        #if 'function eU' in z:
        new_functions.append(z)

    for zfunc in fll():
        print(zfunc)
        new_functions.append(ull(zfunc))

    _new_funcs = []

    for f in new_functions:
        f = f.replace('}()}', '')
        f = f.replace("function eX(h,i,j,k,n,o,s,v,x,gU,B,C,D){return gU = (number) => b(number),B={'esFhS':gU(443),'bYhhR':function(E,F){return E*F},'Dlkwb':function(E,F){return F===E},'xYuhN':gU(1253),'SVjOu':function(E,F){return E(F)},'BDXAP':function(E,F){return E+F},'qNooy':function(E,F){return E-F},'KUxcn':function(E,F){return F^E},'gHPKB':function(E,F){return F^E}},C=this,D=this.h[B[gU(806)](60,this.g)],h=h[gU(1175)](),h[4]=h[4][gU(1175)](),this.h[110.83^this.g][gU(482)]([NaN,'','',0,[]],this.h[198^this.g][gU(307)],143),this.h[this.g^176]=j,this.h[33.05^this.g]=x,this.h[B[gU(806)](96,this.g)]=o,this.h[this.g^232.72]=v,this.h[8^this.g]=n,this.h[this.g^235.93]=s,this.h[B[gU(806)](60,this.g)]=h,this.h[this.g^198.75][gU(482)](-1),this.h[B[gU(375)](200,this.g)]=i,this.h[this.g^23]=k,function(gV,E,F,G){if(gV=gU,E={'dJwKO':function(H,I){return I===H},'uxxKx':B[gV(940)],'HPwKB':gV(515),'HvMIF':function(H,I){return I^H},'kBHTh':function(H,I){return H+I},'yuLPz':function(H,I,gW){return gW=gV,B[gW(875)](H,I)},'zZTdJ':function(H,I,gX){return gX=gV,B[gX(255)](H,I)},'bLKEl':gV(526),'TJLPY':function(H,I){return H^I}},B[gV(201)]!==gV(1253))k();else{for(F={},F.j=void 0,G={};!B[gV(457)](isNaN,C.h[60^C.g][0]);G.j=C.h[C.g^60][3]^B[gV(152)](B[gV(967)](C.h[C.g^60.85][1][gV(1149)](C.h[C.g^60.52][0]++),232),256)&255.26,function(I){return function(gY,O,P,Q,J,K,L,M){if(gY=b,E[gY(772)](E[gY(692)],E[gY(961)]))O={},O[gY(1098)]=gY(955),P=C[gY(1242)](new J([gY(326)],O)),Q=new O(P),j[gY(805)](P),Q[gY(843)]();else{J=(J=C.h[E[gY(732)](60,C.g)],K=J[3]+I.j,J[3]=E[gY(597)](E[gY(1010)](K,K)*32310,E[gY(1010)](39792,K))+62142&255,C.h[C.g^I.j]);try{J[gY(920)](C)(I.j)}catch(O){if(J=C.h[198.71^C.g],0<J[gY(307)]){if(E[gY(357)](gY(580),gY(442)))return!![];else for(L=E[gY(598)][gY(1073)]('|'),M=0;!![];){switch(L[M++]){case'0':C.h[E[gY(1188)](110,C.g)][gY(1089)](K);continue;case'1':K=J[gY(788)]();continue;case'2':if(E[gY(357)](-1,K))throw O;continue;case'3':C.h[C.g^60.88]=J[gY(788)]();continue;case'4':C.h[E[gY(732)](159,C.g)]=O;continue}break}}else throw O}}}}(G)(),G=F);return C.h[33.86^C.g]}}(),this.h[60.94^this.g]=D,this.h[this.g^143]}", "function eX(h,i,j,k,n,o,s,v,x,gU,B,C,D){return gU = (number) => b(number),console.log(h, i, j, k, h[4]),B={'esFhS':gU(443),'bYhhR':function(E,F){return E*F},'Dlkwb':function(E,F){return F===E},'xYuhN':gU(1253),'SVjOu':function(E,F){return E(F)},'BDXAP':function(E,F){return E+F},'qNooy':function(E,F){return E-F},'KUxcn':function(E,F){return F^E},'gHPKB':function(E,F){return F^E}},C=this,D=this.h[B[gU(806)](60,this.g)],h=h[gU(1175)](),h[4]=h[4][gU(1175)](),this.h[110.83^this.g][gU(482)]([NaN,'','',0,[]],this.h[198^this.g][gU(307)],143),this.h[this.g^176]=j,this.h[33.05^this.g]=x,this.h[B[gU(806)](96,this.g)]=o,this.h[this.g^232.72]=v,this.h[8^this.g]=n,this.h[this.g^235.93]=s,this.h[B[gU(806)](60,this.g)]=h,this.h[this.g^198.75][gU(482)](-1),this.h[B[gU(375)](200,this.g)]=i,this.h[this.g^23]=k,function(gV,E,F,G){if(gV=gU,E={'dJwKO':function(H,I){return I===H},'uxxKx':B[gV(940)],'HPwKB':gV(515),'HvMIF':function(H,I){return I^H},'kBHTh':function(H,I){return H+I},'yuLPz':function(H,I,gW){return gW=gV,B[gW(875)](H,I)},'zZTdJ':function(H,I,gX){return gX=gV,B[gX(255)](H,I)},'bLKEl':gV(526),'TJLPY':function(H,I){return H^I}},B[gV(201)]!==gV(1253))k();else{for(F={},F.j=void 0,G={};!B[gV(457)](isNaN,C.h[60^C.g][0]);G.j=C.h[C.g^60][3]^B[gV(152)](B[gV(967)](C.h[C.g^60.85][1][gV(1149)](C.h[C.g^60.52][0]++),232),256)&255.26,function(I){return function(gY,O,P,Q,J,K,L,M){if(gY=b,E[gY(772)](E[gY(692)],E[gY(961)]))O={},O[gY(1098)]=gY(955),P=C[gY(1242)](new J([gY(326)],O)),Q=new O(P),j[gY(805)](P),Q[gY(843)]();else{J=(J=C.h[E[gY(732)](60,C.g)],K=J[3]+I.j,J[3]=E[gY(597)](E[gY(1010)](K,K)*32310,E[gY(1010)](39792,K))+62142&255,C.h[C.g^I.j]);try{J[gY(920)](C)(I.j)}catch(O){if(J=C.h[198.71^C.g],0<J[gY(307)]){if(E[gY(357)](gY(580),gY(442)))return!![];else for(L=E[gY(598)][gY(1073)]('|'),M=0;!![];){switch(L[M++]){case'0':C.h[E[gY(1188)](110,C.g)][gY(1089)](K);continue;case'1':K=J[gY(788)]();continue;case'2':if(E[gY(357)](-1,K))throw O;continue;case'3':C.h[C.g^60.88]=J[gY(788)]();continue;case'4':C.h[E[gY(732)](159,C.g)]=O;continue}break}}else throw O}}}}(G)(),G=F);return C.h[33.86^C.g]}}(),this.h[60.94^this.g]=D,this.h[this.g^143]}")
        _new_funcs.append(f)
    return _new_funcs
