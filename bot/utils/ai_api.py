
import requests
import json
import aiohttp


# def get_response_from_server(history):
#     url = 'http://gptserver.alwaysdata.net/get_response'
#     headers = {
#         'Content-Type': 'application/json'
#     }
#     data = {
#         "history": history
#     }

#     response = requests.post(url, headers=headers, data=json.dumps(data))
    
    
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {"error": f"Request failed with status code {response.status_code}"}


async def get_response_from_server(history):
    url = 'http://gptserver.alwaysdata.net/get_response'
    headers = {'Content-Type': 'application/json'}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json={"history": history}) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Request failed with status code {response.status}"}
        




# async def main():
#     result = await chatgpt_text_generator("mavzu", [{"role": "user", "content": "mening ismim amirjon"}])
#     print(result)
# asyncio.run(main())