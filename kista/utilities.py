import os, sys, json, time

__version__ = '2.0.2'

w3, private, public = None, None, None

def balance(address=None):
    return w3.eth.get_balance(address or w3.eth.default_account)

def set_private(x):
    global private
    private = x
    pass

def set_public(x):
    global public
    public = w3.eth.default_account = x
    pass

def w3_connect(default_account, gasfactor=None, onion=None):
    global w3
    from web3.auto import w3 as _w3
    w3 = _w3
    if default_account is not None:
        w3.eth.default_account = w3.eth.accounts[default_account]
    else:
        set_public (os.getenv('PUBLIC'))
        set_private(os.getenv('PRIVATE',''))
        pass
    if onion: add_onion(w3)
    return w3

def add_onion(w3, _private = None):
    from web3.middleware import construct_sign_and_send_raw_middleware
    from eth_account import Account
    acct = Account.from_key(_private or private)
    #acct = Account.create('KEYSMASH FJAFJKLDSKF7JKFDJ 1530')
    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(acct))
    return w3

def tx_wait(tx_hash):
    return w3.eth.wait_for_transaction_receipt(tx_hash)

def load_abi(name):
    return json.load(open(f'out/{name}.abi'))

def load_bytecode(name):
    return           open(f'out/{name}.bin').read()

def load_contractAddress(name):
    return           open(f'out/{name}.cta').read()

def save_contractAddress(name, contractAddress):
    return           open(f'out/{name}.cta','w').write(contractAddress)

def load_wrapped_contract(*a, **kw):
    import sys
    sys.stderr.write("LOAD WRAPPED CONTRACT DEPRECATED\n")
    return WrapContract(load_contract(*a, **kw))

def cta(name):
    return load_contractAddress(name)

def save_cta(name, contractAddress):
    return save_contractAddress(name, contractAddress)

def  _link_contract(old_name, new_name, ext, msg):
    if os.system(f"ln -s ./{old_name}.{ext} out/{new_name}.{ext}") > 0:
        raise Exception(msg)
    return

def   link_contract(old_name, new_name):
    _link_contract(old_name, new_name, "abi", "ABI ERR")
    _link_contract(old_name, new_name, "bin", "BIN ERR")
    pass

def   load_contract(name, address=None):
    if address is None:
        address = load_contractAddress(name)
        pass
    return w3.eth.contract(abi=load_abi(name), address=address)

def   wrap_contract(*a, **kw):
    return WrapContract(load_contract(*a, **kw))

def    new_contract(name):
    return w3.eth.contract(abi=load_abi(name),
                           bytecode=load_bytecode(name))

def deploy_contract(name, *args, **kw):
    tx_receipt = _wcall(new_contract(name).constructor, *args, **kw)
    save_contractAddress(name, tx_receipt.contractAddress)
    return tx_receipt.contractAddress

def _raw_wcall(func, *args, _from=None, **kw):
    if _from: kw['from'] = _from
    tx_hash = func(*args).transact(kw)
    tx_receipt = tx_wait(tx_hash)
    return tx_receipt

def _wcall(func, *args, _from=None, **kw):
    if _from: kw['from'] = _from
    while 1:
        try:
            tx_hash = func(*args).transact(kw)
            tx_receipt = tx_wait(tx_hash)
            return tx_receipt
        except ValueError as e:
            if e.args[0]['code'] != -32010:
                raise
            print("retry...")
            time.sleep(0.1)
            continue
        pass
    return

def q_wcall(func, *args, _from=None, tries=-1, **kw):
    if _from: kw['from'] = _from
    while 1:
        try:
            tx_hash = func(*args).transact(kw)
            tx_receipt = tx_wait(tx_hash)
            return tx_receipt
        except ValueError as e:

            tries -= 1
            
            if tries == 0:
                raise
            
            if e.args[0]['code'] != -32010:
                raise
            
            print("retry...")
            
            time.sleep(0.1)
            
            pass

        pass

    return

def _rcall(func, *args, **kw):
    return func(*args).call(kw)

'''
def new_wcall(contract, funcname, *args, _from=None, **kw):
    if private is None:
        return old_wcall(contract, funcname, *args, _from, **kw)
    kw['from'] = _from or public
    func = get_func(contract, funcname)
    if gasfactor is not None:
        gas = func(*args).estimateGas()
        kw['gas']   = int(gasfactor * gas)
        pass
    if pay:
        kw['value'] = int(pay)
        pass
    kw['nonce'] = w3.eth.get_transaction_count(public)
    print("@@@@@@ KW", kw)
    txn = func(*args).buildTransaction(kw)
    signed_txn = w3.eth.account.sign_transaction(txn, private)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = tx_wait(tx_hash)
    return tx_receipt
'''

class WrapMixin:
    
    def get_balance(_, address=None):
        return w3.eth.get_balance(address or _.address)
    
    pass
 
class WrapContract(WrapMixin):

    @property
    def address(_):
        return _.contract.address
    
    @property
    def events(_):
        return _.contract.events
    
    def __init__(_, contract):
        _.ras, _.was, _.contract = _.get_func_names_from_contract(contract)
        pass

    def getattr(_, key):
        from functools import partial
        func = _.contract.functions.__dict__[key]
        return partial(_rcall if key in _.ras else
                       _wcall if key in _.was else
                       None,
                       _.contract.functions.__dict__[key])
    
    def __getattr__(_, key):
        return _.getattr(key)
    
    def get_func_names_from_contract(_, c):
        r, w = [], []
        for f in c.functions._functions:
            a = r if f['stateMutability'] in ['view','pure'] else w
            a.append(f['name'])
            pass
        return r, w, c

    pass

class WrapAccount(WrapMixin):

    def transfer(_, **kw): # to, value
        try:
            _ = w3.eth.default_account
            w3.eth.default_account = _.address
            return tx_wait(w3.eth.send_transaction(kw))
            #    'to': address,
            #    'value': w3.toWei(amount, 'ether'),
            #    #'gas': 2000000,
            #    #'gasPrice': w3.toWei('50', 'gwei')
        finally:
            w3.eth.default_account = _
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

    pass
