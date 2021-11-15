"""
High level python EVM interface

Old Norse for 'bag' (since it's a bag of tricks)

Usage:
  kista.py ( deploy   | d ) [ -q ] <contract_name>            [<args>...]
  kista.py ( call     | c ) [ -q ] <contract_name> <function> [<args>...]
  kista.py ( transact | t ) [ -q ] <contract_name> <function> [<args>...]
  kista.py -h | --help
  kista.py --version

Options:
  -h --help     Show this screen.
  -q            quiet mode
  --version     Show version.
"""
import sys, kista, docopt

def f(x):
    if x == 'true':
        return True
    if x == 'false':
        return False
    if x == 'null':
        return None
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
    arguments = docopt.docopt(__doc__, version=kista.version)

    w3 = kista.w3_connect(None)

    quiet = arguments['-q']

    if not w3.isConnected():
        print("no connection")
        raise exit(1)

    if arguments['deploy'] or arguments['d']:

        name = arguments['<contract_name>']
        args = [f(x) for x in arguments['<args>']]
        x = kista.deploy_contractAddress(name, *args)
        if not quiet: print(x)
        pass
        
    elif arguments['call'] or arguments['c']:

        name = arguments['<contract_name>']
        func = arguments['<function>']
        args = [f(x) for x in arguments['<args>']]

        x = w3.eth.contract(address=kista.load_contractAddress(name),
                            abi=kista.load_abi(name))
        x = kista.WrapContract(x)
    
        if func not in x.ras:
            print("func not found")
            raise exit(2)

        result = x.getattr(func)(*args)

        if not quiet: print(result)
        pass
    
    elif arguments['transact'] or arguments['t']:

        name = arguments['<contract_name>']
        func = arguments['<function>']
        args = [f(x) for x in arguments['<args>']]

        x = w3.eth.contract(address=kista.load_contractAddress(name),
                            abi=kista.load_abi(name))
        x = kista.WrapContract(x)
    
        if func not in x.was:
            print("func not found")
            raise exit(2)

        result = x.getattr(func)(*args)

        if not quiet: print(result)
        pass

    else:
        print("dunno what to do", arguments)
        pass
