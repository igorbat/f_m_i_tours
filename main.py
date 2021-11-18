import os

import discord
import random
from secret import TOKEN
from discord.ext import commands
from tasks_5_strong import TASKS_STRONG
from abaka_cls import *


client = discord.Client()
bot = commands.Bot(command_prefix='!')
state_machine = StateMachine()

game_strong_5 = GameAbaka("pro_5", "link", TASKS_STRONG)
state_machine.add_tour("pro_5", game_strong_5)


@bot.command(name='register', help='зарегистрировать команду: школа, класс')
async def register(ctx):
    parts = str(ctx.message.content).strip().split(maxsplit=2)
    if len(parts) < 3:
        await ctx.send("Недостаточно аргументов. Нужно написать школу класс")
    else:
        team_name = state_machine.register_player(ctx.author.id, parts[1], parts[2])
        await ctx.send("Ваша команда: {}".format(team_name))


@bot.command(name='join', help='Присоединиться к игре')
async def join(ctx):
    parts = str(ctx.message.content).strip().split(maxsplit=1)
    if len(parts) < 2:
        await ctx.send("Недостаточно аргументов. Нужно написать название соревнования")
    else:
        ok, msg = state_machine.join_tour(ctx.author.id, parts[1])
        await ctx.send(msg)


# @bot.command(name='leave', help='Отсоединиться от игры. Прогресс сохранится')
# async def leave(ctx):
#     ok, msg = state_machine.leave(ctx.author.id)
#     await ctx.send(msg)


@bot.command(name='solve', help='Отправить решение в виде "solve ТЕМА ЗАДАЧА ОТВЕТ"')
async def solve(ctx):
    parts = str(ctx.message.content).strip().split(maxsplit=4)
    if len(parts) < 4:
        await ctx.send("Недостаточно аргументов. Нужно написать название соревнования")
    else:
        print(parts[1], parts[2], parts[3])
        ok, msg = state_machine.solve(ctx.author.id, parts[1], parts[2], parts[3])
        await ctx.send(msg)


@bot.command(name='tasks', help='Получить ссылку на задания')
async def tasks_link(ctx):
    msg = state_machine.tasks(ctx.author.id)
    await ctx.send(msg)


@bot.command(name='points', help='Сколько у нас очков')
async def points(ctx):
    msg = state_machine.points(ctx.author.id)
    await ctx.send(msg)


@bot.command(name='res_res_res', help='Обновить результаты')
async def res_res_res(ctx):
    state_machine.reload_res()
    await ctx.send("Обновлено")


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
