config.load_autoconfig(False)
from tab import tab
from statusbar import statusbar
from completion import completion
tab(c, config)
statusbar(c, config)
completion(c, config)

# WebRTC基本設定
c.content.webrtc_ip_handling_policy = "all-interfaces"
c.colors.webpage.darkmode.enabled=False

# より強力なChromium引数
c.qt.args = [
    # WebRTC基本
    "--enable-webrtc",
    "--enable-webrtc-remote-event-log",
    
    # メディアデバイス
    "--enable-media-stream",
    "--use-fake-ui-for-media-stream",
    "--use-fake-device-for-media-stream",  # テスト用
    "--enable-usermedia-screen-capturing",
    
    # GPU/ハードウェア加速
    "--enable-gpu-rasterization",
    "--ignore-gpu-blacklist",
    "--disable-gpu-sandbox",
    
    # セキュリティ関連（テスト用）
    "--allow-running-insecure-content",
    "--disable-web-security",
    "--disable-features=VizDisplayCompositor",
    "--enable-features=VaapiVideoDecoder"
    "--autoplay-policy=no-user-gesture-required",
    "--enable-logging=stderr",
    "--v=1"

    # デバッグ用
    "--enable-logging",
    "--log-level=0",
    "--vmodule=*media*=3"
]

config.bind('<Ctrl-b>', 'config-cycle tabs.show always never')
config.bind('<Ctrl-g>', 'mode-leave', mode='passthrough')

# メディア許可
c.content.media.audio_capture = True
c.content.media.video_capture = True
c.content.media.audio_video_capture = True

# 自動許可設定（Meetの場合）
c.content.notifications.enabled = True
c.content.autoplay = True

# Media
c.content.media.audio_capture = True
c.content.media.video_capture = True
c.content.media.audio_video_capture = True
c.content.desktop_capture = True
# HTTPS以外でのWebRTC使用許可（テスト用）
# c.content.tls.insecure_ciphers = True
c.content.javascript.enabled = True
# カメラ・マイクアクセス許可
c.content.media.audio_capture = True
c.content.media.video_capture = True
c.content.media.audio_video_capture = True

c.tabs.position = 'left'
c.fonts.default_size = '8pt'
c.fonts.default_family = 'JetBrains Mono'

# Vibrant, high-contrast colors for hints
c.colors.hints.fg = "#FFFFFF"          # White text
c.colors.hints.bg = "#1e1e2e"          # Dark purple background
c.colors.hints.match.fg = "#f7768e"    # Neon pink for matched text

# Standout font
c.fonts.hints = "bold 8pt JetBrains Mono, monospace"

# Padding and rounded corners for a pill effect
c.hints.padding = { 'top': 1, 'right': 4, 'bottom': 1, 'left': 4 }
c.hints.radius = 3

# Border using a neon-like color
c.hints.border = "1px solid #7dcfff"   # Cyan neon border

# Uncommon, visually striking hint characters
# c.hints.chars = 'NEONXZCV'

# (Optional) Make hint tags uppercase for emphasis
c.hints.uppercase = True

# Start color of the tab indicator (progress bar in tabs)
c.colors.tabs.indicator.start = '#2ECC40'

# End color for the indicator gradient
c.colors.tabs.indicator.stop = '#FFDC00'

# Color for the tab indicator when there is an error
c.colors.tabs.indicator.error = 'red'

# Key-remapping
c.bindings.key_mappings = {"<Ctrl-G>": "<Escape>"}
c.url.start_pages = 'https://perplexity.ai'
c.url.default_page = 'https://perplexity.ai'
c.url.searchengines = {
  'DEFAULT': 'https://perplexity.ai?q={}',
  'a': 'https://amazon.co.jp/s?k={}',
  'g': 'https://google.com/search?q={}',
  'r': 'https://reddit.com/search/?q={}',
  'c': 'https://chat.openai.com/?q={}',
  'm': 'https://google.com/maps/search/{}',
  'yt': 'https://youtube.com/results?search_query={}',
  'dr': 'https://drive.google.com/drive/search?q={}',
  'tw': 'https://x.com/search?q={}',
  'wt': 'https://en.wiktionary.org/wiki/{}',
  'wk': 'https://en.wikipedia.org/wiki/{}',
  'gh': 'https://github.com/search?q={}',
  'gl': 'https://gitlab.com/search?search={}',
  'sc': 'https://scholar.google.com/scholar?q={}',
  # 'gm': 'https://www.google.com/search?q=site:gemini.google.com+{}',
  'cl': 'https://claude.ai/new?q={}',
  'aur': 'https://aur.archlinux.org/packages?K={}',
  'rae': 'https://dle.rae.es/{}',
  'per': 'https://perplexity.ai/search?q={}',
  'ytm': 'https://music.youtube.com/search?q={}',
  'esja': 'https://kotobank.jp/esjaword/{}'
}

def map(key, command):
    config.unbind(key)
    config.bind(key, command)

map('j', 'scroll down')
map('k', 'scroll up')
map('h', 'scroll left')
map('l', 'scroll right')
# map('H', 'tab-prev')
# map('L', 'tab-next')
