import disnake
from disnake.ext import commands
from disnake import TextInputStyle


import main


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class Modal(disnake.ui.Modal):

        @property.setter
        def author(self, author):
            self.__author = author

        @property
        def author(self):
            return self.__author

        # emae

        def __init__(self):
            self.__author = None
            self.components = [
                disnake.ui.TextInput(
                    label="Сколько Вам лет?",
                    placeholder="Вы уже дедушка или бабушка?",
                    custom_id="Возраст",
                    style=TextInputStyle.short,
                    max_length=3,
                ),
                disnake.ui.TextInput(
                    label="Что Вы планируете делать на этом сервере?",
                    placeholder="Ваши идеи..",
                    custom_id="Идеи",
                    style=TextInputStyle.paragraph,
                ),
                disnake.ui.TextInput(
                    label="Откуда Вы узнали о нас?",
                    placeholder="Платформа",
                    custom_id="Платформа",
                    style=TextInputStyle.short,
                    max_length=50,
                ),
                disnake.ui.TextInput(
                    label="Как часто Вы будете играть на сервере?",
                    placeholder="Я буду играть..",
                    custom_id="Время",
                    style=TextInputStyle.short,
                    max_length=50,
                ),
                disnake.ui.TextInput(
                    label="Какой Ваш ник в Minecraft?",
                    placeholder="Ник Minecraft",
                    custom_id="Ник",
                    style=TextInputStyle.short,
                    max_length=100,
                ),
            ]
            super().__init__(title="Заявка", components=self.components)

        async def callback(self, inter: disnake.ModalInteraction):

            embed = disnake.Embed(title="Заявка", color=disnake.Color.green())
            for key, value in inter.text_values.items():
                embed.add_field(
                    name=key.capitalize(),
                    value=value[:1024],
                    inline=False,
                )

            components = [
                disnake.ui.Button(
                    label="Принять",
                    style=disnake.ButtonStyle.success,
                    custom_id="confirm",
                ),
                disnake.ui.Button(
                    label="Отклонить",
                    style=disnake.ButtonStyle.danger,
                    custom_id="decline",
                ),
            ]
            await inter.response.send_message(embed=disnake.Embed(
                title="Успешно!",
                description="Вы успешно подали заявку, ожидайте.",
                color=disnake.Color.green(),
            ), delete_after=15)  # Закрывает модальное окно, костыль

            guild = inter.guild
            channel = await guild.create_text_channel("ticket-" + str(inter.author.name))

            self.setAuthor(self, inter.author.id)

            embChannel = main.getChannel(channel)
            await embChannel.send(embed=embed, components=components)

    @commands.slash_command()
    async def ticket(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="Заявка",
            description="Нажмите на кнопку, чтобы открыть заявку по регистрации",
            color=disnake.Color.green(),
        )
        components = [
            disnake.ui.Button(label="Открыть заявку", style=disnake.ButtonStyle.success, custom_id="ok"),
        ]
        await inter.response.send_message(embed=embed, components=components)

    @commands.Cog.listener("on_button_click")
    async def help_listener(self, inter):
        if inter.component.custom_id not in ["ok", "decline", "confirm"]:
            return

        if inter.component.custom_id == "ok":
            modal = self.Modal()
            await inter.response.send_modal(modal=modal)
        elif inter.component.custom_id == "decline":
            author = self.Modal.getAuthor(self.Modal())
            author.send("Ваша заявка отклонена!")




def setup(bot):
    bot.add_cog(Tickets(bot))
