[app]
title = ConnekTor
package.name = connektor
package.domain = org.citpc
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,otf,json,ini
version = 4.0.0
requirements = python3,kivy==2.3.0,kivymd,requests,certifi,charset-normalizer,urllib3,idna
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,ACCESS_NETWORK_STATE,CHANGE_NETWORK_STATE
android.minapi = 21
android.targetapi = 33
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
