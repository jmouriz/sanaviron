BASE=../../3rd/pycha/pycha

all: install

install:
	sed 's/pycha\.//g' $(BASE)/bar.py > bar.py
	sed 's/pycha\.//g' $(BASE)/chart.py > chart.py
	sed 's/pycha\.//g' $(BASE)/color.py > color.py
	sed 's/pycha\.//g' $(BASE)/line.py > line.py
	sed 's/pycha\.//g' $(BASE)/pie.py > pie.py
	sed 's/pycha\.//g' $(BASE)/scatter.py > scatter.py
	sed 's/pycha\.//g' $(BASE)/stackedbar.py > stackedbar.py
	echo '# -*- coding: utf-8 -*-' > __init__.py
	cat $(BASE)/__init__.py chart.tpl.py >> __init__.py
