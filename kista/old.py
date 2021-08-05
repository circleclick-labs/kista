"""
# kista - utilites for coins and whatnot, mostly ETH.

    kista is old norse for "box", because calling this 
    package "misc" or "util" seemed afraught with namespace collisions.
"""

import os, sys, json
from web3 import Web3
from pprint import pprint

w3 = None

version = '1.0.0'

def w3_connect(default_account = None):
    global w3
    from web3.auto import w3 as _w3
    w3 = _w3
    if default_account is not None:
        w3.eth.default_account = w3.eth.accounts[default_account]
        pass
    return w3
    
def send(tx, pk=None, wait=False, verbose=False):
    if pk:
        signed_tx = w3.eth.account.sign_transaction(tx, pk) if pk else tx
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    else:
        tx_hash = w3.eth.send_transaction(tx)
        pass
    if verbose: print("TXH:", tx_hash.hex())
    if wait:
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if verbose:
            d = dict(tx_receipt)
            del d['logs']
            del d['logsBloom']
            print("TXR:")
            pprint(d)
            pass
        return tx_receipt

def load_abi(name):
    return json.load(open(f'out/{name}.abi'))

def load_bytecode(name):
    return           open(f'out/{name}.bin').read()

def load_contractAddress(name):
    return           open(f'out/{name}.cta').read()

def save_contractAddress(name, contractAddress):
    return           open(f'out/{name}.cta','w').write(contractAddress)

def deploy_contract(name, *args):
    abi        = load_abi(name)
    bytecode   = load_bytecode(name)
    contract   = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash    = contract.constructor(*args).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contractAddress = tx_receipt.contractAddress
    save_contractAddress(name, contractAddress)
    return contractAddress

def force_load_contract(name,*args,reload=0):
    if reload:
        return deploy_contract(name,*args)
    try:
        return load_contractAddress(name)
    except FileNotFoundError:
        return deploy_contract(name,*args)
    pass

def force_load_contract_address(name,*args,**kw):
    contractAddress = force_load_contract(name,*args,**kw)
    return w3.eth.contract(contractAddress, abi=load_abi(name))

def wcall(contract, funcname, *args, _from=None, **kw):
    if _from: kw['from'] = _from
    tx_hash = contract.functions.__dict__[funcname](*args).transact(kw)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt

def rcall(contract, funcname, *args, **kw):
    return contract.functions.__dict__[funcname](*args).call(kw)

class WrapContract:

    @property
    def address(_):
        return _.contract.address
    
    @property
    def events(_):
        return _.contract.events
    
    def __init__(_, contract):
        _.contract = contract
        _.ras, _.was = _.get_func_names_from_contract()
        pass

    def __getattr__(_, key):
        def wrap_rfunc(name):
            return(lambda *args, **kw:
                   rcall(_.contract, name, *args, **kw))
        def wrap_wfunc(name):
            return(lambda *args, **kw:
                   wcall(_.contract, name, *args, **kw))
        if key in _.ras: return wrap_rfunc(key)
        if key in _.was: return wrap_wfunc(key)
        name, value = repr(type(_).__name__), repr(key)
        msg = f"{name} object has no attribute {value}"
        raise AttributeError(msg)
    
    def get_balance(_, address=None):
        return w3.eth.get_balance(address or _.contract.address)
    
    def get_func_names_from_contract(_):
        r, w = [], []
        for f in _.contract.functions._functions:
            if f['stateMutability'] in ['view','pure']:
                r.append(f['name'])
                #print("read only", f['name'])
            else:
                #print("writes something", f['name'])
                w.append(f['name'])
                pass
            pass
        return r, w

    pass

def get_default_address():
    return w3.eth.default_account

def set_default_address(default_account):
    if type(default_account) == int:
        default_account = w3.eth.accounts[default_account]
        pass
    w3.eth.default_account = default_account
    return default_account

class WrapAccount:

    def transfer(_, address, amount):
        try:
            da = get_default_address()
            set_default_address(_.address)
            tx_hash = w3.eth.send_transaction({
                'to': address,
                'value': w3.toWei(amount, 'ether'),
                #'gas': 2000000,
                #'gasPrice': w3.toWei('50', 'gwei')
            })
            #print("TXH", tx_hash)
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            #print("TXR", dict(tx_receipt).keys())
            #print("TXR", dict(tx_receipt)['logs'])
            #print("TXR", dict(tx_receipt)['status'])
            return tx_receipt['transactionHash'].hex()
        finally:
            set_default_address(da)
            pass
    
    def __init__(_, address):
        if type(address) == int:
            address = w3.eth.accounts[address]
            pass
        _.address = address
        pass

    def __repr__(_):
        return repr(_.address)

    def __str__(_):
        return  str(_.address)

    def get_balance(_, address=None):
        return w3.eth.get_balance(address or _.contract.address)

    pass
