PACKAGE=sanaviron

all: help

help:
	@echo
	@echo "FIRST TIME TRANSLATION"
	@echo "----------------------"
	@echo
	@echo "1. To generate translation file for first time, add the language in languages.all, then \"make generate\" to generate"
	@echo "   the file input/<LANG>/$(PACKAGE).po."
	@echo "2. Translate the generated file input/<LANG>/$(PACKAGE).po and run \"make compile\"."
	@echo "3. Run \"make install\" to install generated compiled files."
	@echo
	@echo "UPDATE TRANSLATION"
	@echo "------------------"
	@echo
	@echo "1. To update translation file, run \"make update\". "
	@echo "2. Translate the updated file input/<LANG>/$(PACKAGE).po and run \"make compile\"."
	@echo "3. Run \"make install\" to install generated compiled files."
	@echo

clean:
	@test -e input/$(PACKAGE).pot && rm -rf input/$(PACKAGE).pot
	@cat languages.all | while read language; do test -e input/$${language}/$(PACKAGE).po~ && rm -rf input/$${language}/$(PACKAGE).po~; done

distclean:
	@test -e input && rm -rf input
	@test -e languages.all && rm -f languages.all

purge: distclean
	@test -e output && rm -rf output

update:
	@xgettext --default-domain=$(PACKAGE) --language=Python --keyword=_ --output=input/$(PACKAGE).pot --files-from=input/$(PACKAGE).files --from-code=utf-8; \
	cat languages.all | while read language; do \
		test -e input/$${language} || mkdir input/$${language}; \
		msgmerge --update input/$${language}/$(PACKAGE).po input/$(PACKAGE).pot; \
		echo Now you can translate file `pwd`/input/$${language}/$(PACKAGE).po; \
	done

generate:
	@test -e input || { \
		mkdir input; \
		touch input/$(PACKAGE).files; \
		echo Put your sources files to be translated in input/$(PACKAGE).files and rerun this script.; \
		exit; \
	}; \
	xgettext --default-domain=$(PACKAGE) --language=Python --keyword=_ --output=input/$(PACKAGE).pot --files-from=input/$(PACKAGE).files --from-code=utf-8; \
	test -e languages.all || { \
		touch languages.all; \
		echo Put the target languages in languages.all and rerun this script.; \
		exit; \
	}; \
	cat languages.all | while read language; do \
		test -e input/$${language} || mkdir input/$${language}; \
		msginit --input=input/$(PACKAGE).pot --output-file=input/$${language}/$(PACKAGE).po; \
		echo Now you can translate file `pwd`/input/$${language}/$(PACKAGE).po; \
	done

compile:
	@test -e output || mkdir output
	@cat languages.all | while read language; do \
		test -e output/$${language}/LC_MESSAGES || mkdir -p output/$${language}/LC_MESSAGES; \
		msgfmt --output-file=output/$${language}/LC_MESSAGES/$(PACKAGE).mo input/$${language}/$(PACKAGE).po; \
	done

install:
	@cat languages.all | while read language; do \
		test -d ../../localization/$${language} || mkdir -p ../../localization/$${language}; \
		cp output/$${language}/LC_MESSAGES/$(PACKAGE).mo ../../localization/$${language}/LC_MESSAGES; \
	done
