import math
import random
import string
from typing import List, Dict, Any

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tortoise import Model, fields


class TelegramChannel(Model):
    channel_id = fields.BigIntField(pk=True)
    group_id = fields.BigIntField(null=True)
    post_id = fields.BigIntField(null=True)
    owner_id = fields.BigIntField()
    give_callback_value = fields.TextField()
    channel_callback_value = fields.TextField()
    name = fields.TextField()



    async def add_channel(
        self,
        owner_id: int,
        channel_id: int,
        give_callback_value: str,
        name: str,
        group_id: int = False
    ):

        random_callback_value = ''.join(
            random.choices(
                string.ascii_letters + string.digits, k=60
            )
        )

        await self.create(
            owner_id=owner_id,
            group_id=group_id,
            channel_id=channel_id,
            give_callback_value=give_callback_value,
            channel_callback_value=random_callback_value,
            name=name
        )


    async def add_post_id(self, callback_value: str, post_id: int):
        await self.filter(give_callback_value=callback_value).update(post_id=post_id)


    async def delete_channel(self, channel_callback_value: str = False, give_callback_value: str = False):

        if channel_callback_value:
            await self.filter(channel_callback_value=channel_callback_value).delete()

        else:
            await self.filter(give_callback_value=give_callback_value).all().delete()


    async def exists_channel(self, channel_id: int) -> bool:
        return await self.filter(channel_id=channel_id).exists()


    async def get_channel_id(self, channel_callback_value: str) -> list[dict[str, Any]] | dict[str, Any]:
        return await self.filter(channel_callback_value=channel_callback_value).all().values('channel_id')


    async def get_channel_data(
        self,
        channel_callback_value: str = False,
        owner_id: int = False,
    ):
        if channel_callback_value:
            return await self.filter(channel_callback_value=channel_callback_value).all().values(
                'channel_id',
                'name',
                'post_id',
                'group_id'
            )

        else:
            return await self.filter(owner_id=owner_id).all().values(
                'channel_id',
                'name',
                'post_id',
                'group_id'
            )


    async def get_keyboard(self, owner_id: int) -> InlineKeyboardMarkup | bool:
        channels_data = await self.filter(owner_id=owner_id).all().values('name', 'channel_callback_value')


        if channels_data:
            markup = InlineKeyboardMarkup()

            for channel in channels_data:
                markup.add(InlineKeyboardButton(
                    channel['name'],
                    callback_data=channel['channel_callback_value']
                ))


            return markup

        else:
            return False
