import discord
from discord.ext import commands
from core.memory import MemoryManager
from config.settings import OWNER_ID


class CommandHandler(commands.Cog):
    """Обработчик команд бота"""
    
    def __init__(self, bot):
        self.bot = bot
        self.memory = MemoryManager()
    
    @commands.command(name="забудь", aliases=["forget"])
    async def forget_me(self, ctx: commands.Context):
        """Стирает память бота о пользователе"""
        user_id = ctx.author.id
        username = ctx.author.display_name
        
        if self.memory.delete_user_memory(user_id):
            responses = [
                f"*отворачивается* Ч-что? {username}? Не помню никакого {username}... *краснеет*",
                f"Хм... а кто ты вообще такой, {username}? *делает вид, что не помнит*",
                f"*пожимает плечами* Память стёрта. Довольн? Н-не то чтобы мне было важно... дурачок.",
                f"Ладно-ладно, забыла уже! *надувает щёки* Теперь ты для меня никто!"
            ]
            await ctx.send(responses[hash(username) % len(responses)])
        else:
            responses = [
                f"Я и так тебя не помню, {username}! *фыркает*",
                "А чего забывать-то? Ты мне и не запомнился особо... *отводит взгляд*",
                f"Хм? {username}? Первый раз вижу. *хмурится*"
            ]
            await ctx.send(responses[hash(username) % len(responses)])
    
    @commands.command(name="память", aliases=["memory"])
    async def show_memory(self, ctx: commands.Context):
        """Показывает что Акира помнит о пользователе"""
        user_id = ctx.author.id
        username = ctx.author.display_name
        memory = self.memory.get_user_memory(user_id)
        
        if memory:
            # Разбиваем на части если слишком длинное
            if len(memory) > 1800:
                memory = memory[-1800:] + "\n...(показаны последние записи)"
            
            embed = discord.Embed(
                title=f"💭 Что я помню о {username}",
                description=f"*смущённо отводит взгляд*\n\nН-ну ладно, вот что я... случайно запомнила:\n\n```{memory}```",
                color=discord.Color.pink()
            )
            embed.set_footer(text="Н-не подумай, что я специально запоминала!")
            await ctx.send(embed=embed)
        else:
            responses = [
                f"*пожимает плечами* Ничего о тебе не помню, {username}. Мы вообще знакомы?",
                "Хм... память пуста. *смотрит с любопытством* Может расскажешь о себе?",
                f"А кто ты такой, {username}? *наклоняет голову* Не припомню тебя...",
                "*зевает* Ты слишком скучный, чтобы тебя запоминать~ *ухмыляется*"
            ]
            await ctx.send(responses[hash(username) % len(responses)])
    
    @commands.command(name="сброс", aliases=["reset"])
    async def reset_channel(self, ctx: commands.Context):
        """Очищает историю канала (только для владельца)"""
        if ctx.author.id != OWNER_ID:
            responses = [
                "*бьёт по руке* Эй! Это не для тебя!",
                "Ты кто такой вообще? Только хозяин может это делать! *фыркает*",
                "*скрещивает руки* Нет уж, это только мой владелец может.",
                "Ха! Думал прокатит? *смеётся* Иди отсюда~"
            ]
            await ctx.send(responses[hash(ctx.author.name) % len(responses)])
            return
        
        channel_id = ctx.channel.id
        if self.memory.clear_channel_history(channel_id):
            await ctx.send("*щёлкает пальцами* История канала стёрта, хозяин. Начнём всё с чистого листа? *улыбается*")
        else:
            await ctx.send("История канала и так пуста, хозяин~ *пожимает плечами*")


async def setup(bot):
    """Загружает Cog с командами"""
    await bot.add_cog(CommandHandler(bot))
