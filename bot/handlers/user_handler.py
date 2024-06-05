# import asyncio
# import random
# from asyncio import sleep
#
# from aiogram import F, Router, Bot
# from aiogram.enums import ContentType
# from aiogram.types import Message
# from openai import AsyncOpenAI
# from bot.lexicon.errors import wrong_format
#
# from bot.lexicon.waiting import waiting_words
# from servecies.gpt_request import get_response_image_file, get_response_image_url, get_image
#
# from utils.encode_media import encode_image, encode_bytes
# from utils.validation import validate_url
#
# router = Router()
#
#
# @router.message(~F.content_type.in_({ContentType.TEXT, ContentType.PHOTO}), )
# async def wrong_file_format(message: Message):
#     await message.answer(text=wrong_format)
#
#
# @router.message(F.content_type.in_({ContentType.PHOTO}))
# async def processed_load_image_file(message: Message, bot: Bot, openai_client: AsyncOpenAI):
#     file_id = message.photo[-1].file_id
#     file = await bot.get_file(file_id)
#     photo = await bot.download_file(file.file_path)
#
#     base64_image = await encode_bytes(image_data=photo.getvalue())
#
#     response_future = asyncio.create_task(
#         get_response_image_file(image=base64_image, client=openai_client, system_prompt=system_prompt,
#                                 user_prompt=user_prompt, temperature=0.0)
#     )
#
#     waiting_message = await message.answer(text=random.choice(waiting_words))
#
#     while not response_future.done():
#         await asyncio.sleep(2)
#         new_waiting_text = random.choice(waiting_words)
#         # Check to avoid Telegram "Bad Request" error
#         if waiting_message.text != new_waiting_text:
#             try:
#                 await bot.edit_message_text(
#                     chat_id=waiting_message.chat.id,
#                     message_id=waiting_message.message_id,
#                     text=new_waiting_text
#                 )
#             except Exception as e:
#                 print(e)  # For logging the specific Telegram error
#     else:
#         await bot.delete_message(chat_id=waiting_message.chat.id, message_id=waiting_message.message_id)
#
#     response = await response_future
#
#     await bot.send_message(
#         chat_id=message.chat.id,
#         reply_to_message_id=message.message_id,
#         text=response,
#         parse_mode="MARKDOWN"
#     )
#     images = await get_image(client=openai_client, prompt=gen_image.format(response=response))
#     print()
#     # await bot.send_message(
#     #     chat_id=message.chat.id,
#     #     reply_to_message_id=message.message_id,
#     #     text=images,
#     #     parse_mode="MARKDOWN"
#     # )
#
# @router.message(F.content_type.in_({ContentType.TEXT}))
# async def processed_load_image_url(message: Message, openai_client: AsyncOpenAI, bot: Bot):
#     url = message.text
#     is_url = await validate_url(url)
#     if not is_url:
#         await message.answer(text="Это не ссылка")
#     else:
#
#         response_future = asyncio.create_task(
#             get_response_image_url(image_url=url, client=openai_client, system_prompt=system_prompt,
#                                    user_prompt=user_prompt, temperature=0.0)
#         )
#
#         waiting_message = await message.answer(text=random.choice(waiting_words))
#
#         while not response_future.done():
#             await asyncio.sleep(2)
#             new_waiting_text = random.choice(waiting_words)
#             # Check to avoid Telegram "Bad Request" error
#             if waiting_message.text != new_waiting_text:
#                 try:
#                     await bot.edit_message_text(
#                         chat_id=waiting_message.chat.id,
#                         message_id=waiting_message.message_id,
#                         text=new_waiting_text
#                     )
#                 except Exception as e:
#                     print(e)  # For logging the specific Telegram error
#         else:
#             await bot.delete_message(chat_id=waiting_message.chat.id, message_id=waiting_message.message_id)
#
#         response = await response_future
#
#         await bot.send_message(
#             chat_id=message.chat.id,
#             reply_to_message_id=message.message_id,
#             text=response,
#             parse_mode="MARKDOWN"
#         )
