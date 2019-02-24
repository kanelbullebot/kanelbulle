import yaml

async def fetchguildconfig(guild_id: int):
    try:
        with open(f"configs/{guild_id}.yml") as gconfig:
            guildsettings = yaml.safe_load(gconfig)
    except:
        print(f"{guild_id} tried to execute a command without a valid config.")
        return
    return(guildsettings)
