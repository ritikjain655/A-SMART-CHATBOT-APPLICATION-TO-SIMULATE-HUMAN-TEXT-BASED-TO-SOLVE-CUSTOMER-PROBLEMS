from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from AiContext import recognize_intent2
from intents import intents
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import question_fetcher, solution, score_updater
import asyncio

token = '6723215363:AAHWFqM1OgNFFZ5vxCjwRGZSGKsA3ebeF_4'
#token='6490021167:AAEGZFo0IzCDa6VIhNbL3ObMBos8y6pTZi4'
ADMIN_ID = 5906012237
dp = Dispatcher()
bot = Bot(token, parse_mode=ParseMode.HTML)

dict2 = {1:'performance_faq',
                         2:'update_faq',
                         3:'display_faq',
                         4:'netw_faq',
                         5:'crash_faq'}

def drop_down_all():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Performance ⚡️", callback_data="1")
    keyboard_builder.button(text="Update 🔄", callback_data="2")
    keyboard_builder.button(text="Screen 🖥️", callback_data="3")
    keyboard_builder.button(text="Network & Bluetooth 🌐🔵", callback_data="4")
    keyboard_builder.button(text="System Crash | Reboot | Shut Down 💥🔄🛑", callback_data="5")
    keyboard_builder.button(text="Explain Your Issue Again 🔄❓", callback_data="6")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()



def qustions(data):
    keyboard_builder = InlineKeyboardBuilder()
    c = 1
    for i in data:
        keyboard_builder.button(text=f"{i}", callback_data=f"{c}")
        c += 1

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def yes_no():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Yes ✅", callback_data="1")
    keyboard_builder.button(text="No ❌", callback_data="0")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


class problemss(StatesGroup):
    take_problem = State()
    second_input = State()
    drop_down_state = State()
    solutionsss = State()
    solution_c = State()
    customer_s = State()

class with_intent(StatesGroup):
    provide_det = State()
    common_prob = State()

def recognize_intent(message):
    global context  # Using the global context variable

    for intent in intents:
        for pattern in intent['patterns']:
            if pattern in message:
                if 'context' in intent:
                    context = intent['context']  # Updating the context
                return intent
    return None


@dp.message(lambda m : m.from_user.id == ADMIN_ID)
async def land_msg(message: types.Message,state:FSMContext) -> None:
    if message.reply_to_message:
        reply_message = message.reply_to_message
        CURRENT_CHAT = reply_message.forward_from.id
        try:
            if message.photo or message.video or message.audio or message.voice:
                await message.copy_to(CURRENT_CHAT, message.message_thread_id)
            else:
                await bot.send_message(CURRENT_CHAT, message.text)
        except Exception as e:
            await bot.send_message(ADMIN_ID, str(e))
    else:
        await bot.send_message(ADMIN_ID, 'No Chat Selected')

@dp.message(lambda m : m.text == '/start')
async def all_messages(message: types.Message,state:FSMContext) -> None:
    if message.from_user.id != ADMIN_ID:
        await message.answer('''👋 Hello! I'm your customer service chatbot.
        I'm here to assist you with Windows Troubleshooting. 🛠️ 
        Please, briefly explain your issue, and I'll do my best to help!''')
        await state.set_state(problemss.take_problem)



