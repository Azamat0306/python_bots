from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram import Bot,Dispatcher,types,executor
from my_buttons import main_menu
from datas import add_to_db, start_db

async def on_startup(_):
    await start_db()


class Registration(StatesGroup):
    model = State()
    colour = State()
    dvigatel = State()
    year = State()
    poziciya = State()
    probeg = State()
    cena = State()
    yoqilgi = State()
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
Siz mashina modelin saylan:''')
    await Registration.model.set()
    
@dp.message_handler(state=Registration.model)
async def set_model(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['model'] = message.text
    await message.answer(text='Endi bizge renin jazip qaldirin:')
    await Registration.colour.set()

@dp.message_handler(state=Registration.colour)
async def set_colour(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['colour']=message.text
    await message.answer('Endi bizge mashina dvigatelin jazin:')
    await Registration.dvigatel.set()


@dp.message_handler(state=Registration.dvigatel)
async def set_dvigatel(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['dvigatel']=message.text
    await message.answer('Endi bizge mashina jilin jazin:')
    await Registration.year.set()
    

@dp.message_handler(state=Registration.year)
async def set_year(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['year']=message.text
    await message.answer('Endi bizge mashina poziciyasin jazin:')
    await Registration.poziciya.set()


@dp.message_handler(state=Registration.poziciya)
async def set_poziciya(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['poziciya']=message.text
    await message.answer('Endi bizge mashina probegin jazin:')
    await Registration.probeg.set()

@dp.message_handler(state=Registration.probeg)
async def set_probeg(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['probeg']=message.text
    await message.answer('Endi bizge mashina bahasin jazin:')
    await Registration.cena.set()

@dp.message_handler(state=Registration.cena)
async def set_cena(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['cena']=message.text
    await message.answer('Endi bizge mashina yoqilgisi qanday ekinin jazin:')
    await Registration.yoqilgi.set()

@dp.message_handler(state=Registration.yoqilgi)
async def set_yoqilgi(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['yoqilgi']=message.text
    await message.answer('Endi bizge mashina fotosin jiberin:')
    await Registration.photo.set()

@dp.message_handler(state=Registration.photo, content_types=['photo'])
async def set_photo(message:types.Message,state:FSMContext):
    img_id = message.photo[0].file_id
    async with state.proxy() as data:
        data['photo']= img_id
    await add_to_db(
        model=data['modeli'],
        year=data['jili'],
        probegi=['probegi'],
        colour=['reni'],
        cena = ['cenasi'],
        poziciya = ['poziciyasi'],
        dvigatel = ['dvigateli'],
        photo = ['fotosi']

    )
    await bot.send_photo(
        photo= img_id,
        chat_id=message.from_user.id,
        caption=f'''Registraciya juwmaqlandi:
   🚘model: {data['modeli']},
   ⚪️colour: {data['reni']},
    🎛dvigatel: {data['dvigateli']},
   ⚡️year: {data['jili']},
   🎚poziciya: {data['poziciyasi']},
   🔝probeg: {data['probegi']},
   💲cena: {data['cenasi']},
   🔋yoqilgi: {data['yoqilgisi']} ''')

    await state.finish()


if __name__=='__main__':
    executor.start_polling(dp,skip_updates=True, on_startup=on_startup)
