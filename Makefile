DIST = /usr/local/src/cambd-cli
BIN = /usr/bin/cambd

install:
	cp -f cambd-cli/cambd.sh $(BIN)
	chmod +x $(BIN)
	mkdir -m 777 -p $(DIST)
	cp -f cambd-cli/cambd.py $(DIST)
	@echo "Install successful."

uninstall:
	rm -rf $(bin_file)
	rm -rf $(dest_dir)
	@echo "Uninstall successful."
