@echo off
set web_root=d:\_minecraft_site

python mine_stats.py
python publish_md.py
python site_map.py
python medal_stats.py

copy _build\*.html %web_root%
copy _build\*.json %web_root%\assets\json

copy docs\*.png %web_root%