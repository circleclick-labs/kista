SOLC=solc -oout --abi --bin --overwrite --allow-paths=.
all:
	$(SOLC) contracts/*.sol
	tree -s .
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
	tree .
dclean:
	docker rm -f t.
drealclean:
	docker ps     -aq | xargs docker rm  -f
	docker images -aq | xargs docker rmi -f
