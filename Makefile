PY3 = python3
G = git
cm = "Update"

run:
	$(PY3) main.py

update: clean
	$(G) add .
	$(G) commit -m "$cm"
	$(G) push

clean:
	rm -rf *~
	ls
