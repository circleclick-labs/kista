"""
Naval Fate.

Usage:
  kista.py deploy <contract_name> [<args>...]
  kista.py ship new <name>...
  kista.py ship <name> move <x> <y> [--speed=<kn>]
  kista.py ship shoot <x> <y>
  kista.py mine (set|remove) <x> <y> [--moored|--drifting]
  kista.py -h | --help
  kista.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
"""
import kista, docopt
arguments = docopt.docopt(__doc__)
if arguments['deploy']:

    def f(x):
        try:    return int(x)
        except: pass
        try:    return float(x)
        except: pass
        return x
        
    name = arguments['<contract_name>']
    args = [f(x) for x in arguments['<args>']]

    w3 = kista.w3_connect()

    print("DEPLOY", name, args, w3.isConnected())

    if not w3.isConnected():
        print("no connection")
        raise exit(1)

    print([f(x) for x in args])

    x = kista.force_load_contract_address(name, *args,
                                          reload=1)
    print("X", x)
    
else:
    print("dunno what to do", arguments)
    pass
