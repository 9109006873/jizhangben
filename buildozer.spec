[app]

# (str) Title of your application
# 注意：中文标题在某些打包环境下会导致编码错误，如果打包报错，请改为英文，如 My Account Book
title = 我的记账本

# (str) Package name
package.name = jizhangben

# (str) Package domain (needed for android/ios packaging)
package.domain = com.jizhangben

# (str) Source code where the main.py lives
source.dir = .

# (str) Application version
version = 1.0.0

# (list) Application requirements
# 添加了 et_xmlfile，因为 openpyxl 依赖它
requirements = python3,kivy==2.3.1,openpyxl==3.1.5,et_xmlfile

# (str) Supported orientation (portrait, landscape, all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Presplash of the application
presplash.filename =

# (str) Icon of the application
icon.filename =

# (list) List of service to declare
services =

# ========== 新增的核心配置，用于解决 aidl/build-tools 报错 ==========
# 自动接受 Android SDK 许可协议（必须！否则会卡在 aidl not found）
android.accept_sdk_license = True

# 设置日志级别为 2，方便看到下载和许可协议的提示
log_level = 2

# 指定目标 CPU 架构，现代手机通常只需 arm64-v8a，可大幅缩短构建时间
android.archs = arm64-v8a

# 指定 Android API 版本
android.api = 34
android.minapi = 21

# 指定 Android NDK 版本（如果本地没有，buildozer 会自动下载）
# android.ndk = 25b
# ===================================================================

[buildozer]

# (str) Directory where buildozer should store its global data
build_dir = .buildozer

# (str) Directory where buildozer should store the generated apk
bin_dir = bin

# (str) Warn about deprecated buildozer.spec options
warn_on_root = 1
