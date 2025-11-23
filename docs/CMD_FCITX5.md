# Fcitx5

## `fcitx5` vs `fcitx5-remote`

| Aspect | `fcitx5` | `fcitx5-remote` |
|--------|----------|-----------------|
| **Role** | The input method **daemon** itself | A **client** that talks to the daemon |
| **Function** | Runs the actual input method service | Sends commands to a running daemon |
| **Lifecycle** | Long-running process | Executes once and exits |
| **Typical use** | Started once at login/session start | Called repeatedly for control tasks |

## Analogy

Think of it like a music player:

- `fcitx5` = The music player application running in the background
- `fcitx5-remote` = A remote control to play, pause, skip tracks, etc.

## Practical Example

```bash
# Start the daemon (do this once)
fcitx5 -d

# Now use fcitx5-remote to control it
fcitx5-remote -t      # toggle input method
fcitx5-remote -s pinyin   # switch to pinyin
fcitx5-remote -e      # tell the daemon to exit
```

## Why Two Separate Commands?

This is a common Unix design pattern (client-server separation):

1. **Stability** — The daemon runs continuously; a buggy client won't crash the daemon
2. **Scripting** — You can easily control input methods from shell scripts or keybindings
3. **IPC** — `fcitx5-remote` communicates via D-Bus, allowing any program to control fcitx5

In short: `fcitx5` **is** the input method engine, while `fcitx5-remote` **controls** it.
Fcitx5 is a lightweight input method framework for Linux. Here's a comprehensive breakdown of its commands organized by function.

## 1. Core Daemon Commands

| Command | Purpose |
|---------|---------|
| `fcitx5` | Start the main input method daemon |
| `fcitx5 -d` | Start in daemon mode (background) |
| `fcitx5 -r` | Replace an existing running instance |
| `fcitx5 --enable <addon>` | Start with specific addon enabled |
| `fcitx5 --disable <addon>` | Start with specific addon disabled |

## 2. Remote Control Commands (`fcitx5-remote`)

These control a running fcitx5 instance:

**State queries:**
- `fcitx5-remote` — Print current input method state (1=inactive, 2=active)
- `fcitx5-remote -c` — Deactivate input method (switch to direct input)
- `fcitx5-remote -o` — Activate input method
- `fcitx5-remote -t` — Toggle input method state

**Input method switching:**
- `fcitx5-remote -s <im-name>` — Switch to a specific input method by name
- `fcitx5-remote -g` — Get current input method group
- `fcitx5-remote -G <group>` — Set input method group

**Information retrieval:**
- `fcitx5-remote -n` — Get current input method name
- `fcitx5-remote -m` — List all available input methods

**Lifecycle control:**
- `fcitx5-remote -e` — Exit fcitx5
- `fcitx5-remote -a` — Reload configuration
- `fcitx5-remote -r` — Reload addon configuration

## 3. Configuration Tools

| Command | Purpose |
|---------|---------|
| `fcitx5-configtool` | Launch the graphical configuration GUI |
| `fcitx5-diagnose` | Run diagnostics and print environment/configuration status |

## 4. Diagnostic & Debugging Commands

| Command | Purpose |
|---------|---------|
| `fcitx5-diagnose` | Comprehensive system diagnostic (checks environment variables, installed addons, etc.) |
| `fcitx5 --verbose=<level>` | Run with specified verbosity for debugging |

## 5. Dictionary/Data Management

These vary by input method addon, but common ones include:

| Command | Purpose |
|---------|---------|
| `libime_pinyindict` | Build/convert pinyin dictionary files |
| `libime_tabledict` | Build/convert table-based dictionary files |
| `libime_history` | Manage input history data |
| `libime_migrate` | Migrate data from fcitx4 to fcitx5 |

## Summary Matrix

| Category | Commands |
|----------|----------|
| **Daemon** | `fcitx5`, `fcitx5 -d`, `fcitx5 -r` |
| **Remote Control** | `fcitx5-remote` (with various flags) |
| **Configuration** | `fcitx5-configtool` |
| **Diagnostics** | `fcitx5-diagnose`, `fcitx5 --verbose` |
| **Data Tools** | `libime_*` utilities |

To see all available options for any command, use `--help`, for example: `fcitx5 --help` or `fcitx5-remote --help`.
