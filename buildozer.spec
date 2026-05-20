[app]
title = ConnekTor
package.name = connektor
package.domain = org.citpc
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,otf,json,ini
version = 4.0.0
<<<<<<< HEAD
requirements = kivy==2.3.0,kivymd,requests,certifi,chardet,charset-normalizer,urllib3,idna,six,filetype
=======
requirements = kivy==2.3.0,kivymd,requests,certifi,chardet,charset-normalizer,urllib3,idna,six,filetype
>>>>>>> 1379fb34537b8862cf0db512d119646077a16a08
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
