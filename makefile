.PHONY: romchverse vga romchverse-sync vga-sync romchverse-notify vga-notify

romchverse:
	BOT_ENV=.env.romchverse uv run bot

vga:
	BOT_ENV=.env.vga uv run bot

romchverse-sync:
	BOT_ENV=.env.romchverse uv run bot-sync

vga-sync:
	BOT_ENV=.env.vga uv run bot-sync

romchverse-notify:
	BOT_ENV=.env.romchverse uv run bot-notify

vga-notify:
	BOT_ENV=.env.vga uv run bot-notify
