# musea - Browser Configuration as Code

IaC (Infrastructure as Code) for browser configurations (Qutebrowser & Firefox).

## Features

- **Qutebrowser**: Complete configuration management
- **Firefox**: Comprehensive settings, UI customization, containers, extensions
- **Version Control**: All configurations tracked in Git
- **Easy Deployment**: Single command setup with Makefile
- **Backup Scripts**: Automated data backup for Firefox

## Setup

```bash
# Setup everything (Qutebrowser + Firefox)
make all

# Or setup individually
make mapping           # Qutebrowser only
make firefox           # Firefox only
make firefox-config    # Firefox config files only
make firefox-extensions # Install Firefox extensions
```

## Firefox Configuration

See [FIREFOX_CONFIG_STRUCTURE.md](FIREFOX_CONFIG_STRUCTURE.md) for detailed documentation.

### Files Managed

- `FIREFOX_USER_JS` - All Firefox preferences (about:config)
- `FIREFOX_CHROME_CSS` - UI customization (userChrome.css)
- `FIREFOX_CONTAINERS_JSON` - Multi-Account Containers
- `FIREFOX_HANDLERS_JSON` - File/protocol handlers
- `FIREFOX_POLICIES_JSON` - Enterprise policies

### Backup

```bash
make firefox-backup
```

Backups are stored in `firefox-backups/` with timestamp.

## Structure

```
musea/
├── Makefile                    # Main automation
├── mapping                     # Qutebrowser mappings
├── QUTE_BROWSER_CONFIG*.py     # Qutebrowser configs
├── FIREFOX_*                   # Firefox config files
├── scripts/
│   ├── install-firefox-extensions.sh
│   └── backup-firefox-data.sh
└── FIREFOX_CONFIG_STRUCTURE.md # Comprehensive docs
```

## Requirements

- Firefox / Qutebrowser
- sqlite3 (for backups)
- wget (for extension installation)