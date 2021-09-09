"""
Naval Fate.

Usage:
  kista.py deploy   <contract_name>            [<args>...]
  kista.py call     <contract_name> <function> [<args>...]
  kista.py transact <contract_name> <function> [<args>...]
  kista.py -h | --help
  kista.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
import kista, docopt

def f(x):
    try:    return int(x)
    except: pass
    try:    return float(x)
    except: pass
    return x

arguments = docopt.docopt(__doc__, version=kista.version)

w3 = kista.w3_connect(0)

if not w3.isConnected():
    print("no connection")
    raise exit(1)

if arguments['deploy']:

    name = arguments['<contract_name>']
    args = [f(x) for x in arguments['<args>']]

    x = kista.deploy_contractAddress(name, *args)
    print(x)
    
elif arguments['call']:

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

    print(result)

elif arguments['transact']:

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

    print(result)

else:
    print("dunno what to do", arguments)
    pass

def hello():
    print("HELLO")
    
