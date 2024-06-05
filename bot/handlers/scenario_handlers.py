import asyncio
import os
import random
import tempfile
import uuid
from asyncio import sleep

from aiogram import F, Router, Bot
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from openai import AsyncOpenAI

from bot.keyboards.inline_keyboards import crete_inline_keyboard_ready, crete_inline_keyboard_assistants
from bot.lexicon.errors import wrong_format
from bot.lexicon.prompts import assistants
from bot.lexicon.waiting import waiting_words
from bot.states.load import FSMSummaryLode
from servecies.gpt_request import get_response_image_file, get_response_image_url, get_image, get_response_file, \
    get_response_from_openai
from utils.content import get_file_content

from utils.encode_media import encode_image, encode_bytes
from utils.validation import validate_url

router = Router()




@router.callback_query(F.data == "contract")
async def process_contract_recognize_choise(
        callback: CallbackQuery,
        state: FSMContext, ):
    await callback.message.answer(text="Загрузи документ")
    await state.set_state(FSMSummaryLode.load_one_file)


@router.callback_query(F.data == "compare")
async def process_compare_contracts_choise(
        callback: CallbackQuery,
        state: FSMContext, ):
    await callback.message.answer(text="Загрузи 2 документа")
    await state.set_state(FSMSummaryLode.load_partaily)


@router.message(
    FSMSummaryLode.load_one_file,
    F.content_type.in_(
        {
            ContentType.DOCUMENT,
        }
    ),
)
async def process_contract_recognize(message: Message, bot: Bot, openai_client: AsyncOpenAI, state: FSMContext, ):
    document = message.document
    # Получаем файл с помощью API и скачиваем его
    file = await bot.get_file(document.file_id)
    file_path = file.file_path
    with tempfile.TemporaryDirectory() as temp:
        destination = os.path.join(temp, f"{uuid.uuid4()}_{document.file_name}.txt")

        await bot.download_file(file_path, destination)
        response = await get_response_file(file_path=destination,
                                           client=openai_client,
                                           system_prompt=assistants['contract']['system_prompt'],
                                           user_prompt=assistants['contract']['user_prompt'])
        await message.answer(text=response,reply_markup=crete_inline_keyboard_assistants())
        await state.clear()


@router.message(
    FSMSummaryLode.load_partaily,
    F.content_type.in_(
        {
            ContentType.DOCUMENT,
        }
    ),
)
async def process_load_partaily(message: Message, bot: Bot, openai_client: AsyncOpenAI, state: FSMContext, ):
    document_id = message.document.file_id
    data = await state.get_data()
    documents = data.get('documents', [])
    documents.append(document_id)
    await state.update_data(documents=documents)
    await message.answer("Документ получен. Отправьте еще документы или нажси кнопку', чтобы начать обработку.",
                         reply_markup=crete_inline_keyboard_ready())


@router.callback_query(
    F.data == "ready",
    FSMSummaryLode.load_partaily,
)
async def process_compare(callback_query: CallbackQuery, bot: Bot, openai_client: AsyncOpenAI, state: FSMContext, ):
    print("lf")
    option_keyboard = crete_inline_keyboard_assistants()
    await callback_query.answer()  # Закрываем уведомление о нажатии кнопки
    data = await state.get_data()
    documents = data.get('documents', [])

    if not documents:
        await bot.send_message(callback_query.from_user.id, "Вы не отправили ни одного документа.")
    else:
        combined_text = ""
        print()
        for document_id in documents:
            # Получаем файл с помощью API и скачиваем его
            file = await bot.get_file(document_id)
            file_path = file.file_path

            with tempfile.TemporaryDirectory() as temp:
                destination = os.path.join(temp, f"{uuid.uuid4()}_{document_id}.txt")

                await bot.download_file(file_path, destination)
                content = await get_file_content(destination)
                combined_text += f"\n\n{content}"

        response = await get_response_from_openai(
            combined_text,
            openai_client,
            system_prompt=assistants['contract']['system_prompt'],
            user_prompt=assistants['contract']['user_prompt']
        )
        await bot.send_document(
            chat_id=callback_query.message.chat.id,
            document=BufferedInputFile(file=response.encode("utf-8"), filename="Документ"),
            reply_markup=option_keyboard

        )

        await state.clear()
