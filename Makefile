SOLC=solc -oout --abi --bin --overwrite --allow-paths=.
all:
	$(SOLC) contracts/*.sol
	tree -s .
