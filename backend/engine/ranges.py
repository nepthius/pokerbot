#ranks for now, will find better way to implement later
RANKS   = ["A","K","Q","J","T","9","8","7","6","5","4","3","2"]
RANK_INDEX = { r : i   for   i, r   in enumerate( RANKS )   }

def _rank_char( x ):
        if x.upper() in ("10" , "T"):
            return  "T"
        else:
            return x


def canonical_from_cards( c1   , c2 ):
    #gonna move out later
    def _v_to_chr( vv ):
        return {
         14:"A",13:"K",12:"Q",11:"J",10:"T",

          9:"9",8:"8",7:"7",6:"6",5:"5",4:"4",3:"3",2:"2"
        }[ vv ]

    r1   =   (14 if c1[0] == 1 else c1[0])
    r2 = 14 if c2[0] == 1 else c2[0]

    s1, s2 = c1[1]  , c2[1]

    c1txt = _v_to_chr(r1)
    c2txt = _v_to_chr(r2)
    if r2 > r1:
         c1txt, c2txt ,  s1 , s2 , r1, r2 = c2txt, c1txt, s2, s1, r2, r1

    if r1 == r2:     # in case of pairs, using this as a check rq
        return f"{c1txt}{c2txt}"

    suited = ( s1==s2 )
    return f"{c1txt}{c2txt}{   ('s' if suited else 'o')   }"



def canonical_from_text( hole ):
    xx = hole.strip().upper()
    bits = xx.split()

    #make into func later
    if len(bits)==2 and bits[0][-1] in "CDHS"   and  bits[1][-1] in "CDHS":

        def _grab(one):
            rr , st = one[:-1] , one[-1].lower()
            lkup={"A":14,"K":13,"Q":12,"J":11,"T":10}
            try:    
                rv = int(rr)
            except:
                rv = lkup[rr]

            return ((14 if rv==1 else rv), st)

        a = _grab(bits[0])
        b = _grab(bits[1])

        suit_flag = (a[1] == b[1])

        inv = {14:"A",13:"K",12:"Q",11:"J",10:"T",
               9:"9",8:"8",7:"7",6:"6",5:"5",4:"4",3:"3",2:"2"}

        A1, A2 = inv[a[0]], inv[b[0]]
        v1, v2 = a[0], b[0]

        if v2 > v1:
            A1, A2 = A2, A1


        if A1==A2: return f"{A1}{A2}"

        return f"{A1}{A2}{'s' if suit_flag else 'o'}"

    else:
        #change up 10
        xx = xx.replace("10","T")
        return xx



#csv stuff
def load_range_csv( path : Path ):
        out = {}
        with path.open( newline = "" ) as f:
                rdr = csv.DictReader( f )
                for rw in rdr:
                    h = rw["hand"].strip().upper().replace("10","T")
                    act = rw["action"].strip().lower()
                    out[ h ] = act
        return out



def grid_from_range_map( rmap ):
    n = len(RANKS)
    grid = [
        [ "" for x in range(n) ] 
        for   x   in range(n)
    ]

    for ii, r1 in enumerate(RANKS):
        for jj, r2 in enumerate(RANKS):

            if ii==jj:
                key = f"{r1}{r2}"
            elif ii < jj:
                key = f"{r1}{r2}s"
            else:
                key = f"{r2}{r1}o"

            if key in rmap:
                grid[ii][jj] = rmap[key]

    return grid


def action_for_hand( rmap , hc ):
         return rmap.get(hc ,    "")
