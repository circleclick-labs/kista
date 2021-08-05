"""
Naval Fate.

Usage:
  kista.py deploy <contract_name> <args>...
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
import kista
import docopt
arguments = docopt.docopt(__doc__)
#print(args)
#print(args)
#print(args)
if arguments['deploy']:
    name = arguments['<contract_name>']
    args = arguments['<args>']

    w3 = kista.w3_connect()

    print("DEPLOY", name, args, w3.isConnected())
else:
    print("dunno what to do", arguments)
    pass
