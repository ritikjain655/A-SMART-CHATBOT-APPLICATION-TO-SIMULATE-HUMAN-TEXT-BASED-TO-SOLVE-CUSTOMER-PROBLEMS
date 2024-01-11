import asyncio,requests
import logging
from aiogram import Bot, Dispatcher
from dataclasses import dataclass
from aiogram import Router
from aiogram.types import Message


router: Router = Router()

@router.message()
async def process_any_message(message: Message):
    await message.answer('DU DU DU DU DU DORA... DORA')

@dataclass
class TelegramBotConfig:
    token: str

@dataclass
class Config:
    tg_bot: TelegramBotConfig

def load_config() -> Config:
    return Config(tg_bot=TelegramBotConfig(token="6539551104:AAEb3Sre042AhUnOiGE78_HVk6h2vtxxBng"))

logger = logging.getLogger(__name__)

import re

def extract_order_id(text):
    pattern = r'Order ID: (\w+)'
    match = re.search(pattern, text)

    if match:
        return match.group(1)
    else:
        return None

def caesar_decrypt_numeric_lowercase(ciphertext):
    shift = 5
    decrypted_data = ''
    for char in ciphertext:
        if char.isalpha():
            # Convert lowercase alphabet to numeric digit
            decrypted_data += str((ord(char) - ord('a') - shift) % 10)
        else:
            decrypted_data += char
    return int(decrypted_data)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher()

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")