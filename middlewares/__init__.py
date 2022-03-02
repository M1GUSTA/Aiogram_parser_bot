from aiogram import Dispatcher
from loader import dp

from .throttling import ThrottlingMiddleware
from .link_checking import LinkCheck


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(LinkCheck())