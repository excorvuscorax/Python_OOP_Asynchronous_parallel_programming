import asyncio
import os

import aiohttp


async def download_one_image(
        session,
        url,
        image_number,
        path,
        results
):
    file_path = os.path.join(
        path,
        f"img_{image_number}.jpg"
    )

    try:
        async with session.get(url) as response:

            if response.status != 200:
                results.append(
                    {
                        "number": image_number,
                        "url": url,
                        "status": "Ошибка"
                    }
                )
                return

            content_type = response.headers.get(
                "Content-Type",
                ""
            )

            content = await response.read()

            if (
                not content
                or not content_type.startswith("image/")
            ):
                results.append(
                    {
                        "number": image_number,
                        "url": url,
                        "status": "Ошибка"
                    }
                )
                return


        with open(file_path, "wb") as file:
            file.write(content)


        results.append(
            {
                "number": image_number,
                "url": url,
                "status": "Успех"
            }
        )


    except aiohttp.ClientError:

        results.append(
            {
                "number": image_number,
                "url": url,
                "status": "Ошибка"
            }
        )


    except OSError:

        results.append(
            {
                "number": image_number,
                "url": url,
                "status": "Ошибка"
            }
        )


async def collect_links(path, results):

    tasks = []

    async with aiohttp.ClientSession() as session:

        image_number = 1

        while True:

            url = await asyncio.to_thread(
                input
            )

            url = url.strip()

            if not url:
                break


            task = download_one_image(
                session,
                url,
                image_number,
                path,
                results
            )

            tasks.append(task)

            image_number += 1


        if tasks:
            await asyncio.gather(*tasks)


    return results