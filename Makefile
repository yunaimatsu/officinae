SHELL := /bin/bash
MAP_FILE := mapping

# Firefox configuration
FIREFOX_PROFILE := $(HOME)/.mozilla/firefox/a2v38d27.default-release
FIREFOX_CHROME := $(FIREFOX_PROFILE)/chrome
FIREFOX_POLICIES_DIR := /etc/firefox/policies

# Targets
.PHONY: all mapping firefox firefox-config firefox-extensions firefox-backup help

all: mapping firefox

help:
	@echo "Available targets:"
	@echo "  all              - Setup Qutebrowser and Firefox"
	@echo "  mapping          - Link Qutebrowser configs"
	@echo "  firefox          - Setup Firefox (config + extensions)"
	@echo "  firefox-config   - Link Firefox configuration files"
	@echo "  firefox-extensions - Install Firefox extensions"
	@echo "  firefox-backup   - Backup Firefox data"
	@echo "  help             - Show this help message"

mapping:
	@while IFS=':' read -r src dest; do \
		src_path="$$HOME/musea/$$src"; \
		dest_path=$$(eval echo $$dest); \
		sudo ln -sf "$$src_path" "$$dest_path"; \
		echo "Linked $$src -> $$dest"; \
	done < $(MAP_FILE)

firefox: firefox-config firefox-extensions

firefox-config:
	@echo "Setting up Firefox configuration..."
	@mkdir -p $(FIREFOX_CHROME)
	@mkdir -p $(HOME)/.mozilla/firefox/policies
	@ln -sf $(PWD)/FIREFOX_USER_JS $(FIREFOX_PROFILE)/user.js
	@echo "Linked user.js"
	@ln -sf $(PWD)/FIREFOX_CHROME_CSS $(FIREFOX_CHROME)/userChrome.css
	@echo "Linked userChrome.css"
	@ln -sf $(PWD)/FIREFOX_CONTAINERS_JSON $(FIREFOX_PROFILE)/containers.json
	@echo "Linked containers.json"
	@ln -sf $(PWD)/FIREFOX_HANDLERS_JSON $(FIREFOX_PROFILE)/handlers.json
	@echo "Linked handlers.json"
	@if [ -w $(FIREFOX_POLICIES_DIR) ] || sudo -n true 2>/dev/null; then \
		sudo mkdir -p $(FIREFOX_POLICIES_DIR); \
		sudo ln -sf $(PWD)/FIREFOX_POLICIES_JSON $(FIREFOX_POLICIES_DIR)/policies.json; \
		echo "Linked policies.json (system-wide)"; \
	else \
		ln -sf $(PWD)/FIREFOX_POLICIES_JSON $(HOME)/.mozilla/firefox/policies/policies.json; \
		echo "Linked policies.json (user-level, no sudo)"; \
	fi
	@echo "Firefox configuration complete!"
	@echo "Restart Firefox to apply changes."

firefox-extensions:
	@echo "Installing Firefox extensions..."
	@./scripts/install-firefox-extensions.sh

firefox-backup:
	@echo "Backing up Firefox data..."
	@./scripts/backup-firefox-data.sh
