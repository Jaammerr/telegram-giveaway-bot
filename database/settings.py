from tortoise import Tortoise
from config import database_url, timezone_info



async def initialize_database():
    await Tortoise.init(
        db_url=database_url,
        modules=
        {
            'models':
                [
                    'database.models.giveaway',
                    'database.models.telegram_channel',
                    'database.models.giveaway_statistic',
                    'database.models.temporary_users',
                ]
        },
        timezone=str(timezone_info.zone)
    )

    await Tortoise.generate_schemas()
