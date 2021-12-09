import os, sys, json, time

version = '1.8.14'

w3, private, public = None, None, None
gasfactor = None
pay = 0

def set_pay(x):
    global pay
    pay = x
    pass

def set_gasfactor(x):
    global gasfactor
    gasfactor = x
    pass

def set_private(x):
    global private
    private = x
    pass

def set_public(x):
    global public
    set_default_address(x)
    public = x
    pass

def w3_connect(default_account, gasfactor=None):
    global w3
    from web3.auto import w3 as _w3
    w3 = _w3
    if default_account is not None:
        w3.eth.default_account = w3.eth.accounts[default_account]
    else:
        set_public (os.getenv('PUBLIC'))
        set_private(os.getenv('PRIVATE',''))
        pass
    set_gasfactor(gasfactor or int(os.getenv('GASFACTOR', '1')))
    return w3

def add_onion(w3):
    from web3.middleware import construct_sign_and_send_raw_middleware
    from eth_account import Account
    acct = Account.from_key(private)
    #acct = Account.create('KEYSMASH FJAFJKLDSKF7JKFDJ 1530')
    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(acct))
    #w3.eth.default_account = acct.address
    return w3

def wait_for_tx(tx_hash):
    return w3.eth.wait_for_transaction_receipt(tx_hash)

def send(tx, pk=None, wait=False, verbose=False):
    if pk:
        signed_tx = w3.eth.account.sign_transaction(tx, pk) if pk else tx
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    else:
        tx_hash = w3.eth.send_transaction(tx)
        pass
    if verbose: print("TXH:", tx_hash.hex())
    if wait:
        tx_receipt = wait_for_tx(tx_hash)
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

def cta(name):
    return load_contractAddress(name)

def save_cta(name, contractAddress):
    return save_contractAddress(name, contractAddress)
'''
def link_contract(old_name, new_name):
    print("LINK", repr((old_name, new_name)))
    ret = os.system(f"ln -s ./{old_name}.abi out/{new_name}.abi")
    #ret = os.system(f"(cd out; ln -s {old_name}.abi {new_name}.abi")
    if ret != 0:
        raise Exception("ABI ERR")
    ret = os.system(f"ln -s ./{old_name}.bin out/{new_name}.bin")
    #ret = os.system(f"(cd out; ln -s {old_name}.bin {new_name}.bin")
    if ret != 0:
        raise Exception("BIN ERR")
    pass
'''
def _link_contract(old_name, new_name, ext, msg):
    if os.system(f"ln -s ./{old_name}.{ext} out/{new_name}.{ext}") > 0:
        raise Exception(msg)
    return

def link_contract(old_name, new_name):
    #print("LINK", repr((old_name, new_name)))
    _link_contract(old_name, new_name, "abi", "ABI ERR")
    _link_contract(old_name, new_name, "bin", "BIN ERR")
    pass

def load_contract(name, address=None):
    if address is None:
        address = load_contractAddress(name)
        pass
    abi        = load_abi(name)
    contract   = w3.eth.contract(abi=abi, address=address)
    return contract

def load_wrapped_contract(*a, **kw):
    return WrapContract(load_contract(*a, **kw))

def raw_deploy_contract(contract, name, *args, **kw):
    tx_hash    = contract.constructor(*args).transact(kw)
    tx_receipt = wait_for_tx(tx_hash)
    contractAddress = tx_receipt.contractAddress
    save_contractAddress(name, contractAddress)
    return contractAddress
    
def deploy_contract(name, *args, **kw):
    abi        = load_abi(name)
    bytecode   = load_bytecode(name)
    contract   = w3.eth.contract(abi=abi, bytecode=bytecode)
    while 1:
        try:
            return raw_deploy_contract(contract, name, *args, **kw)
        except ValueError as e:
            if e.args[0]['code'] != -32010:
                raise
            print("retry...")
            time.sleep(0.1)
            continue
        pass
    return
'''    
def old_deploy_contractAddress(name, *args):
    abi        = load_abi(name)
    bytecode   = load_bytecode(name)
    contract   = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash    = contract.constructor(*args).transact()
    tx_receipt = wait_for_tx(tx_hash)
    contractAddress = tx_receipt.contractAddress
    save_contractAddress(name, contractAddress)
    return contractAddress

def deploy_contractAddress(name, *args, **kw):
    if private is None:
        return old_deploy_contractAddress(name, *args)
    abi         = load_abi(name)
    bytecode    = load_bytecode(name)
    contract    = w3.eth.contract(abi=abi, bytecode=bytecode)
    if gasfactor is not None:
        gas = contract.constructor(*args).estimateGas()
        kw['gas']   = int(gasfactor * gas)
        pass
    kw['nonce'] = w3.eth.get_transaction_count(public)
    txn         = contract.constructor(*args).buildTransaction(kw)
    signed_txn  = w3.eth.account.sign_transaction(txn, private)
    tx_hash     = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt  = wait_for_tx(tx_hash)
    contractAddress = tx_receipt.contractAddress
    save_contractAddress(name, contractAddress)
    return contractAddress
'''
def get_default_address():
    return w3.eth.default_account

def set_default_address(default_account):
    if type(default_account) == int:
        default_account = w3.eth.accounts[default_account]
        pass
    w3.eth.default_account = default_account
    return default_account

class WrapMixin:
    def get_balance(_, address=None):
        return w3.eth.get_balance(address or _.address)
    pass
 
def get_func(contract, funcname):
    return contract.functions.__dict__[funcname]
'''
def old_wcall(contract, funcname, *args, _from=None, **kw):
    if _from: kw['from'] = _from
    func = get_func(contract, funcname)
    tx_hash = func(*args).transact(kw)
    tx_receipt = wait_for_tx(tx_hash)
    return tx_receipt
'''
def raw_wcall(func, *args, **kw):
    tx_hash = func(*args).transact(kw)
    tx_receipt = wait_for_tx(tx_hash)
    return tx_receipt

def wcall(contract, funcname, *args, _from=None, **kw):
    if _from: kw['from'] = _from
    func = get_func(contract, funcname)
    while 1:
        try:
            return raw_wcall(func, *args, **kw)
        except ValueError as e:
            if e.args[0]['code'] != -32010:
                raise
            print("retry...")
            time.sleep(0.1)
            continue
        pass
    return
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
    tx_receipt = wait_for_tx(tx_hash)
    return tx_receipt
'''
def rcall(contract, funcname, *args, **kw):
    return get_func(contract, funcname)(*args).call(kw)

class WrapContract(WrapMixin):

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

    def getattr(_, key):
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
    
    def __getattr__(_, key):
        return _.getattr(key)
    
    def get_func_names_from_contract(_):
        r, w = [], []
        for f in _.contract.functions._functions:
            #print("SM", f['stateMutability'])
            if f['stateMutability'] in ['view','pure']:
                r.append(f['name'])
            else:
                w.append(f['name'])
                pass
            pass
        return r, w

    pass

class WrapAccount(WrapMixin):

    #def transfer(_, address, amount):
    def transfer(_, **kw): # to, value
        try:
            da = get_default_address()
            set_default_address(_.address)
            tx_hash = w3.eth.send_transaction(kw)
            #tx_hash = w3.eth.send_transaction({
            #    'to': address,
            #    'value': w3.toWei(amount, 'ether'),
            #    #'gas': 2000000,
            #    #'gasPrice': w3.toWei('50', 'gwei')
            #})
            tx_receipt = wait_for_tx(tx_hash)
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

    pass
