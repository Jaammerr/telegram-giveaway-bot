from tortoise import Model, fields



class TemporaryUsers(Model):
    giveaway_callback_value = fields.TextField(pk=True)
    users = fields.JSONField(null=True)



    async def add_user(
        self,
        callback_value: str,
        new_member_id: str,
        new_member_username: str
    ):

        old_data = await self.filter(
            giveaway_callback_value=callback_value
        ).all().values('users')

        members = []
        try:
            members = old_data[0]['users']

            for member in members:
                if new_member_id == member['user_id']:
                    return False

            else:
                members.append(
                    {
                        'user_id': new_member_id,
                        'username': new_member_username,
                    }
                )

                await self.filter(
                    giveaway_callback_value=callback_value
                ).update(users=members)


        except (KeyError, IndexError):
            members.append(
                {
                    'user_id': new_member_id,
                    'username': new_member_username,
                }
            )

            await self.create(
                giveaway_callback_value=callback_value,
                users=members
            )

        return True


    async def get_all_users(self, callback_value: str) -> list:

        data = await self.filter(
            giveaway_callback_value=callback_value
        ).all().values('users')

        try:
            return data[0]['users']

        except (KeyError, IndexError):
            return []
