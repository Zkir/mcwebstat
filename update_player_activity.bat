@echo off
set web_root=d:\_minecraft_site

python activity_stats.py

copy _build\activity\*.png %web_root%\activity


