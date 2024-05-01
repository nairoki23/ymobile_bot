import discord
from discord import app_commands
import ymobile
import datetime
import json

config_file = open("./config.json")
config = json.load(config_file)
config_file.close()

PhoneNumber=config["PhoneNumber"]
password=config["PassWord"]
discord_token = config["discord_token"]

intents = discord.Intents.default()#適当に。
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def monthFormat(mon):
    if mon>=10:
        return str(mon)
    else:
        return "0"+str(mon)



@client.event
async def on_ready():
    print("lunched")
    await tree.sync()#スラッシュコマンドを同期

@tree.command(name="easy-check",description="かんたん確認(データ量残量)")
async def easy_check(interaction: discord.Interaction):
    await interaction.response.defer()
    info=ymobile.get_info(PhoneNumber,password)
    dt_now = datetime.datetime.now()
    total=info["kurikoshi"]+info["kihon"]+info["yuryou"]
    res="お客さまのご利用状況をご案内します💡\n\n"
    res=res+"データ量残量："+str(total-info["used"])+"GB/"+str(total)+"GB\n"
    res=res+"リセット日："+monthFormat(dt_now.month+1)+"/"+"01\n\n"
    res=res+"詳細はこちら😉\nhttps://stn.mb.softbank.jp/34402"
    await interaction.followup.send(res)


client.run(discord_token)
