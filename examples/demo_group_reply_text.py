# -*- coding: utf-8 -*-
import asyncio
import os

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message
from maint import search_main

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")
        asyncio.create_task(self.keep_alive())

    async def on_group_at_message_create(self, message: GroupMessage):
        results = await search_main(message.content)
        messageResult = await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content=f'查询结果：\n{results}',)
        _log.info(messageResult)

    async def keep_alive(self):
        while True:
            await asyncio.sleep(30)  # 每30秒发送一次心跳包
            _log.info("Sending heartbeat")

    async def start_client(self, appid, secret):
        while True:
            try:
                await self.start(appid=appid, secret=secret)
            except Exception as e:
                _log.error(f"连接失败: {e}")
                await asyncio.sleep(5)  # 等待5秒后重试
            _log.info("重连中...")


async def nmain():
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    await client.start_client(appid=test_config["appid"], secret=test_config["secret"])


# asyncio.run(nmain())
