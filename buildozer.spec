[app]

title = 我的记账本
package.name = jizhangben
package.domain = com.jizhangben

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,txt,json,xlsx

version = 1.0.0

requirements = python3,kivy==2.3.1,openpyxl==3.1.5

orientation = portrait
fullscreen = 0

presplash.filename =
icon.filename =

android.api = 33
android.minapi = 24
android.ndk = 28c

android.archs = arm64-v8a,armeabi-v7a

android.accept_sdk_license = True

p4a.branch = develop
p4a.commit = 0382d27

[buildozer]

build_dir = .buildozer
bin_dir = bin

warn_on_root = 1

log_level = 2
