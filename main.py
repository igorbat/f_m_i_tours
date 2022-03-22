import discord
from secret import TOKEN
from discord.ext import commands
from abaka.data.tasks_5_strong import *
from abaka.data.tasks_5_weak import *
from abaka.data.tasks_8_strong import *
from abaka.data.tasks_8_weak import *

from abaka.abaka_cls import *


client = discord.Client()
bot = commands.Bot(command_prefix='!')
state_machine = StateMachine()


game_test = \
    GameAbaka("test",
              "https://docs.google.com/document/d/1VlLj1B6JeLmsBeVtijxZNSb5KWbF4nHI-uD7-zvZnwQ/edit?usp=sharing",
              TASKS_TEST)
state_machine.add_tour("test", game_test)

game_strong_5 = \
    GameAbaka("pro_5",
              "https://drive.google.com/file/d/1Aw00bK3RMkRLVxQPVVUnTMzpNe3wihFV/view?usp=sharing",
              TASKS_5_STRONG)
state_machine.add_tour("pro_5", game_strong_5)

game_weak_5 = \
    GameAbaka("novice_5",
              "https://drive.google.com/file/d/1eXZjFVYTt9Iu9EQbZVulwQ4mYaHzUgeR/view?usp=sharing",
              TASKS_5_WEAK)
state_machine.add_tour("novice_5", game_weak_5)


game_strong_8 = \
    GameAbaka("pro_8",
              "https://drive.google.com/file/d/1Mjlc2-P1wdZw6WLuH6KPEML1CIz_Mrfb/view?usp=sharing",
              TASKS_8_STRONG)
state_machine.add_tour("pro_8", game_strong_8)


game_weak_8 = \
    GameAbaka("novice_8",
              "https://drive.google.com/file/d/1a9L0kT0yJs9VTFjIgxTaZO7ELQdOYcin/view?usp=sharing",
              TASKS_8_WEAK)
state_machine.add_tour("novice_8", game_weak_8)


@bot.command(name='register', help='зарегистрировать команду: школа, класс или целиком название')
async def register(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = str(ctx.message.content).strip().split(maxsplit=1)
    if len(parts) < 2:
        msg = "Недостаточно аргументов. Нужно написать школу класс"
        print(msg)
        await ctx.send(msg)
    else:
        team_name = state_machine.register_player(ctx.author.id, parts[1])
        msg = "Ваша команда: {}".format(team_name)
        print(msg)
        await ctx.send(msg)


@bot.command(name='join', help='Присоединиться к игре')
async def join(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = str(ctx.message.content).strip().split(maxsplit=1)
    if len(parts) < 2:
        msg = "Недостаточно аргументов. Нужно написать название соревнования"
        print(msg)
        await ctx.send()
    else:
        ok, msg = state_machine.join_tour(ctx.author.id, parts[1])
        print(msg)
        await ctx.send(msg)


# @bot.command(name='leave', help='Отсоединиться от игры. Прогресс сохранится')
# async def leave(ctx):
#     ok, msg = state_machine.leave(ctx.author.id)
#     await ctx.send(msg)


@bot.command(name='solve', help='Отправить решение в виде "solve ТЕМА ЗАДАЧА ОТВЕТ"')
async def solve(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = str(ctx.message.content).strip().split(maxsplit=4)
    if len(parts) < 4:
        msg = "Недостаточно аргументов. Нужно написать !solve ТЕМА ЗАДАЧА ОТВЕТ"
        print(msg)
        await ctx.send(msg)
    else:
        ok, msg = state_machine.solve(ctx.author.id, parts[1], parts[2], parts[3])
        print(msg)
        await ctx.send(msg)


@bot.command(name='tasks', help='Получить ссылку на задания')
async def tasks_link(ctx):
    # print(ctx.author.id, ctx.author.name, ctx.message.content)
    ok, msg = state_machine.tasks(ctx.author.id)
    # print(msg)
    await ctx.send(msg)


@bot.command(name='sent_task', help='Какие задания вы отправили')
async def sent_task(ctx):
    # print(ctx.author.id, ctx.author.name, ctx.message.content)
    ok, msg = state_machine.sent_task(ctx.author.id)
    # print(msg)
    await ctx.send(msg)


@bot.command(name='points', help='Сколько у нас очков')
async def points(ctx):
    # print(ctx.author.id, ctx.author.name, ctx.message.content)
    ok, msg = state_machine.points(ctx.author.id)
    # print(msg)
    await ctx.send(msg)


@bot.command(name='res_res_res', help='Обновить результаты')
async def res_res_res(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    state_machine.reload_res()
    msg = "Обновлено"
    print(msg)
    await ctx.send(msg)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
