# -*- coding: utf8 -*-
import asyncio
import logging
from random import choice

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import RetryAfter, BadRequest

import bot_config
from base_parser import BaseParser
from generate_array import generate

# from sql import ReadData, WriteData

__author__ = '3eca'
__github__ = 'https://github.com/3eca'

bot = Bot(token=bot_config.TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

bp = BaseParser()


# rd = ReadData()
# wd = WriteData()


@dp.message_handler(commands='girls', commands_prefix='/')
async def media_group(message: types.Message):
    await bot.send_message(message.chat.id, 'Подготовка данных...',
                           reply_to_message_id=message.message_id)
    random_girl = choice(bp.all_urls_content)
    for images in generate(bp.upload_image_2(random_girl)):
        media = types.MediaGroup()
        for image in images:
            media.attach_photo(image)
        try:
            await bot.send_media_group(message.chat.id, media=media,
                                       reply_to_message_id=message.message_id)
            del media
        except RetryAfter as why:
            await asyncio.sleep(why.timeout)
        except BadRequest:
            await asyncio.sleep(10)


@dp.message_handler(commands='girl', commands_prefix='/')
async def photo(message: types.Message):
    await bot.send_message(message.chat.id, 'Подготовка данных...',
                           reply_to_message_id=message.message_id)
    random_girl = choice(bp.all_urls_content)
    for images in generate(bp.upload_image_2(random_girl)):
        for image in images:
            try:
                await bot.send_photo(message.chat.id, photo=image,
                                     reply_to_message_id=message.message_id)
            except RetryAfter as why:
                await asyncio.sleep(why.timeout)
            except BadRequest:
                await asyncio.sleep(10)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
