import discord


class KeyEmbedder():
    def __init__(self, list:list, desc, start_time):
        self.list = list
        self.desc = desc
        self.starttime = start_time

    def get_embed(self, list = None, isTimedOut = False):
        description = self.desc
        if self.starttime != None:
            description += f'\n{self.starttime}'
        embed = discord.Embed(title='Key Group', description=description, color=0x00ff00)
        
        if list != None:
            self.list = list
        playerstr = ''
        rolestr = ''
        for item in self.list:
            playerstr += f'{item[0].display_name}\n'
            if item[1]:
                rolestr += '<:dps:1257129006462144644>'
            if item[2]:
                rolestr += '<:healer:1257129028276719718>'
            if item[3]:
                rolestr += '<:tank:1257129045993459775>'
            if not item[1] and not item[2] and not item[3]:
                rolestr += 'No role selected'
            rolestr += '\n'

        embed.add_field(name='Player', value=playerstr, inline=True)
        embed.add_field(name='Role', value=rolestr, inline=True)
        if isTimedOut:
            embed.add_field(name='', value='This group is closed', inline=False)

        return embed