import asyncio
import json
import os
import re
import time

import aiohttp
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from sqlalchemy import select

from config_data.config import HEADERS
from lexicon.lexicon_en import LEXICON
from models.methods import get_user
from models.models import User
from services.api_requests import make_async_post_request, stream_messages

router = Router()


#
@router.message(CommandStart())
async def process_start_command(message: Message, **kwargs):
    user_id = message.from_user.id
    session = kwargs['session_maker']
    user = await get_user(user_id, session)
    if not user:
        user = User(id=user_id)
        async with session() as session:
            session.add(user)
            await session.commit()
        await message.answer('You have been successfully registered')
    await message.answer(LEXICON['/start'])


@router.message(F.text)
async def send_message(message: Message, **kwargs):
    session = kwargs['session_maker']
    async with session() as session:
        user = await session.execute(select(User).where(User.id == message.from_user.id))
        user = user.scalars().one()
        session_uuid = user.session_uuid
        if not session_uuid:
            url = f'https://app.gpt-trainer.com/api/v1/chatbot/{os.getenv("CHAT_BOT_UUID")}/session/create'
            response_text = await make_async_post_request(url=url)
            response = json.loads(response_text)
            session_uuid = response.get('uuid')
            user.session_uuid = session_uuid
            session.add(user)
            await session.commit()
    url = f"https://app.gpt-trainer.com/api/v1/session/{session_uuid}/message/stream"
    request_text = message.text
    data = {
        'query': request_text
    }
    final_response = ''
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.post(url, headers=HEADERS, json=data, timeout=None) as response:
            if response.status == 200:
                is_first = True
                async for line in response.content.iter_any():
                    await asyncio.sleep(1.5)
                    final_response = final_response + line.decode()
                    if is_first:
                        sent_message = await message.answer(final_response)
                        is_first = False
                    else:
                        await sent_message.edit_text(final_response)
                        is_first = False
            else:
                print("Error:", response.status)
