PY3 = python3
G = git
m = Update

run:
	$(PY3) main.py

update: clean
	$(G) add .
	$(G) commit -m "$m"
	$(G) push

rupdate: clean
	$(G) reset HEAD~1

clean:
	rm -rf *~
	ls
