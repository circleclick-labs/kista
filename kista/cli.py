"""
High level python EVM interface

Old Norse for 'bag' (since it's a bag of tricks)

Usage:
  kista ( b | balance  )  [ -q ] [ -j | +j ] <address>
  kista ( s | save     )  [ -q ] [ -j | +j ] <contract>  --as=<x>       <new_address>
  kista ( d | deploy   )  [ -q ] [ -j | +j ] [--v=<value>] <contract> [--as=<x>] [<args>...]
  kista ( t | transact )  [ -v ] [ -j | +j ] [--v=<value>] <contract>   <function>  [<args>...]
  kista ( c | call     )  [ -q ] [ -j | +j ]               <contract>   <function>  [<args>...]
  kista ( a | address  )  [ -q ] [ -j | +j ]               <contract>
  kista -h | --help
  kista --version

Options:
  -h --help     Show this screen.
  -q            quiet mode
  -v            verbose mode
  +j            JSON on
  -j            JSON off
  --version     Show version.
"""

def _f(x):
    if x == 'true':
        return True
    if x == 'false':
        return False
    if x == 'null':
        return None
    if x.startswith('@@'):
        return open(f"out/{x[2:]}.cta").read().strip()
    if x.startswith('@'):
        return _f(open(       x[1:]      ).read().strip())
    if x.startswith('~'):
        try:    return -int(x[1:])
        except: pass
        try:    return -float(x[1:])
        except: pass
        pass
    try:    return int(x)
    except: pass
    try:    return float(x)
    except: pass
    return x

def println(result, _json):
    if _json:
        print(json.dumps(result))
    else:
        print(result)
        pass
    pass

def main():
    import os, sys, eth_account, kista, docopt, json

    A = docopt.docopt(__doc__, version=kista.version)

    nname = A['--as']
    vbose = A['-v']
    quiet = A['-q']
    _json = bool(A['+j'])
    name  = A['<contract>']
    func  = A['<function>']
    value = A['--v'] or 0
    unit  = 'wei'

    w3 = kista.add_onion(kista.w3_connect(None))
    
    if not w3.isConnected():
        print("no connection")
        raise exit(1)

    args = lambda: [_f(x) for x in A['<args>']]

    if A['deploy'] or A['d']:

        if nname:
            kista.link_contract(name, nname)
            name = nname
            pass

        r = kista.deploy_contract(name, *args(), value=w3.toWei(value, unit))
        
        if not quiet:
            println(r, _json)
            pass
        pass
        
    elif A['save'] or A['s']:

        if nname:
            kista.link_contract(name, nname)
            name = nname
            pass

        new_address = A['<new_address>']

        if new_address:
            kista.save_contractAddress(name, new_address)
            raise exit(0)

        pass
        
    elif A['transact'] or A['t']:

        x = kista.load_wrapped_contract(name)
        
        if func not in x.was:
            print("func not found")
            raise exit(2)

        r = x.getattr(func)(*args(), value=w3.toWei(value, unit))

        if vbose:
            println(r, _json)
            pass
        
        pass

    elif A['call'] or A['c']:

        x = kista.load_wrapped_contract(name)
    
        if func not in x.ras:
            print("func not found")
            raise exit(2)

        result = x.getattr(func)(*args())

        if not quiet:
            println(result, _json)
            pass
        pass
    
    elif A['balance'] or A['b']:

        bal = w3.eth.get_balance(A['<address>'])
        
        sys.stdout.write(str(bal))
        
        if not quiet:
            sys.stdout.write('\n')
            pass

        pass
    
    elif A['address'] or A['a']:

        address = kista.load_contractAddress(name)
        if not quiet:
            println(address, _json)
            pass
        pass

    else:
        print("dunno what to do", A)
        pass
