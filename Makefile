include $(TOPDIR)/rules.mk

PKG_NAME:=easy-websockd-python
PKG_RELEASE:=1

PKG_MAINTAINER:=Jiwan Kim <wldhks1004@naver.com>

include $(INCLUDE_DIR)/package.mk

define Package/easy-websockd-python
  SECTION:=Kaonbroadband
  CATEGORY:=Kaonbroadband
  TITLE:=Easy WebSocket Python Server
  DEPENDS:=+python3-light +python3-email +python3-urllib +python3-openssl
endef

define Package/easy-websockd-python/description
  A simple Python-based JSON-RPC WebSocket server that executes ubus commands and auto-starts on boot.
endef

define Build/Compile
	# Skip...
endef

define Package/easy-websockd-python/install
	$(INSTALL_DIR) $(1)/sbin
	$(INSTALL_BIN) ./files/sbin/server.py $(1)/sbin/server.py
	$(INSTALL_BIN) ./files/sbin/SimpleWebSocketServer.py $(1)/sbin/SimpleWebSocketServer.py

	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/etc/init.d/easy-websockd-python $(1)/etc/init.d/easy-websockd-python
endef

$(eval $(call BuildPackage,easy-websockd-python))
