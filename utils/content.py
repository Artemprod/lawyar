
import aiofiles


async def read_txt(file_path):
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
        text = await file.read()
    return text


async def get_file_content(file_path):
    if file_path.endswith('.txt'):
        return await read_txt(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or TXT file.")
