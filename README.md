# kista
kista (old norse for bag)

Help on package kista:

## NAME

    kista - utilites for coins and whatnot, mostly ETH.

## DESCRIPTION

    kista is old norse for "box", because calling this 
    package "misc" or "util" seemed afraught with namespace collisions.

## PACKAGE CONTENTS

    cli - command line interface

## CLASSES

    builtins.object
        WrapMixin
            WrapAccount
            WrapContract
    
    class WrapAccount(WrapMixin)
     |  WrapAccount(address)
     |  
     |  Method resolution order:
     |      WrapAccount
     |      WrapMixin
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  __init__(_, address)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  __repr__(_)
     |      Return repr(self).
     |  
     |  __str__(_)
     |      Return str(self).
     |  
     |  transfer(_, address, amount)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from WrapMixin:
     |  
     |  get_balance(_, address=None)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from WrapMixin:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class WrapContract(WrapMixin)
     |  WrapContract(contract)
     |  
     |  Method resolution order:
     |      WrapContract
     |      WrapMixin
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  __getattr__(_, key)
     |  
     |  __init__(_, contract)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  get_func_names_from_contract(_)
     |  
     |  getattr(_, key)
     |  
     |  ----------------------------------------------------------------------
     |  Readonly properties defined here:
     |  
     |  address
     |  
     |  events
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from WrapMixin:
     |  
     |  get_balance(_, address=None)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from WrapMixin:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class WrapMixin(builtins.object)
     |  Methods defined here:
     |  
     |  get_balance(_, address=None)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

## FUNCTIONS

    deploy_contractAddress(name, *args)
    
    get_default_address()
    
    get_func(contract, funcname)
    
    load_abi(name)
    
    load_bytecode(name)
    
    load_contract(name, address=None)
    
    load_contractAddress(name)
    
    load_wrapped_contract(name, address=None)
    
    rcall(contract, funcname, *args, **kw)
    
    save_contractAddress(name, contractAddress)
    
    send(tx, pk=None, wait=False, verbose=False)
    
    set_default_address(default_account)
    
    w3_connect(default_account)
    
    wait_for_tx(tx_hash)
    
    wcall(contract, funcname, *args, _from=None, **kw)

## DATA
    version = '1.2.0'
    w3 = None

## FILE
    /Users/val/src/kista/kista/__init__.py

----

Help on module kista.cli in kista:

## NAME

    kista.cli - High level python EVM interface

## DESCRIPTION

    Old Norse for 'bag' (since it's a bag of tricks)
    
    Usage:
      kista.py deploy   <contract_name>            [<args>...]
      kista.py call     <contract_name> <function> [<args>...]
      kista.py transact <contract_name> <function> [<args>...]
      kista.py -h | --help
      kista.py --version
    
    Options:
      -h --help     Show this screen.
      --version     Show version.

## FUNCTIONS
    
    main()

## FILE

    /Users/val/src/kista/kista/cli.py


