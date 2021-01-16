from asyncio import get_event_loop

from src.service_client import ServiceClient

loop = get_event_loop()

SERVICE_URL = "http://testapi.ru/"


async def main():
    client = ServiceClient(SERVICE_URL)
    await client.auth()
    data = await client.get_user_info("ivanov")
    await client.update_user_info("0", data)


if __name__ == "__main__":
    loop.run_until_complete(main())
