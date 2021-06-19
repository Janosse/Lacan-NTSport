from discord.ext import commands
from packages.utils import Embed
from mongoclient import DBClient
import discord
from nitrotype import NT_to_discord
class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener('on_member_join')
    async def event(self, member):
        dbclient = DBClient()
        collection = dbclient.db.servers
        server = await dbclient.get_array(collection, {'serverID': member.guild.id})
        try:
            async for x in server:
                data = x
                break
        except:
            return
        print(data)
        channel_id = data['channel_id']
        channel = discord.utils.get(self.client.get_all_channels(), id=channel_id)
        message = data['message']
        racer = await NT_to_discord(member.id)
        racer = racer[1]
        try:
            username = racer.username
            speed = racer.speed_role
            accuracy = racer.accuracy_role
            races = racer.race_role
        except Exception as e:
            print(e)
        message = message.replace('{{user.mention}}', member.mention)
        message = message.replace('{{user.id}}', str(member.id))
        message = message.replace('{{user.racer.username}}', username)
        message = message.replace('{{user.racer.speed}}', speed)
        message = message.replace('{{user.racer.accuracy}}', accuracy)
        message = message.replace('{{user.racer.races}}', races)
        await channel.send(message)
def setup(client):
    client.add_cog(Events(client))