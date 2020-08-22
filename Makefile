PY3 = python3
G = git
c = Update
rr = "rerun"

run:
	$(PY3) main.py

rerun:
	$(PY3) main.py $(rr)

update: clean
	$(G) add .
	$(G) commit -m "$c"
	$(G) push

rupdate: clean
	$(G) reset HEAD~1

clean:
	rm -rf *~
	ls
