from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram import Bot,Dispatcher,types,executor
from my_buttons import main_menu

# from datas import add_to_db, start_db

# async def on_startup(_):
#     await start_db()


class Registration(StatesGroup):
    name = State()
    surname = State()
    age = State()
    phone_num = State()
    adress = State()
    photo = State()

API = '7066715672:AAG4A04gMX_gI0s5XoR_wYmuYhUtzy5G5io'

bot = Bot(API)
storage = MemoryStorage()
dp = Dispatcher(bot=bot,storage=storage)


@dp.message_handler(commands=['start'])
async def send_hi(message:types.Message):
    user = message.from_user.first_name
    await message.answer(text=f'Asslamu aleykum {user}!',
                         reply_markup=main_menu)

@dp.message_handler(text='Registration📝')
async def begin_reg(message:types.Message):
    await message.answer('''Siz registraciya tuymesin bastiniz.
Birinshi bizge atinizdi jazip qaldirin:''')
    await Registration.name.set()
    
@dp.message_handler(state=Registration.name)
async def set_name(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer(text='Endi bizge familiyanizdi jazip qaldirin:')
    await Registration.surname.set()

@dp.message_handler(state=Registration.surname)
async def set_surname(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['surname']=message.text
    await message.answer('Endi bizge jasinizdi qaldirin:')
    await Registration.age.set()


@dp.message_handler(state=Registration.age)
async def set_age(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['age']=message.text
    await message.answer('Endi bizge nomerinizdi qaldirin:')
    await Registration.phone_num.set()
    


@dp.message_handler(state=Registration.phone_num)
async def set_age(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['phone_num']=message.text
    await message.answer('Endi bizge adresinizdi qaldirin:')
    await Registration.adress.set()



@dp.message_handler(state=Registration.adress)
async def set_age(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['adress']=message.text
    await message.answer('Endi bizge suwretinizdi qaldirin:')
    await Registration.photo.set()

@dp.message_handler(state=Registration.photo, content_types=['photo'])
async def set_photo(message:types.Message,state:FSMContext):
    img_id = message.photo[0].file_id
    async with state.proxy() as data:
        data['photo']= img_id,
    await bot.send_photo(
        photo= img_id,
        chat_id=message.from_user.id,
        caption=f'''Registarciya juwmaqlandi:
    ati: {data['name']},
    familiyasi: {data['surname']},
    jasi: {data['age']},
    nomeri: {data['phone_num']},
    addresi: {data['adress']} ''')

    await state.finish()


if __name__=='__main__':
    executor.start_polling(dp,skip_updates=True)
