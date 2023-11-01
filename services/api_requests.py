import aiohttp

from config_data.config import HEADERS


async def make_async_get_request(url, data=None):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url, headers=HEADERS, data=data) as response:
            response_text = await response.text()
            return response_text


async def make_async_post_request(url, data=None):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.post(url, headers=HEADERS, data=data) as response:
            response_text = await response.text()
            return response_text


async def stream_messages(session_uuid, request_text):
    url = f'https://app.gpt-trainer.com/api/v1/session/{session_uuid}/message/stream'
    data = {
        'query': request_text
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=HEADERS, json=data, timeout=None) as response:
            if response.status == 200:
                async for line in response.content.iter_any():
                    print(line.decode())
            else:
                print("Error:", response.status)
