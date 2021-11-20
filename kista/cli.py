"""
High level python EVM interface

Old Norse for 'bag' (since it's a bag of tricks)

Usage:
  kista ( d | deploy   )  [ -q ] <contract_name>            [<args>...]
  kista ( c | call     )  [ -q ] <contract_name> <function> [<args>...]
  kista ( t | transact )  [ -v ] <contract_name> <function> [<args>...]
  kista ( p | pay ) <wei> [ -v ] <contract_name> <function> [<args>...]
  kista -h | --help
  kista --version

Options:
  <wei>         amount to send in wei.
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

def main():
    import os, eth_account, kista, docopt

    arguments = docopt.docopt(__doc__, version=kista.version)

    w3 = kista.w3_connect(None)

    if 1:
        from web3.middleware import construct_sign_and_send_raw_middleware
        from eth_account import Account
        PRIVATE = os.getenv('PRIVATE')
        acct = eth_account.Account.from_key(PRIVATE)
        #acct = Account.create('KEYSMASH FJAFJKLDSKF7JKFDJ 1530')
        w3.middleware_onion.add(construct_sign_and_send_raw_middleware(acct))
        w3.eth.default_account = acct.address
        pass
    
    quiet = arguments['-q']

    if not w3.isConnected():
        print("no connection")
        raise exit(1)

    if arguments['deploy'] or arguments['d']:

        name = arguments['<contract_name>']
        args = [_f(x) for x in arguments['<args>']]
        x = kista.deploy_contractAddress(name, *args)
        if not quiet: print(x)
        pass
        
    elif arguments['call'] or arguments['c']:

        name = arguments['<contract_name>']
        func = arguments['<function>']
        args = [_f(x) for x in arguments['<args>']]

        x = w3.eth.contract(address=kista.load_contractAddress(name),
                            abi=kista.load_abi(name))
        x = kista.WrapContract(x)
    
        if func not in x.ras:
            print("func not found")
            raise exit(2)

        result = x.getattr(func)(*args)

        import json
        
        if not quiet: print(json.dumps(result))
        pass
    
    elif arguments['transact'] or arguments['t']:

        name = arguments['<contract_name>']
        func = arguments['<function>']
        args = [_f(x) for x in arguments['<args>']]

        x = w3.eth.contract(address=kista.load_contractAddress(name),
                            abi=kista.load_abi(name))
        x = kista.WrapContract(x)
    
        if func not in x.was:
            print("func not found")
            raise exit(2)

        result = x.getattr(func)(*args)

        if arguments['-v']: print(result)
        pass

    elif arguments['pay'] or arguments['p']:

        wei  = arguments['<wei>']
        name = arguments['<contract_name>']
        func = arguments['<function>']
        args = [_f(x) for x in arguments['<args>']]

        x = w3.eth.contract(address=kista.load_contractAddress(name),
                            abi=kista.load_abi(name))
        x = kista.WrapContract(x)

        if func not in x.was:
            print("func not found")
            raise exit(2)

        unit = 'wei'
        #result = x.getattr(func)(*args, value=int(wei))
        #result = x.getattr(func)(*args, value=web3.toWei(wei, 'gwei'))
        #print(repr(w3.toWei(wei, unit)))
        result = x.getattr(func)(*args, value=w3.toWei(wei, unit))

        if arguments['-v']: print(result)
        pass

    else:
        print("dunno what to do", arguments)
        pass
