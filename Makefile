PY3 = python3
G = git
c = Update

run:
	$(PY3) main.py

update: clean
	$(G) add .
	$(G) commit -m "$c"
	$(G) push

rupdate: clean
	$(G) reset HEAD~1

clean:
	rm -rf *~
	ls
