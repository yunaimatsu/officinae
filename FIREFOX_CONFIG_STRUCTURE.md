# Firefox設定のIaC化: MECE階層構造

## 目次
1. [アプリケーション設定](#1-アプリケーション設定)
2. [拡張機能](#2-拡張機能)
3. [ユーザーデータ](#3-ユーザーデータ)
4. [セキュリティ](#4-セキュリティ)
5. [統合設定](#5-統合設定)
6. [セッション/キャッシュ](#6-セッションキャッシュ)

---

## 1. アプリケーション設定

### 1.1 基本設定 (Preferences)

#### ファイル: `prefs.js` / `user.js`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/`
- **形式**: JavaScript
- **IaC適性**: ✅ 完全管理可能
- **説明**: すべてのabout:config設定

```javascript
// user.js (推奨: prefs.jsは自動生成されるため、user.jsで上書き)
user_pref("browser.tabs.closeWindowWithLastTab", false);
user_pref("browser.download.dir", "/home/user/Downloads");
user_pref("privacy.trackingprotection.enabled", true);
user_pref("privacy.trackingprotection.socialtracking.enabled", true);
user_pref("browser.urlbar.suggest.searches", false);
user_pref("browser.newtabpage.enabled", false);
user_pref("browser.startup.page", 3); // 前回のセッション復元
user_pref("general.smoothScroll", false);
user_pref("layout.css.devPixelsPerPx", "1.25"); // DPI設定
```

**主要カテゴリ**:
- `browser.*` - ブラウザ動作
- `privacy.*` - プライバシー設定
- `network.*` - ネットワーク設定
- `security.*` - セキュリティ設定
- `ui.*` / `layout.*` - UI/レイアウト

---

### 1.2 ポリシー (Enterprise Policies)

#### ファイル: `policies.json`
- **場所**: `/etc/firefox/policies/policies.json` (システム全体)
- **場所**: `~/.mozilla/firefox/policies/policies.json` (ユーザー)
- **形式**: JSON
- **IaC適性**: ✅ 完全管理可能
- **説明**: 強制的な設定（ユーザーが変更不可）

```json
{
  "policies": {
    "DisableTelemetry": true,
    "DisablePocket": true,
    "DisableFirefoxStudies": true,
    "DontCheckDefaultBrowser": true,
    "DisplayBookmarksToolbar": "always",
    "Homepage": {
      "URL": "https://example.com",
      "Locked": true,
      "StartPage": "homepage"
    },
    "ExtensionSettings": {
      "uBlock0@raymondhill.net": {
        "installation_mode": "force_installed",
        "install_url": "https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi"
      }
    },
    "Preferences": {
      "extensions.pocket.enabled": {
        "Value": false,
        "Status": "locked"
      }
    },
    "Proxy": {
      "Mode": "manual",
      "HTTPProxy": "proxy.example.com:8080",
      "UseHTTPProxyForAllProtocols": true
    }
  }
}
```

---

### 1.3 UI/UXカスタマイズ

#### ファイル: `chrome/userChrome.css`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/chrome/`
- **形式**: CSS
- **IaC適性**: ✅ 完全管理可能
- **説明**: Firefox UIのスタイル変更

```css
/* userChrome.css */
/* タブバーを非表示 */
#TabsToolbar {
  visibility: collapse !important;
}

/* URLバーを小さく */
#urlbar {
  max-height: 24px !important;
  font-size: 12px !important;
}

/* サイドバーのヘッダーを非表示 */
#sidebar-header {
  display: none !important;
}

/* コンパクトモード */
:root {
  --tab-min-height: 30px !important;
  --toolbarbutton-inner-padding: 6px !important;
}
```

#### ファイル: `chrome/userContent.css`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/chrome/`
- **形式**: CSS
- **IaC適性**: ✅ 完全管理可能
- **説明**: Webページコンテンツのスタイル変更

```css
/* userContent.css */
/* すべてのサイトでダークモード */
@-moz-document url-prefix(http://), url-prefix(https://) {
  * {
    background-color: #1a1a1a !important;
    color: #e0e0e0 !important;
  }
}

/* 特定ドメインのカスタマイズ */
@-moz-document domain("example.com") {
  .annoying-banner {
    display: none !important;
  }
}
```

#### ファイル: `xulstore.json`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/`
- **形式**: JSON
- **IaC適性**: △ 部分的に管理可能
- **説明**: ツールバーのカスタマイズ、ウィンドウサイズなど

```json
{
  "chrome://browser/content/browser.xhtml": {
    "main-window": {
      "screenX": "0",
      "screenY": "0",
      "width": "1920",
      "height": "1080",
      "sizemode": "maximized"
    },
    "PersonalToolbar": {
      "collapsed": "false"
    }
  }
}
```

---

## 2. 拡張機能

### 2.1 拡張機能リスト

#### ファイル: `addons.json` / `extensions.json`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/`
- **形式**: JSON
- **IaC適性**: ✅ リストは管理可能
- **説明**: インストール済み拡張機能の情報

```json
{
  "addons": [
    {
      "id": "uBlock0@raymondhill.net",
      "syncGUID": "{uuid}",
      "version": "1.58.0",
      "type": "extension",
      "loader": null,
      "updateURL": "https://addons.mozilla.org/...",
      "active": true
    }
  ]
}
```

**IaC化方法**:
```bash
# 拡張機能の自動インストール
EXTENSION_ID="uBlock0@raymondhill.net"
EXTENSION_URL="https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi"
wget -O "/tmp/${EXTENSION_ID}.xpi" "$EXTENSION_URL"
cp "/tmp/${EXTENSION_ID}.xpi" "~/.mozilla/firefox/PROFILE.default-release/extensions/${EXTENSION_ID}.xpi"
```

---

### 2.2 拡張機能データ

#### ディレクトリ: `browser-extension-data/`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/browser-extension-data/`
- **形式**: JSON
- **IaC適性**: △ 拡張機能による
- **説明**: 各拡張機能の設定データ

#### ファイル: `extension-preferences.json`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/`
- **形式**: JSON
- **IaC適性**: ✅ 管理可能

```json
{
  "uBlock0@raymondhill.net": {
    "permissions": ["storage", "webRequest", "webRequestBlocking"],
    "origins": ["<all_urls>"]
  }
}
```

---

## 3. ユーザーデータ

### 3.1 ブックマーク

#### ファイル: `places.sqlite`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/`
- **形式**: SQLite3
- **IaC適性**: ✅ エクスポート/インポート可能
- **説明**: ブックマーク、履歴、タグ

**スキーマ**:
```sql
-- ブックマークテーブル
CREATE TABLE moz_bookmarks (
  id INTEGER PRIMARY KEY,
  type INTEGER,           -- 1: bookmark, 2: folder, 3: separator
  fk INTEGER,            -- 外部キー to moz_places
  parent INTEGER,        -- 親フォルダID
  position INTEGER,      -- 表示順序
  title LONGVARCHAR,
  dateAdded INTEGER,     -- マイクロ秒
  lastModified INTEGER,
  guid TEXT UNIQUE
);

-- URL情報
CREATE TABLE moz_places (
  id INTEGER PRIMARY KEY,
  url LONGVARCHAR UNIQUE,
  title LONGVARCHAR,
  rev_host LONGVARCHAR,
  visit_count INTEGER DEFAULT 0,
  hidden INTEGER DEFAULT 0,
  typed INTEGER DEFAULT 0,
  frecency INTEGER DEFAULT -1,
  last_visit_date INTEGER,
  guid TEXT UNIQUE,
  foreign_count INTEGER DEFAULT 0,
  url_hash INTEGER DEFAULT 0,
  description TEXT,
  preview_image_url TEXT
);

-- 訪問履歴
CREATE TABLE moz_historyvisits (
  id INTEGER PRIMARY KEY,
  from_visit INTEGER,
  place_id INTEGER,
  visit_date INTEGER,
  visit_type INTEGER,
  session INTEGER
);

-- タグ
CREATE TABLE moz_tags (
  id INTEGER PRIMARY KEY,
  tag TEXT UNIQUE
);
```

**IaC化方法**:
```bash
# ブックマークのエクスポート (HTML形式)
sqlite3 places.sqlite <<EOF
.mode html
.output bookmarks.html
SELECT b.title, p.url
FROM moz_bookmarks b
JOIN moz_places p ON b.fk = p.id
WHERE b.type = 1;
.quit
EOF

# またはJSON形式で
sqlite3 places.sqlite <<EOF
.mode json
.output bookmarks.json
SELECT
  b.id, b.title, p.url, b.dateAdded, b.parent,
  (SELECT title FROM moz_bookmarks WHERE id = b.parent) as folder
FROM moz_bookmarks b
JOIN moz_places p ON b.fk = p.id
WHERE b.type = 1
ORDER BY b.dateAdded;
.quit
EOF
```

**ブックマークバックアップ**:
```bash
# Firefoxが自動生成するバックアップ
~/.mozilla/firefox/PROFILE.default-release/bookmarkbackups/
# bookmarks-2025-10-28_XXXXX.jsonlz4
```

---

### 3.2 履歴

#### ファイル: `places.sqlite` (上記と同じ)
- **IaC適性**: △ スナップショットとして管理可能

```sql
-- 履歴のクエリ例
SELECT
  p.url,
  p.title,
  datetime(v.visit_date/1000000, 'unixepoch') as visit_time,
  v.visit_type
FROM moz_historyvisits v
JOIN moz_places p ON v.place_id = p.id
ORDER BY v.visit_date DESC
LIMIT 100;
```

---

### 3.3 コンテナ (Multi-Account Containers)

#### ファイル: `containers.json`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/`
- **形式**: JSON
- **IaC適性**: ✅ 完全管理可能

```json
{
  "version": 5,
  "lastUserContextId": 5,
  "identities": [
    {
      "userContextId": 1,
      "public": true,
      "icon": "fingerprint",
      "color": "blue",
      "l10nId": "user-context-personal",
      "name": "Personal"
    },
    {
      "userContextId": 2,
      "public": true,
      "icon": "briefcase",
      "color": "orange",
      "l10nId": "user-context-work",
      "name": "Work"
    },
    {
      "userContextId": 3,
      "public": true,
      "icon": "dollar",
      "color": "green",
      "l10nId": "user-context-banking",
      "name": "Banking"
    },
    {
      "userContextId": 4,
      "public": true,
      "icon": "cart",
      "color": "pink",
      "l10nId": "user-context-shopping",
      "name": "Shopping"
    }
  ]
}
```

**カスタムコンテナ追加例**:
```json
{
  "userContextId": 6,
  "public": true,
  "icon": "fence",
  "color": "purple",
  "name": "Development",
  "accessKey": "D"
}
```

---

### 3.4 パスワード

#### ファイル: `logins.json` / `key4.db`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/`
- **形式**: JSON (暗号化) + SQLite3
- **IaC適性**: ❌ セキュリティ上非推奨

```json
{
  "nextId": 123,
  "logins": [
    {
      "id": 1,
      "hostname": "https://example.com",
      "httpRealm": null,
      "formSubmitURL": "https://example.com/login",
      "usernameField": "username",
      "passwordField": "password",
      "encryptedUsername": "...",
      "encryptedPassword": "...",
      "guid": "{uuid}",
      "timeCreated": 1234567890000,
      "timeLastUsed": 1234567890000,
      "timePasswordChanged": 1234567890000,
      "timesUsed": 5
    }
  ]
}
```

**key4.db (暗号鍵)**:
```sql
-- マスターパスワードで保護された鍵情報
CREATE TABLE metaData (
  id INTEGER PRIMARY KEY,
  item1 BLOB,  -- 暗号化アルゴリズム情報
  item2 BLOB   -- Salt
);

CREATE TABLE nssPrivate (
  id INTEGER PRIMARY KEY,
  a11 BLOB,  -- 暗号化された秘密鍵
  a102 BLOB
);
```

---

### 3.5 Cookie

#### ファイル: `cookies.sqlite`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/`
- **形式**: SQLite3
- **IaC適性**: △ スナップショットとして管理可能（セキュリティ注意）

```sql
CREATE TABLE moz_cookies (
  id INTEGER PRIMARY KEY,
  originAttributes TEXT NOT NULL DEFAULT '',
  name TEXT,
  value TEXT,
  host TEXT,
  path TEXT,
  expiry INTEGER,
  lastAccessed INTEGER,
  creationTime INTEGER,
  isSecure INTEGER,
  isHttpOnly INTEGER,
  inBrowserElement INTEGER DEFAULT 0,
  sameSite INTEGER DEFAULT 0,
  rawSameSite INTEGER DEFAULT 0,
  schemeMap INTEGER DEFAULT 0,
  CONSTRAINT moz_uniqueid UNIQUE (name, host, path, originAttributes)
);
```

**Cookie エクスポート例**:
```bash
sqlite3 cookies.sqlite <<EOF
.mode json
.output cookies_backup.json
SELECT host, name, value, path, expiry, isSecure, isHttpOnly, sameSite
FROM moz_cookies
WHERE host LIKE '%example.com%';
.quit
EOF
```

---

## 4. セキュリティ

### 4.1 証明書

#### ファイル: `cert9.db`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/`
- **形式**: SQLite3 (NSS database)
- **IaC適性**: △ 部分的に管理可能

```sql
-- 証明書データベーススキーマ
CREATE TABLE nssPublic (
  id INTEGER PRIMARY KEY,
  a0 BLOB,   -- DER encoded certificate
  a1 BLOB,
  a2 BLOB,
  a3 BLOB
);

CREATE TABLE nssPrivate (
  id INTEGER PRIMARY KEY,
  a0 BLOB,   -- Encrypted private key
  a1 BLOB
);
```

**証明書インポート**:
```bash
# PKCS#12形式の証明書をインポート
certutil -d sql:~/.mozilla/firefox/PROFILE.default-release -A \
  -n "My Certificate" -t "u,u,u" -i certificate.pem
```

---

### 4.2 セキュリティ状態

#### ファイル: `SiteSecurityServiceState.bin`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/`
- **形式**: Binary
- **IaC適性**: ❌ 管理困難
- **説明**: HSTS (HTTP Strict Transport Security) 情報

#### ディレクトリ: `security_state/`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/security_state/`
- **IaC適性**: ❌ 管理困難

---

### 4.3 許可設定

#### ファイル: `permissions.sqlite`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/`
- **形式**: SQLite3
- **IaC適性**: ✅ 管理可能

```sql
CREATE TABLE moz_hosts (
  id INTEGER PRIMARY KEY,
  host TEXT,
  type TEXT,        -- 許可タイプ (例: "cookie", "geo", "camera")
  permission INTEGER, -- 1: allow, 2: deny, 0: unknown
  expireType INTEGER,
  expireTime INTEGER,
  modificationTime INTEGER
);

CREATE TABLE moz_perms (
  id INTEGER PRIMARY KEY,
  origin TEXT UNIQUE,
  type TEXT,
  permission INTEGER,
  expireType INTEGER,
  expireTime INTEGER,
  modificationTime INTEGER
);
```

**許可設定のエクスポート**:
```sql
-- カメラ/マイク許可
SELECT origin, type,
  CASE permission
    WHEN 1 THEN 'allow'
    WHEN 2 THEN 'deny'
    ELSE 'unknown'
  END as permission
FROM moz_perms
WHERE type IN ('camera', 'microphone', 'geo', 'desktop-notification');
```

**IaC化例**:
```bash
sqlite3 permissions.sqlite <<EOF
INSERT INTO moz_perms (origin, type, permission, expireType, expireTime, modificationTime)
VALUES
  ('https://meet.google.com', 'camera', 1, 0, 0, $(date +%s)000),
  ('https://meet.google.com', 'microphone', 1, 0, 0, $(date +%s)000);
EOF
```

---

## 5. 統合設定

### 5.1 検索エンジン

#### ファイル: `search.json.mozlz4`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/`
- **形式**: LZ4圧縮されたJSON
- **IaC適性**: ✅ 管理可能（解凍/圧縮必要）

**解凍方法**:
```python
#!/usr/bin/env python3
import lz4.block
import sys

with open('search.json.mozlz4', 'rb') as f:
    magic = f.read(8)  # "mozLz40\0"
    if magic != b'mozLz40\0':
        raise ValueError("Invalid file format")
    data = lz4.block.decompress(f.read())
    print(data.decode('utf-8'))
```

**JSONフォーマット**:
```json
{
  "version": 8,
  "engines": [
    {
      "_name": "Google",
      "_shortName": "google",
      "description": "Google Search",
      "queryCharset": "UTF-8",
      "_iconURL": "https://www.google.com/favicon.ico",
      "_urls": [
        {
          "template": "https://www.google.com/search",
          "params": [
            {"name": "q", "value": "{searchTerms}"},
            {"name": "ie", "value": "utf-8"}
          ]
        }
      ]
    },
    {
      "_name": "DuckDuckGo",
      "_shortName": "ddg",
      "description": "DuckDuckGo Privacy Search",
      "queryCharset": "UTF-8",
      "_iconURL": "https://duckduckgo.com/favicon.ico",
      "_urls": [
        {
          "template": "https://duckduckgo.com/",
          "params": [{"name": "q", "value": "{searchTerms}"}]
        }
      ]
    }
  ],
  "metaData": {
    "current": "DuckDuckGo",
    "hash": "..."
  }
}
```

---

### 5.2 ファイルハンドラー

#### ファイル: `handlers.json`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/`
- **形式**: JSON
- **IaC適性**: ✅ 完全管理可能

```json
{
  "defaultHandlersVersion": {},
  "mimeTypes": {
    "application/pdf": {
      "action": 3,  // 0: save, 1: open with default, 2: always ask, 3: use Firefox viewer
      "extensions": ["pdf"]
    },
    "image/webp": {
      "action": 3,
      "extensions": ["webp"]
    },
    "application/x-msdownload": {
      "action": 0,
      "ask": true
    },
    "video/mp4": {
      "action": 1,
      "handlers": [
        {
          "name": "VLC",
          "path": "/usr/bin/vlc"
        }
      ]
    }
  },
  "schemes": {
    "mailto": {
      "stubEntry": true,
      "handlers": [
        null,
        {
          "name": "Gmail",
          "uriTemplate": "https://mail.google.com/mail/?extsrc=mailto&url=%s"
        }
      ]
    },
    "magnet": {
      "action": 4,  // Use system handler
      "handlers": [
        {
          "name": "Transmission",
          "path": "/usr/bin/transmission-gtk"
        }
      ]
    }
  },
  "isDownloadsImprovementsAlreadyMigrated": false
}
```

---

### 5.3 プロトコルハンドラー

上記 `handlers.json` の `schemes` セクションで管理

---

## 6. セッション/キャッシュ

### 6.1 セッション

#### ファイル: `sessionstore.jsonlz4`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/`
- **形式**: LZ4圧縮されたJSON
- **IaC適性**: △ スナップショットとして管理可能

```json
{
  "version": ["sessionrestore", 1],
  "windows": [
    {
      "tabs": [
        {
          "entries": [
            {
              "url": "https://example.com",
              "title": "Example Domain",
              "charset": "UTF-8"
            }
          ],
          "lastAccessed": 1234567890000,
          "index": 1,
          "userContextId": 0
        }
      ],
      "selected": 1,
      "_closedTabs": []
    }
  ]
}
```

#### ファイル: `sessionCheckpoints.json`
```json
{
  "profile-after-change": true,
  "final-ui-startup": true,
  "sessionstore-windows-restored": true,
  "quit-application-granted": true,
  "quit-application": true,
  "sessionstore-final-state-write-complete": true
}
```

---

### 6.2 キャッシュ

#### ディレクトリ: `cache2/`
- **場所**: `~/.cache/mozilla/firefox/PROFILE.default-release/cache2/`
- **IaC適性**: ❌ 管理不要（一時ファイル）

#### ファイル: `webappsstore.sqlite`
- **場所**: `~/.mozilla/firefox/PROFILE.default-release/`
- **形式**: SQLite3
- **IaC適性**: △ スナップショット可能
- **説明**: localStorage データ

```sql
CREATE TABLE webappsstore2 (
  originAttributes TEXT,
  originKey TEXT,
  scope TEXT,
  key TEXT,
  value TEXT,
  secure INTEGER,
  owner TEXT
);
```

---

## 7. その他の重要ファイル

### 7.1 フォーム履歴

#### ファイル: `formhistory.sqlite`
```sql
CREATE TABLE moz_formhistory (
  id INTEGER PRIMARY KEY,
  fieldname TEXT NOT NULL,
  value TEXT NOT NULL,
  timesUsed INTEGER,
  firstUsed INTEGER,
  lastUsed INTEGER,
  guid TEXT UNIQUE
);
```

---

### 7.2 コンテンツ設定

#### ファイル: `content-prefs.sqlite`
```sql
CREATE TABLE prefs (
  id INTEGER PRIMARY KEY,
  setting TEXT UNIQUE NOT NULL
);

CREATE TABLE groups (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL  -- ドメイン名
);

CREATE TABLE prefs_values (
  id INTEGER PRIMARY KEY,
  groupID INTEGER REFERENCES groups(id),
  settingID INTEGER NOT NULL REFERENCES prefs(id),
  value BLOB
);
```

**例**: サイトごとのズーム設定
```sql
SELECT g.name, p.setting, v.value
FROM prefs_values v
JOIN groups g ON v.groupID = g.id
JOIN prefs p ON v.settingID = p.id
WHERE p.setting = 'zoom';
```

---

### 7.3 Favicon

#### ファイル: `favicons.sqlite`
```sql
CREATE TABLE moz_icons (
  id INTEGER PRIMARY KEY,
  icon_url TEXT UNIQUE,
  fixed_icon_url_hash INTEGER,
  width INTEGER NOT NULL DEFAULT 0,
  root INTEGER NOT NULL DEFAULT 0,
  color INTEGER,
  expire_ms INTEGER NOT NULL DEFAULT 0,
  data BLOB
);

CREATE TABLE moz_pages_w_icons (
  id INTEGER PRIMARY KEY,
  page_url TEXT UNIQUE NOT NULL,
  page_url_hash INTEGER NOT NULL
);

CREATE TABLE moz_icons_to_pages (
  page_id INTEGER NOT NULL,
  icon_id INTEGER NOT NULL,
  expire_ms INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (page_id, icon_id)
);
```

---

## IaC管理の優先度マトリックス

| カテゴリ | ファイル | IaC適性 | 優先度 | 管理方法 |
|---------|---------|---------|--------|---------|
| 基本設定 | user.js | ✅ | 高 | Git管理 |
| ポリシー | policies.json | ✅ | 高 | Git管理 |
| UI | userChrome.css | ✅ | 高 | Git管理 |
| UI | userContent.css | ✅ | 中 | Git管理 |
| コンテナ | containers.json | ✅ | 高 | Git管理 |
| ハンドラー | handlers.json | ✅ | 中 | Git管理 |
| 拡張機能リスト | addons.json | ✅ | 高 | スクリプト |
| ブックマーク | places.sqlite | ✅ | 中 | エクスポート/インポート |
| 許可設定 | permissions.sqlite | ✅ | 中 | SQLスクリプト |
| 検索エンジン | search.json.mozlz4 | ✅ | 中 | 圧縮/解凍スクリプト |
| セッション | sessionstore.jsonlz4 | △ | 低 | バックアップのみ |
| Cookie | cookies.sqlite | △ | 低 | バックアップのみ |
| 履歴 | places.sqlite (visits) | △ | 低 | バックアップのみ |
| パスワード | logins.json | ❌ | - | 外部ツール推奨 |
| 証明書 | cert9.db | △ | 低 | certutil |
| キャッシュ | cache2/ | ❌ | - | 管理不要 |

---

## 実装ガイド

### Makefileへの統合例

```makefile
FIREFOX_PROFILE := $(HOME)/.mozilla/firefox/a2v38d27.default-release
FIREFOX_CHROME := $(FIREFOX_PROFILE)/chrome

.PHONY: firefox-setup
firefox-setup: firefox-dirs firefox-config firefox-extensions

firefox-dirs:
	mkdir -p $(FIREFOX_CHROME)
	mkdir -p $(HOME)/.mozilla/firefox/policies

firefox-config:
	ln -sf $(PWD)/FIREFOX_USER_JS $(FIREFOX_PROFILE)/user.js
	ln -sf $(PWD)/FIREFOX_CHROME_CSS $(FIREFOX_CHROME)/userChrome.css
	ln -sf $(PWD)/FIREFOX_CONTENT_CSS $(FIREFOX_CHROME)/userContent.css
	ln -sf $(PWD)/FIREFOX_CONTAINERS_JSON $(FIREFOX_PROFILE)/containers.json
	ln -sf $(PWD)/FIREFOX_HANDLERS_JSON $(FIREFOX_PROFILE)/handlers.json
	sudo ln -sf $(PWD)/FIREFOX_POLICIES_JSON /etc/firefox/policies/policies.json

firefox-extensions:
	./scripts/install-firefox-extensions.sh

firefox-backup:
	./scripts/backup-firefox-data.sh
```

### 拡張機能インストールスクリプト例

```bash
#!/bin/bash
# scripts/install-firefox-extensions.sh

PROFILE="$HOME/.mozilla/firefox/a2v38d27.default-release"
EXTENSIONS_DIR="$PROFILE/extensions"

mkdir -p "$EXTENSIONS_DIR"

# 拡張機能リスト
declare -A extensions=(
  ["uBlock0@raymondhill.net"]="https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi"
  ["treestyletab@piro.sakura.ne.jp"]="https://addons.mozilla.org/firefox/downloads/latest/tree-style-tab/latest.xpi"
  ["{446900e4-71c2-419f-a6a7-df9c091e268b}"]="https://addons.mozilla.org/firefox/downloads/latest/bitwarden-password-manager/latest.xpi"
)

for id in "${!extensions[@]}"; do
  url="${extensions[$id]}"
  echo "Installing $id..."
  wget -O "$EXTENSIONS_DIR/$id.xpi" "$url"
done
```

### データバックアップスクリプト例

```bash
#!/bin/bash
# scripts/backup-firefox-data.sh

PROFILE="$HOME/.mozilla/firefox/a2v38d27.default-release"
BACKUP_DIR="$HOME/musea/firefox-backups/$(date +%Y%m%d)"

mkdir -p "$BACKUP_DIR"

# ブックマークのエクスポート
sqlite3 "$PROFILE/places.sqlite" <<EOF
.mode json
.output $BACKUP_DIR/bookmarks.json
SELECT b.id, b.title, p.url, b.dateAdded, b.parent
FROM moz_bookmarks b
JOIN moz_places p ON b.fk = p.id
WHERE b.type = 1;
.quit
EOF

# 許可設定のエクスポート
sqlite3 "$PROFILE/permissions.sqlite" <<EOF
.mode json
.output $BACKUP_DIR/permissions.json
SELECT * FROM moz_perms;
.quit
EOF

echo "Backup completed: $BACKUP_DIR"
```

---

## 参考資料

- [Mozilla Firefox Profile Files](https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data)
- [Enterprise Policy Documentation](https://github.com/mozilla/policy-templates)
- [userChrome.css Examples](https://www.userchrome.org/)
- [SQLite Database Schema](https://dxr.mozilla.org/mozilla-central/source/)
