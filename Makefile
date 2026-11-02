SCRIPT_NAME := 6gen66
INSTALL_DIR ?= /usr/local/bin
PYTHON_CMD ?= python3

.PHONY: install uninstall clean help

install: $(INSTALL_DIR)/$(SCRIPT_NAME)
	@echo "$(SCRIPT_NAME) installed successfully! Run it by simply typing: 6gen66"

$(INSTALL_DIR)/$(SCRIPT_NAME): $(SCRIPT_NAME).py
	@mkdir -p $(INSTALL_DIR)
	@cp $< $@
	@chmod +x $@

uninstall:
	rm -f $(INSTALL_DIR)/$(SCRIPT_NAME)
	@echo "  $(SCRIPT_NAME) uninstalled successfully!"

clean:
	rm -f $(INSTALL_DIR)/$(SCRIPT_NAME)
	@echo " Cleaned up installation"

