import math
import random
import string
from datetime import date

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tortoise import Model, fields


class GiveAway(Model):
    owner_id = fields.BigIntField()
    run_status = fields.BooleanField()
    type = fields.TextField()
    name = fields.TextField()
    callback_value = fields.TextField(pk=True)
    text = fields.TextField()
    photo_id = fields.TextField(null=True)
    video_id = fields.TextField(null=True)
    over_date = fields.DatetimeField()
    captcha = fields.BooleanField()
    winners_count = fields.IntField()


    async def create_give(
        self,
        owner_id: int,
        name: str,
        type_of_give: str,
        text: str,
        photo_id: str,
        video_id: str,
        over_date: date,
        captcha: bool,
        winners_count: int
    ):
        random_callback_value = ''.join(
            random.choices(
                string.ascii_letters + string.digits, k=40
            )
        )

        await self.create(
            owner_id=owner_id,
            run_status=False,
            name=name,
            callback_value=random_callback_value,
            type=type_of_give,
            text=text,
            photo_id=photo_id,
            video_id=video_id,
            over_date=over_date,
            captcha=captcha,
            winners_count=winners_count
        )


    async def change_give_over_date(self, callback_value: str, over_date: date):
        await self.filter(callback_value=callback_value).update(over_date=over_date)


    async def delete_give(
        self,
        callback_value: str
    ):
        await self.filter(callback_value=callback_value).delete()


    async def update_give_status(self, callback_value: str, status: bool):
        await self.filter(callback_value=callback_value).update(run_status=status)


    async def get_owner_by_callback_value(self, give_callback_value: str):
        data = await self.filter(callback_value=give_callback_value).all().values('owner_id')
        return data[0]["owner_id"]


    async def exists_give_name(
        self,
        user_id: int,
        name: str
    ) -> bool:
        return await self.filter(owner_id=user_id, name=name).exists()


    async def get_give_data(
        self,
        user_id: int,
        callback_value: str
    ) -> list[dict]:

        data = await self.filter(owner_id=user_id, callback_value=callback_value).all().values(
            'name',
            'type',
            'text',
            'photo_id',
            'video_id',
            'over_date',
            'captcha',
            'winners_count'
        )
        return data


    async def get_give_data_for_owner(self, callback_value: str) -> list[dict]:
        data = await self.filter(callback_value=callback_value).all().values(
            'name',
            'type',
            'text',
            'photo_id',
            'video_id',
            'over_date',
            'captcha',
            'winners_count'
        )
        return data


    async def get_keyboard_of_created_gives(
        self,
        user_id: int,
        page: int = 1,
        page_size: int = 10
    ) -> InlineKeyboardMarkup | bool:

        gives_data = await self.filter(
            owner_id=user_id,
            run_status=False
        ).all().values(
            'name',
            'callback_value'
        )

        if gives_data:
            markup = InlineKeyboardMarkup()

            start_index = (page - 1) * page_size
            end_index = start_index + page_size
            gives_data_page = gives_data[start_index:end_index]

            for give in gives_data_page:
                markup.add(InlineKeyboardButton(
                    give['name'],
                    callback_data=give['callback_value']
                ))


            num_pages = math.ceil(len(gives_data) / page_size)
            if num_pages > 1:
                prev_page = page - 1 if page > 1 else 1
                next_page = page + 1 if page < num_pages else num_pages
                markup.row(
                    InlineKeyboardButton("⬅️", callback_data=f"page_of_created_gives_prev:{prev_page}"),
                    InlineKeyboardButton(f"Страница {page}/{num_pages}", callback_data="count_pages_in_items"),
                    InlineKeyboardButton("➡️", callback_data=f"page_of_created_gives_next:{next_page}")
                    )

            return markup

        else:
            return False




    async def get_keyboard_of_active_gives(
        self,
        user_id: int,
        page: int = 1,
        page_size: int = 10
    ) -> InlineKeyboardMarkup | bool:

        gives_data = await self.filter(
            owner_id=user_id,
            run_status=True
        ).all().values(
            'name',
            'callback_value'
        )

        if gives_data:
            markup = InlineKeyboardMarkup()

            for give in gives_data:
                markup.add(InlineKeyboardButton(
                    give['name'],
                    callback_data=give['callback_value']
                ))


            return markup

        else:
            return False



    async def get_keyboard_for_owner(
            self,
            page: int = 1,
            page_size: int = 10
    ) -> InlineKeyboardMarkup | bool:

        gives_data = await self.filter(
            run_status=True
        ).all().values(
            'name',
            'callback_value'
        )

        if gives_data:
            markup = InlineKeyboardMarkup()

            for give in gives_data:
                markup.add(InlineKeyboardButton(
                    give['name'],
                    callback_data=give['callback_value']
                ))

            return markup

        else:
            return False

