import re
import asyncio


async def validate_url(url):
    url_regex = (
        r'^(?:https?|ftp)://'  # http://, https:// или ftp://
        r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?::\d{2,5})?'
        r'(?:/[^\s]*)?$'  # путь до ресурса
    )
    return bool(re.match(url_regex, url))


if __name__ == '__main__':
    url = "https://www.example.com"
    print(asyncio.run(validate_url(url)))
