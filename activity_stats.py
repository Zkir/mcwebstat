#python -m pip install --upgrade Pillow
#python -m pip install mysql-connector-python

from PIL import Image, ImageDraw
import mysql.connector
import yaml
import glob
from pathlib import Path
import os

MINECRAFT_DIR = None
MCWEBSTAT_CFG_FILE = "mcwebstat_config.yml"

def init_globals():
    mcwebstat_cfg = read_config()
    global MINECRAFT_DIR
    global PLAYER_DATA_DIR 
    global LOGBLOCK_CFG_FILE
    
    MINECRAFT_DIR = mcwebstat_cfg["MINECRAFT_DIR"]
    PLAYER_DATA_DIR = MINECRAFT_DIR + "/world/playerdata"
    LOGBLOCK_CFG_FILE = MINECRAFT_DIR + "/plugins/LogBlock/config.yml"    

def read_config():
    if not os.path.exists(MCWEBSTAT_CFG_FILE):
        with open(MCWEBSTAT_CFG_FILE, 'w', encoding="utf-8") as f1:
            f1.write("MINECRAFT_DIR: d:/.Minecraft.1.20-paper_world_n2")
        
    with open(MCWEBSTAT_CFG_FILE, "r",encoding='utf-8') as stream:
        config = yaml.safe_load(stream)
    
    return config    
     
    

def open_logblock_db():
    with open(LOGBLOCK_CFG_FILE, "r",encoding='utf-8') as stream:
        try:
            logblock_config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    logblock_db = mysql.connector.connect(
      host=logblock_config["mysql"]["host"],
      port=logblock_config["mysql"]["port"],
      user=logblock_config["mysql"]["user"],
      password=logblock_config["mysql"]["password"],
      database=logblock_config["mysql"]["database"]
    )
    
    return logblock_db
    

# player activity: we count number of days with edits for each of the last 12 "rolling" months
DAYS_IN_MONTH = 30.4375
def get_activity(logblock_db, player_uuid):
    

    cursor = logblock_db.cursor()
    sql="""
    SELECT to_days(NOW())-to_days(`date`) AS edit_date, COUNT(1) AS edit_num 
    FROM `lb-world-blocks` WHERE playerid = (SELECT playerid FROM `lb-players` WHERE UUID='""" + player_uuid + """' ) 
    group BY DATE(`date`)
    ORDER BY DATE desc
    """
    cursor.execute(sql)  
    edit_history = cursor.fetchall()

    activity = [0,0,0,0,0,0,0,0,0,0,0,0]

    for rec in edit_history:
        if rec[1]>0:
            week_id=int(rec[0]//DAYS_IN_MONTH)  #7
            if week_id<len(activity ):
               activity[week_id] += 1

    activity.reverse()
    return activity



# create a diagram  image
# just bars for each month 
def create_diagram(player_uuid, activity):
    im = Image.new("RGB", (157, 32), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    bar_width = im.size[0]//len(activity)
    bar_height_per_unit= int(im.size[1]//DAYS_IN_MONTH)

    fill_color_low = (255, 128, 128, 255)
    fill_color_high = (64, 255, 64, 255)
    outline_color = (0, 0, 0, 255) 

    i = 0
    for day in activity:
        d_norm=day/DAYS_IN_MONTH
        xy = [(i*bar_width,im.size[1]-bar_height_per_unit*day),((i+1)*bar_width, im.size[1] )]
        #print(day, d_norm)
        fill_color = (fill_color_low[0]*(1-d_norm) + fill_color_high[0] *( d_norm),
                          fill_color_low[1]*(1-d_norm) + fill_color_high[1] *( d_norm),
                          fill_color_low[2]*(1-d_norm) + fill_color_high[2] *( d_norm),
                          255)
        fill_color = (int(fill_color[0]),int(fill_color[1]),int(fill_color[2]),fill_color[3] )
        #print(fill_color)
        draw.rectangle(xy, fill_color, outline_color)
        i += 1

    im.save("_build/activity/" + player_uuid +".png", "PNG")
    #im.show()

def main():
    
    init_globals()    
    
     
    playerdata_file_list=glob.glob(PLAYER_DATA_DIR+"/*.dat")
    print(len(playerdata_file_list))
    
    logblock_db = open_logblock_db()

    for playerdata_filename in playerdata_file_list:
        player_uuid = Path(playerdata_filename).stem
        activity = get_activity(logblock_db,player_uuid)
        create_diagram(player_uuid, activity)
        
    logblock_db.close()

if __name__ == "__main__":
    main()
