WETH9=0xd0A1E359811322d97991E03f863a0C30C2cF029C
USDC=0xe22da380ee6B445bb8273C81944ADEB6E8450422
DAI=0x4F96Fe3b7A6Cf9725f59d353F723c1bDb64CA6Aa
SOLC=solc -oout --abi --bin --overwrite --allow-paths=.
KISTA=python3 -um kista
#eall:
#	python3 xx.py
all:
	$(SOLC) contracts/*.sol
	scripts/deploy    Test2 hello\ again
	scripts/kt        Test2 dontPayMe 199
	scripts/kt --v 99 Test2 payMe 99
	scripts/call      Test2 vals
#	python3 xx.py
qqqqqq:
	scripts/call   Test2 getMsgSender
	scripts/call   Test2 vals
	scripts/kt --v 100000000000000 Test2 payMe 25000000
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
irun:
	docker build . -t t
	docker run  \
		-v `pwd`":/root/src" -w/root/src \
		--rm --name t. -it t bash -l
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
