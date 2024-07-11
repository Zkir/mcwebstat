@echo off
rem set web_root=d:\.Minecraft.1.20-paper_world_n2\plugins\dynmap\web
set web_root=d:\__2\html1

python mine_stats.py
python publish_md.py
copy *.html %web_root%
copy _build\*.html %web_root%
copy docs\*.png %web_root%