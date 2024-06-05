import base64

import aiofiles


async def encode_image(image_path):
    async with aiofiles.open(image_path, "rb") as image_file:
        image_data = await image_file.read()
        return base64.b64encode(image_data).decode("utf-8")

async def encode_bytes(image_data: bytes):
    return base64.b64encode(image_data).decode("utf-8")