"""
High level python EVM interface

Old Norse for 'bag' (since it's a bag of tricks)

Usage:
  kista ( b | balance  )  [ -q ] [ -j | +j ] <address>
  kista ( s | save     )  [ -q ] [ -j | +j ]               <contract> [--as=<x>] <address>
  kista ( d | deploy   )  [ -q ] [ -j | +j ] [--v=<value>] <contract> [--as=<x>] [<args>...]
  kista ( t | transact )  [ -v ] [ -j | +j ] [--v=<value>] <contract> <function> [<args>...]
  kista ( c | call     )  [ -q ] [ -j | +j ]               <contract> <function> [<args>...]
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
        return _f(open(f"out/{x[2:]}.cta").read().strip())
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

def println(result, _json, quiet=False):
    if quiet:
        # do nothing
        pass
    elif _json:
        print(json.dumps(result))
    else:
        print(result)
        pass
    return

def main():
    import os, sys, eth_account, kista, docopt, json
    from functools import partial
    A = docopt.docopt(__doc__, version=kista.__version__)
    nname = A['--as']
    vbose = A['-v']
    quiet = A['-q']
    _json = bool(A['+j'])
    name  = A['<contract>']
    func  = A['<function>']
    value = A['--v'] or 0
    unit  =   'wei'
    w3 = kista.w3_connect(None, onion=1)
    if not w3.isConnected():
        print("no connection")
        raise exit(1)
    if nname:
        kista.link_contract(name, nname)
        name = nname
        pass
    if   A['deploy'] or A['d']:
        println(partial(kista.deploy_contract, name)(
            *[_f(x) for x in A['<args>']],
            value=w3.toWei(value, unit)),
                _json, not vbose)
    elif A['transact'] or A['t']:
        println(kista.wrap_contract(name).getattr(func)(
            *[_f(x) for x in A['<args>']],
            value=w3.toWei(value, unit)),
                _json, not vbose)
    elif A['call'] or A['c']:
        println(kista.wrap_contract(name).getattr(func)(
            *[_f(x) for x in A['<args>']],
            value=w3.toWei(value, unit)),
                _json, quiet)
    elif    A['save'] or A['s']: kista.save_cta(name, A['<address>'])
    elif A['address'] or A['a']: println(kista.cta(name), _json, quiet)
    elif A['balance'] or A['b']: print(kista.balance(A['<address>']))
    else:
        print("dunno what to do", A)
        exit(1)