@dp.message(problemss.take_problem)
async def options(message: Message, state: FSMContext) -> None:
    intent = recognize_intent(message.text)
    await message.answer(f"🤖 AI Model Predicted Intent: {recognize_intent2(message.text)}")
    if intent is not None:
        response = intent['responses'][0]
        if 'context' in intent:
            context = intent['context']
        else:
            context = None

    else:
        response = ''
        context = None

        if context is None or message.text == "No":
            await message.answer("🤔 I'm not sure how to respond to that. Please choose an option from the following drop-down.")
            await message.answer('🌟 Choose your options', reply_markup=drop_down_all())
            await state.set_state(problemss.second_input)

    if context is None:
        print(response)
        if response in [None,'']:
            pass
        else:
            await message.answer(response)

    if context == 'describe_issue':
        await message.answer("🔍 Can you please provide more details about your problem?")

    if context == 'provide_details':
        await message.answer(f'{response}')
        await message.answer("👤 Is your request related to technical support?", reply_markup=yes_no())
        await state.set_state(with_intent.provide_det)

    if context == 'crash_faq':
        await message.answer(f'{response}',reply_markup=yes_no())
        await state.update_data(table=context)
        await state.set_state(with_intent.common_prob)

    if context == 'display_faq':
        await message.answer(f'{response}',reply_markup=yes_no())
        await state.update_data(table=context)
        await state.set_state(with_intent.common_prob)

    if context == 'netw_faq':
        await message.answer(f'{response}',reply_markup=yes_no())
        await state.update_data(table=context)
        await state.set_state(with_intent.common_prob)

    if context == 'performance_faq':
        await message.answer(f'{response}',reply_markup=yes_no())
        await state.update_data(table=context)
        await state.set_state(with_intent.common_prob)

    if context == 'update_faq':
        await message.answer(f'{response}',reply_markup=yes_no())
        await state.update_data(table=context)
        await state.set_state(with_intent.common_prob)


@dp.callback_query(with_intent.common_prob)
async def second_options(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.data == '1':
        data = await state.get_data()
        questions = question_fetcher(data['table'])
        questions_keys = questions.keys()
        await callback.message.edit_text("🔍 Select your problem from the following drop-down", reply_markup=qustions(questions_keys))
        await state.set_state(problemss.solutionsss)
    else:
        await callback.message.answer('🔄 Please explain your problem again')
        await callback.message.delete()

        await state.set_state(problemss.take_problem)




@dp.callback_query(with_intent.provide_det)
async def second_options(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.data == '1':
        await callback.answer('🔗 Connecting you to the customer executive!')
        await callback.message.answer("👋 Hi! I am Mann Kumar,How can I help you?")
        await callback.message.delete()

        await state.set_state(problemss.customer_s)

    else:
        await callback.message.answer('Choose',reply_markup=drop_down_all())
        await callback.message.delete()

        await state.set_state(problemss.second_input)

@dp.callback_query(problemss.second_input)
async def second_options(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.data == '6':
        await callback.message.answer("🔄 Please explain your issue again!")
        await callback.message.delete()
        await state.set_state(problemss.take_problem)
    else:
        table = dict2[int(callback.data)]
        await state.update_data(
            table=table
        )
        questions = question_fetcher(table)
        questions_keys = questions.keys()
        await callback.message.edit_text("🔍 Select your problem from the following drop-down", reply_markup=qustions(questions_keys))
        #await callback.message.delete()

        await state.set_state(problemss.solutionsss)

@dp.callback_query(problemss.solutionsss)
async def solution_options(callback: CallbackQuery, state: FSMContext) -> None:
    xnb = await state.get_data()
    x = solution(callback.data, xnb['table'], 0)

    await state.update_data(
        n=0,
        uska_callback=callback.data,
        x = x
    )
    await callback.message.answer(f"💡 Solution: {x}")
    await callback.message.answer("🤔 Is your problem solved?", reply_markup=yes_no())
    await callback.message.delete()
    await state.set_state(problemss.solution_c)


@dp.callback_query(problemss.solution_c)
async def teri_mamki(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    if callback.data == '0':
        try:
            new_value = data['n'] + 1
            await callback.message.answer(f"💡 Solution: {solution(data['uska_callback'], data['table'], new_value)}")
            await state.update_data(
                n = new_value
            )
            await callback.message.answer("🤔 Is your problem solved?", reply_markup=yes_no())
            await callback.message.delete()

        except IndexError:
            await callback.answer('🔗 Connecting you to the customer executive!')
            await callback.message.answer("👋 Hi! I am Mann Kumar,How can I help you?")
            await state.set_state(problemss.customer_s)
    else:
        await callback.message.answer("🌟 Thank you so much! I'm glad I could help you.")
        await callback.message.delete()
        score_updater(data['x'], data['table'])


@dp.message(problemss.customer_s)
async def a9eur_baa(message: Message, state: FSMContext) -> None:
    await bot.forward_message(ADMIN_ID,message.from_user.id, message.message_id)

async def start() -> None:
    try:
        await dp.start_polling(bot,polling_timeout=10)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())



