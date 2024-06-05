from openai import AsyncOpenAI
from utils.content import  read_txt


async def get_response_image_file(image, client: AsyncOpenAI, system_prompt, user_prompt, temperature=1.8,

                                  top_p=0.9,
                                  presence_penalty=0.9,
                                  frequency_penalty=0.9,
                                  model="gpt-4o"):
    answer = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system",
             "content": system_prompt},
            {"role": "user", "content": [
                {"type": "text",
                 "text": user_prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image}"}
                 }
            ]}
        ],
        max_tokens=1000,
        temperature=temperature,
        top_p=top_p,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty

    )
    return answer.choices[0].message.content


async def get_image(client: AsyncOpenAI, prompt, model="dall-e-3", ):
    answer = await client.images.generate(
        prompt=prompt,
        model=model,
        quality='hd',
        size='1024x1792',
        style='natural',
        response_format="b64_json"

    )

    return answer.choices[0].message['content']


async def get_response_image_url(client: AsyncOpenAI, image_url, system_prompt, user_prompt, temperature=0.0,
                                 model="gpt-4o"):
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": user_prompt},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]}
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content






async def get_response_file(file_path,
                            client: AsyncOpenAI,
                            system_prompt,
                            user_prompt,
                            temperature=0.0,
                            top_p=0.0,
                            presence_penalty=0.0,
                            frequency_penalty=0.0, model="gpt-4o"):

    if file_path.endswith('.txt'):
        content = await read_txt(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or TXT file.")

    answer = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prompt}\n\n{content}"}
        ],
        temperature=temperature,
        top_p=top_p,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty
    )
    print()
    return answer.choices[0].message.content

async def get_response_from_openai(content, client: AsyncOpenAI, system_prompt, user_prompt, temperature=1.8,
                                   top_p=0.9, presence_penalty=0.9, frequency_penalty=0.9, model="gpt-4o"):
    answer = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prompt}\n\n{content}"}
        ],
        temperature=temperature,
        top_p=top_p,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty
    )

    return answer.choices[0].message.content