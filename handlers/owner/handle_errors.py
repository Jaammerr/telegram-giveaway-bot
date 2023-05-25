from app import dp, bot
from config import OWNERS



@dp.errors_handler(
    exception=Exception
)
async def handle_bot_exceptions(
        update,
        error
):
    user_id = update['message']['from']['id']
    username = update['message']['from']['username']
    message_text = update['message']['text']

    for owner_id in OWNERS:
        await bot.send_message(
            chat_id=owner_id,
            text=f'<b>🚫  Произошла непредвиденная ошибка</b>\n\nID пользователя: {user_id}\nUsername пользователя: {username}\n\nТекст сообщения:\n<code>{message_text}</code>\n\nТекст ошибки:\n<code>{error}</code>'
        )

    return True
