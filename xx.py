import kista
from web3 import Web3#, EthereumTesterProvider
from web3.middleware import construct_sign_and_send_raw_middleware
w3 = kista.w3_connect(None)
import os, eth_account
PRIVATE = os.getenv('PRIVATE')
PUBLIC  = os.getenv('PUBLIC')
print(PUBLIC, PRIVATE)
acct = eth_account.Account.from_key(PRIVATE)
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(acct))
w3.eth.default_account = acct.address
print(acct)
print(acct.key.hex())
print(acct.address)

z = kista.load_wrapped_contract("Test2")
print(z)
print(z.address)
print(z.vals())
z.dontPayMe(25000000)
print(z.vals())
c = z.contract
print(c.functions)
print(c.all_functions())
payMe = c.functions['payMe']
if 0:
    txh = payMe(50000).transact({
        "value":234523,
    })
    print(txh.hex())
    kista.wait_for_tx(txh)
else:
    z.payMe(50000, value=234500)
    pass
print('ok')
print(z.vals())
exit()
functions = list(c.functions)
print(functions)
print(repr(functions))
print(dir(c))
#z.payMe(25000000, value=900000)
#print(z.vals())
#print(w3.eth.get_balance(z.address))
