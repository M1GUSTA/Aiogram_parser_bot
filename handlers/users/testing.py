from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from states import Test


@dp.message_handler(Command("test"))
async def enter_test(message: types.Message):
    await message.answer("Вы начали тестирование.\n"
                         "Вопрос №1.\n"
                         "Вы часто заниметесь бессмысленными делами "
                         "(бусцельно блуждаете по интернету, клацаете пультом телевизора, просто смотрите в окно)")
await Test.Q1.set()


@dp.message_handler(state=Test.Q1)
async def answer_ql(message:types.Message, state: FSMContext):
    answer = message.text

    # await state.update_data(answer1=answer)
    # await state.update_data(
    #     {
    #         "answer1": answer
    #     }
    # )
    async with state.proxy() as data:
        data["answer1"] = answer
    await message.answer("Впорос №2. \n\n"
                         "Ваша память ухудшилась и вы помите то, что было давно, но забываете недавние события.")
    await Test.next()