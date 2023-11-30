from discord.ui.item import Item
from database import DataBase
import sys
import discord
import asyncio
import time

sys.path.append("../utils")

# ? Views


class UserSelectView(discord.ui.View):
    def __init__(self, *items: Item, timeout: float | None = None, disable_on_timeout: bool = False):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.selected_user = None

    @discord.ui.user_select(placeholder="Select User")
    async def user_select_callback(self, select, interaction):
        selected_user_id = select.values[0]
        self.selected_user = selected_user_id
        await interaction.response.send_message(f"You selected user: {self.selected_user.display_name}", delete_after=0, ephemeral=True)
        self.stop()


class TextInputView(discord.ui.Modal):
    def __init__(self, max_lenght=2, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.input = None
        self.max_lenght = max_lenght

        self.add_item(discord.ui.InputText(
            label="Enter Value", max_length=self.max_lenght))

    async def callback(self, interaction: discord.Interaction):
        self.input = self.children[0].value
        await interaction.response.send_message(f"Done", delete_after=0, ephemeral=True)


class TempRoomControlView(discord.ui.View):
    def __init__(self, *items: Item, timeout: None = None, disable_on_timeout: bool = False):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.db_module = DataBase()
        self.db, self.cr = self.db_module.init_db()
        self.last_name_edit = None

    async def get_user_voice(self, interaction):
        user = interaction.user
        if user.voice and user.voice.channel:
            voice_channel = user.voice.channel
            temp_room = self.db_module.get_temp_room(voice_channel.id)
            if str(user.id) != str(temp_room[2]):
                await interaction.response.send_message("You are not owner.", ephemeral=True, delete_after=1)
            else:
                return voice_channel
        else:
            await interaction.response.send_message("You are not in a voice channel.", ephemeral=True, delete_after=1)
        return False

    @discord.ui.button(label="Rename", emoji="✍️", row=0, style=discord.ButtonStyle.secondary)
    async def rename_button_callback(self, button, interaction):
        if self.last_name_edit is None or (time.time()-self.last_name_edit) > 300:
            voice_channel = await self.get_user_voice(interaction=interaction)
            if voice_channel:
                modal = TextInputView(
                    title="Change temp room name", max_lenght=100)
                await interaction.response.send_modal(modal)
                await modal.wait()
                new_name = modal.input
                if new_name:
                    await voice_channel.edit(name=new_name)
                    self.last_name_edit = time.time()
        else:
            await interaction.response.send_message(f"Please wait {300-(time.time()-self.last_name_edit):.2f}/S before change name", ephemeral=True, delete_after=5)

    @discord.ui.button(label="Set Bitrate", emoji="🔊", row=0, style=discord.ButtonStyle.secondary)
    async def set_bitrate_button_callback(self, button, interaction):
        voice_channel = await self.get_user_voice(interaction=interaction)
        if voice_channel:
            modal = TextInputView(title="Change temp room name")
            await interaction.response.send_modal(modal)
            await modal.wait()
            input = modal.input
            try:
                if 96 < int(input) < 8:
                    raise ValueError
                input = int(input)*1000
                if input:
                    await voice_channel.edit(bitrate=input)
                    await interaction.followup.send(f"Bitrate changed to {input/1000}/kbps", ephemeral=True, delete_after=5)
            except:
                await interaction.followup.send("Please enter a valid integer in this range 96-8", ephemeral=True, delete_after=5)

    @discord.ui.button(label="Set Limit", emoji="🚧", row=0, style=discord.ButtonStyle.secondary)
    async def set_limit_button_callback(self, button, interaction):
        voice_channel = await self.get_user_voice(interaction=interaction)
        if voice_channel:
            modal = TextInputView(title="Change temp room name")
            await interaction.response.send_modal(modal)
            await modal.wait()
            input = modal.input
            try:
                if 99 < int(input) < 0:
                    raise ValueError
                if input:
                    await voice_channel.edit(user_limit=input)
                    await interaction.followup.send(f"User limit changed to {input}", ephemeral=True, delete_after=5)
            except:
                await interaction.followup.send("Please enter a valid integer in this range 99-0", ephemeral=True, delete_after=5)

    @discord.ui.button(label="Hide", emoji="🫥", row=1, style=discord.ButtonStyle.secondary)
    async def hide_button_callback(self, button, interaction):
        voice_channel = await self.get_user_voice(interaction=interaction)
        if voice_channel:
            is_hidden = voice_channel.overwrites_for(
                interaction.guild.default_role).view_channel
            if is_hidden:
                await voice_channel.set_permissions(
                    interaction.guild.default_role, view_channel=False
                )
                button.label = "Show"
                button.emoji = "☀️"
            else:
                button.label = "Hide"
                button.emoji = "🫥"
                await voice_channel.set_permissions(interaction.guild.default_role, view_channel=True)
            await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Lock", emoji="🔒", row=1, style=discord.ButtonStyle.secondary)
    async def lock_button_callback_2(self, button, interaction):
        voice_channel = await self.get_user_voice(interaction=interaction)
        if voice_channel:
            is_loced = voice_channel.overwrites_for(
                interaction.guild.default_role).connect
            if is_loced:
                await voice_channel.set_permissions(
                    interaction.guild.default_role, connect=False
                )
                button.label = "Unlock"
                button.emoji = "🔓"
            else:
                button.label = "Lock"
                button.emoji = "🔒"
                await voice_channel.set_permissions(interaction.guild.default_role, connect=True)
            await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Kick", emoji="🦵", row=1, style=discord.ButtonStyle.secondary)
    async def kick_button_callback(self, button, interaction):
        voice_channel = await self.get_user_voice(interaction=interaction)
        if voice_channel:
            view = UserSelectView()
            await interaction.response.send_message(content="Please select users to kick", ephemeral=True, view=view)
            await view.wait()
            await interaction.delete_original_response()
            user = view.selected_user
            if user.voice:
                if (user.voice.channel == voice_channel and not user.guild_permissions.administrator):
                    await user.move_to(None)
                    await interaction.followup.send(f"{user.mention} Kicked", ephemeral=True, delete_after=3)
                else:
                    await interaction.followup.send(f"You can't kick {user.mention}", ephemeral=True, delete_after=3)
            else:
                await interaction.followup.send(f"You can't kick {user.mention}", ephemeral=True, delete_after=3)

    @discord.ui.button(label="Delete", emoji="❌", row=1, style=discord.ButtonStyle.secondary)
    async def delete_button_callback(self, button, interaction):
        temp_room = self.db_module.get_temp_room_2(
            owner_id=interaction.user.id, room_id=interaction.channel.id)
        voice_channel = interaction.guild.get_channel(temp_room[1])
        if voice_channel:
            self.db_module.delete_temp_room(room_id=temp_room[1])
            await voice_channel.delete()

    @discord.ui.button(label="Claim", emoji="🏆", row=2, style=discord.ButtonStyle.secondary)
    async def claim_button_callback(self, button, interaction):
        user = interaction.user
        if user.voice and user.voice.channel:
            voice_channel = user.voice.channel
            temp_room = self.db_module.get_temp_room(voice_channel.id)
            members = [q.id for q in voice_channel.members]
            owner_id = temp_room[2]
            if int(owner_id) not in members:
                self.db_module.update_temp_room_owner(
                    voice_channel.id, user.id)
                await interaction.response.send_message(
                    f"{user.mention} Now you are owner, you can control this room", delete_after=10
                )
            else:
                await interaction.response.send_message(
                    f"You can't claim room when owner is connected", ephemeral=True, delete_after=3
                )
        else:
            await interaction.response.send_message("You are not in a voice channel.", ephemeral=True, delete_after=1)

    @discord.ui.button(label="Transfer", emoji="💸", row=2, style=discord.ButtonStyle.secondary)
    async def transfer_button_callback(self, button, interaction):
        voice_channel = await self.get_user_voice(interaction=interaction)
        if voice_channel:
            view = UserSelectView()
            await interaction.response.send_message(content="Please select users to give an owner", ephemeral=True, view=view)
            await view.wait()
            await interaction.delete_original_response()
            user = view.selected_user
            if user.voice:
                if (user.voice.channel == voice_channel):
                    self.db_module.update_temp_room_owner(
                        voice_channel.id, user.id)
                    await interaction.followup.send(
                        f"{user.mention} Now you are owner, you can control this room", delete_after=10
                    )
            else:
                await interaction.followup.send(f"{user.mention} can't be room owner", ephemeral=True, delete_after=3)

    @discord.ui.button(label="Block", emoji="🚫", row=2, style=discord.ButtonStyle.secondary)
    async def block_button_callback(self, button, interaction):
        voice_channel = await self.get_user_voice(interaction=interaction)
        if voice_channel:
            view = UserSelectView()
            await interaction.response.send_message(content="Please select users to give an owner", ephemeral=True, view=view)
            await view.wait()
            await interaction.delete_original_response()
            user = view.selected_user
            await voice_channel.set_permissions(user, connect=False)
            await interaction.followup.send(
                f"{user.mention} has been blocked from the channel", ephemeral=True, delete_after=5
            )

    @discord.ui.button(label="Unblock", emoji="✅", row=2, style=discord.ButtonStyle.secondary)
    async def unblock_button_callback(self, button, interaction):
        voice_channel = await self.get_user_voice(interaction=interaction)
        if voice_channel:
            view = UserSelectView()
            await interaction.response.send_message(content="Please select users to give an owner", ephemeral=True, view=view)
            await view.wait()
            await interaction.delete_original_response()
            user = view.selected_user
            await voice_channel.set_permissions(user, connect=True)
            await interaction.followup.send(
                f"{user.mention} has been blocked from the channel", ephemeral=True, delete_after=5
            )


# ? Cogs
class TempVoice(discord.Cog):
    def __init__(self, client):
        self.client = client
        self.db_module = DataBase()
        self.db, self.cr = self.db_module.init_db()

    @discord.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        async def create_channel(category, prefix):
            if isinstance(category, discord.CategoryChannel):
                rooms = [q.name for q in category.voice_channels]
            overwrites = {
                member: discord.PermissionOverwrite(connect=True, view_channel=True),
                member.guild.default_role: discord.PermissionOverwrite(
                    connect=True, view_channel=True
                ),
            }
            channel_name_num = (
                1
                if rooms[-1] != prefix and not (rooms[-1].split()[-1]).isnumeric()
                else int(
                    rooms[-1].split(" ")[-1]
                    if rooms[-1].split(" ")[-1] != prefix
                    else 0
                )
                + 1
            )
            new_channel = await after.channel.category.create_voice_channel(
                name=f"{prefix} {channel_name_num}",
                overwrites=overwrites,
            )
            self.db_module.create_temp_room(
                server_id=member.guild.id, room_id=new_channel.id, owner_id=member.id
            )
            return new_channel
        server_id = member.guild.id
        temp_voice_settings_data = [
            q
            for q in self.cr.execute(
                f'SELECT * FROM temp_voice_config WHERE ServerId="{server_id}"'
            )
        ]
        # ? Create part
        if after.channel:
            if after.channel.id in [q[1] for q in temp_voice_settings_data]:
                for c in temp_voice_settings_data:
                    if c[1] == after.channel.id:
                        room = c
                        break
                category = member.guild.get_channel(after.channel.id).category
                new_channel = await create_channel(category=category, prefix=room[3])
                await member.move_to(new_channel)
                control_view = TempRoomControlView()
                await new_channel.send(f"{member.mention}", view=control_view)
        # ? Delete part
        if before.channel:
            temp_voice = [
                q[0]
                for q in self.cr.execute(
                    f'SELECT RoomId FROM temp_room WHERE ServerID="{server_id}"'
                )
            ]
            if before.channel.id in temp_voice and len(before.channel.members) == 0:
                self.db_module.delete_temp_room(room_id=before.channel.id)
                await before.channel.delete()

#! Whaiting api to setup
# class SetupTemp(discord.Cog):
#     def __init__(self, client):
#         self.client = client

#     @discord.guild_only()
#     @discord.slash_command(description="Setup Temp Voice Room")
#     async def setup_voice(self, ctx, channel_name, room_prefix, category: discord.CategoryChannel):
#         if ctx.author.guild_permissions.administrator:
#             categories = ctx.guild.categories
#             if category.name not in [q.name for q in categories]:
#                 await ctx.respond("Please Enter Valid Category", ephemeral=True)
#                 return
#             else:
#                 for c in categories:
#                     if c.name==category.name:
#                         category.name = c
#                         break
#             vc = await c.create_voice_channel(name=channel_name)
#             DataBase().create_temproom_config(room_id=vc.id, room_name=vc.name, server_id=ctx.guild.id, room_prefix=room_prefix)
#             await ctx.respond(f"Channel \"{channel_name}\" created", ephemeral=True)
#         else:
#             await ctx.respond("You don't have permission to use this command.", ephemeral=True)


def setup(client):
    client.add_cog(TempVoice(client))
    # client.add_cog(SetupTemp(client))
