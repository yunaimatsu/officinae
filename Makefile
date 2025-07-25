SHELL := /bin/zsh 

OFFICINAE := $(HOME)/officinae
MAP_FILE := mapping

map:
	@while IFS=':' read -r src dest; do \
		src_path="$(OFFICINAE)/$$src"; \
		dest_path=$$(eval echo $$dest); \
		sudo ln -sf "$$src_path" "$$dest_path"; \
		echo "Linked $$src -> $$dest"; \
	done < $(MAP_FILE)

locale:
	echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
	locale-gen
	echo "LANG=en_US.UTF-8" > /etc/locale.conf
	sudo localectl set-locale LANG=en_US.UTF-8
	sudo localectl set-keymap us
	sudo localectl status

fonts:
	sudo pacman -S noto-fonts noto-fonts-cjk noto-fonts-emoji
	sudo pacman -S fcitx5-im fcitx5-mozc fcitx5-configtool

nw:
# systemctl enable NetworkManager

x:
	touch "$HOME/.xprofile"
	w 'export GTK_IM_MODULE=fcitx' ~/.profile
	w 'export QT_IM_MODULE=fcitx' ~/.profile
	w 'export XMODIFIERS="@im=fcitx"' ~/.profile
	w 'fcitx5 &' ~/.profile
