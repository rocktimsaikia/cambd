BIN_DEST = /usr/bin/cambd

install:
	cp -f cambd-cli/cambd.py $(BIN_DEST)
	chmod +x $(BIN_DEST)
	@echo "Install successful."

uninstall:
	rm -f $(BIN_DEST)
	@echo "Uninstall successful."
