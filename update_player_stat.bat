@echo off
rem set web_root=d:\.Minecraft.1.20-paper_world_n2\plugins\dynmap\web
set web_root=d:\_minecraft_site

python mine_stats.py
python publish_md.py
python site_map.py

copy _build\*.html %web_root%
copy _build\*.json %web_root%\assets\json

copy docs\*.png %web_root%