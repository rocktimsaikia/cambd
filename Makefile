dest_dir := /usr/local/src/cambd-cli
bin_file := /usr/bin/cambd

preinstall:
	pip install bs4 halo simple-term-menu

install:
	cp -f cambd-cli/cambd.sh $(bin_file)
	chmod +x $(bin_file)
	mkdir -m 777 -p $(dest_dir)
	cp -f cambd-cli/cambd.py $(dest_dir)/cambd.py
	@echo "\nInstall successful ✅"
	@echo "Run: cambd --help"

uninstall:
	rm -rf $(bin_file)
	rm -rf $(dest_dir)
	@echo "Uninstall successful."
