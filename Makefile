SRC_DEST = /usr/local/src/cambd-cli
BIN_DEST = /usr/bin/cambd

install:
	cp -f cambd-cli/cambd.sh $(BIN_DEST)
	chmod +x $(BIN_DEST)
	mkdir -m 777 -p $(SRC_DEST)
	cp -f cambd-cli/cambd.py $(SRC_DEST)
	@echo "Install successful."

uninstall:
	rm -f $(BIN_DEST)
	rm -rf $(SRC_DEST)
	@echo "Uninstall successful."
