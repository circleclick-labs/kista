"""
High level python EVM interface

Old Norse for 'bag' (since it's a bag of tricks)

Usage:
  kista ( d | deploy   )  [ -q ] [ -j ] [ --v <value> [<unit>]] <contract_name> -as <name> [<args>...]
  kista ( t | transact )  [ -v ] [ -j ] [ --v <value> [<unit>]] <contract_name> <function> [<args>...]
  kista ( c | call     )  [ -q ] [ -j ]                         <contract_name> <function> [<args>...]
  kista ( a | address  )  [ -q ] [ -j ]                         <contract_name> [ <new_address> ]
  kista -h | --help
  kista --version

Options:
  <wei>         amount to send in wei.
  <unit>        units to send (default: wei)
  -h --help     Show this screen.
  -q            quiet mode
  -v            verbose mode
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
    import os, eth_account, kista, docopt, json, functools

    A = docopt.docopt(__doc__, version=kista.version)

    nname = A['<name>']
    vbose = A['-v']
    quiet = A['-q']
    _json = A['-j']
    name  = A['<contract_name>']
    value = A['<value>']
    unit  = A['<unit>'] or 'wei'
    wei   = A['<wei>']
    func  = A['<function>']

    w3 = kista.add_onion(kista.w3_connect(None))
    
    if not w3.isConnected():
        print("no connection")
        raise exit(1)

    args = lambda: [_f(x) for x in A['<args>']]

    if A['deploy'] or A['d']:

        if nname:
            kista.link_contract(name, nname)
            nname = name
            pass

        f = functools.partial(kista.deploy_contract(name))

        if value:
            result = f(*args(), value=w3.toWei(value, unit))
            #result = kista.deploy_contract(name, *args(), value=w3.toWei(value, unit))
        else:
            result = f(*args())
            #result = kista.deploy_contract(name, *args())
            pass
        
        if not quiet:
            println(result, _json)
            pass
        pass
        
    elif A['transact'] or A['t']:

        x = kista.load_wrapped_contract(name)
        
        if func not in x.was:
            print("func not found")
            raise exit(2)

        f = x.getattr(func)

        if value:
            result = f(*args(), value=w3.toWei(value, unit))
        else:
            result = f(*args())
            pass
    
        if vbose:
            println(result, _json)
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
    
    elif A['address'] or A['a']:

        new_address = A['<new_address>']

        if new_address:
            save_contractAddress(name, new_address)
            raise exit(0)

        address = load_contractAddress(name)
        if not quiet:
            println(address, _json)
            pass
        pass

    else:
        print("dunno what to do", A)
        pass
