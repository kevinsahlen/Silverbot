import discord

class KeyEmbedder():
    def __init__(self, list:list, description_input, start_time):
        self.player_role_list = list
        self.description = description_input
        if start_time != None:
            self.description += f'\n{start_time}'

    def get_embed(self, new_player_role_list = None, is_timed_out = False):
        embed = discord.Embed(title='Key Group', description=self.description, color=0x00ff00)
        if new_player_role_list != None:
            self.player_role_list = new_player_role_list
        playerstr = ''
        rolestr = ''
        for player_role in self.player_role_list:
            playerstr += f'{player_role[0].display_name}\n'
            if player_role[1]:
                rolestr += '<:dps:1257129006462144644>'
            if player_role[2]:
                rolestr += '<:healer:1257129028276719718>'
            if player_role[3]:
                rolestr += '<:tank:1257129045993459775>'
            if not player_role[1] and not player_role[2] and not player_role[3]:
                rolestr += 'No role selected'
            rolestr += '\n'
        embed.add_field(name='Player', value=playerstr, inline=True)
        embed.add_field(name='Role', value=rolestr, inline=True)
        if is_timed_out:
            embed.add_field(name='', value='This group is closed', inline=False)
        return embed