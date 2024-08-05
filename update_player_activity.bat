@echo off
rem set web_root=d:\.Minecraft.1.20-paper_world_n2\plugins\dynmap\web
set web_root=d:\_minecraft_site

python activity_stats.py

copy _build\activity\*.png %web_root%\activity


