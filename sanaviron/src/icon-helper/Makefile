PYTHON=python

all: help

help:
	@echo
	@echo "ICON HELPER UTILITY"
	@echo "-------------------"
	@echo 
	@echo "1. Make the stock icons: \"make stock\"."
	@echo "2. Run \"make install\" to install generated icon files."
	@echo 

clean:
	@test -d output && rm -rf output

stock:
	@test -e output || mkdir output
	@$(PYTHON) icon-helper.py
	@mv *.png output


install:
	@cp output/*.png ../../ui/stock
