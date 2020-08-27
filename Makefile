PY3 = python3
G = git
c = Update

rr = "rerun"

at = "auto"
at_sch = "[0,1,1]"
at_eval = "[0,0,2]"
at_c = "1"
at_n = "2"
at_s = "s"

run:
	$(PY3) main.py

rerun:
	$(PY3) main.py $(rr)

auto:
	$(PY3) main.py $(at) $(at_sch) $(at_eval) $(at_c) $(at_n) $(at_s)

update: clean
	$(G) add .
	$(G) commit -m "$c"
	$(G) push

rupdate: clean
	$(G) reset HEAD~1

clean:
	rm -rf *~
	ls
