from aiogram import Bot, Dispatcher

from app.routers import inline_router, private_router
from app.middlewares import InfoLoggerMiddleware, ThrottlingMiddleware
from app.config import config
from app import utils


def setup_logging(dp: Dispatcher):
    dp["aiogram_logger"] = utils.logging.setup_logger().bind(type="aiogram")
    dp["throttling_logger"] = utils.logging.setup_logger().bind(type="throttling")


def setup_handlers(dp: Dispatcher):
    dp.include_routers(inline_router, private_router)


def setup_middlewares(dp: Dispatcher):
    dp.update.outer_middleware(InfoLoggerMiddleware(logger=dp["aiogram_logger"]))
    dp.message.middleware(ThrottlingMiddleware(logger=dp["throttling_logger"], throttling_time=5))


async def setup_aiogram(dp: Dispatcher, bot: Bot):
    setup_logging(dp)
    setup_middlewares(dp)
    logger = dp["aiogram_logger"]
    logger.debug("Configuring aiogram")
    setup_handlers(dp)
    logger.info("Configured aiogram")


async def aiogram_on_startup(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_aiogram(dispatcher, bot)
    dispatcher["aiogram_logger"].info("Started polling")


async def aiogram_on_shutdown(dispatcher: Dispatcher, bot: Bot):
    dispatcher["aiogram_logger"].debug("Stopping polling")
    await bot.session.close()
    await dispatcher.storage.close()
    dispatcher["aiogram_logger"].info("Stopped polling")


def main():
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher()

    dp.startup.register(aiogram_on_startup)
    dp.shutdown.register(aiogram_on_shutdown)
    dp.run_polling(bot)


if __name__ == '__main__':
    main()
