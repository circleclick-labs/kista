SOLC=solc -oout --abi --bin --overwrite --allow-paths=.
KISTA=python3 -um kista
#eall:
#	python3 xx.py
all:
	$(SOLC) contracts/*.sol
	scripts/deploy Test2 hello\ again
	scripts/kt     Test2 dontPayMe 199
	scripts/pay 99 Test2 payMe 99
	scripts/call   Test2 vals
#	python3 xx.py
qqqqqq:
	scripts/call   Test2 getMsgSender
	scripts/call   Test2 vals
	scripts/pay 100000000000000 Test2 payMe 25000000
	scripts/call   Test2 vals
	python3 xx.py
#	python3 test/test.py
bashr: all
	docker exec -it -w /root/src t. bash -l
run:
	docker build . -t t
	docker run  --network=bridge -p8545:8545 \
		-v `pwd`":/root/src" -w/root/src \
		-d --name t. -it t bash -c \
		'ganache-cli -h0>g.log'
clean:
	rm -fr out ?.p?? *.log
	find . -name __pycache__ | xargs rm -r
	find . -name '*~' | xargs rm -r
	rm -fr kista.egg-info dist build
dclean:
	docker rm -f t.
drealclean:
	docker ps     -aq | xargs docker rm  -f
	docker images -aq | xargs docker rmi -f
