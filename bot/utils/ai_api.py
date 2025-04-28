
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


# async def get_response_from_server(history):
#     url = 'http://gptserver.alwaysdata.net/get_response'
#     headers = {'Content-Type': 'application/json'}
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, headers=headers, json={"history": history}) as response:
#             if response.status == 200:
#                 return await response.json()
#             return {"error": f"Request failed with status code {response.status}"}
        
import requests
url = "https://chatbot-ji1z.onrender.com/chatbot-ji1z"
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "sec-ch-ua-platform": '"Android"',
    "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "sec-ch-ua-mobile": "?1",
    "origin": "https://seoschmiede.at",
    "sec-fetch-site": "cross-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "accept-language": "uz-UZ,uz;q=0.9,en-US;q=0.8,en;q=0.7",
    "priority": "u=1, i"
}

async def get_response_from_server(history):
    data = {
        "messages":history
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return {'response':response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response from API.")}
    else:
        return "Error: Could not get a valid response from the API."

# data = [
#         {
#             "role": "user",
#             "content": (
#                 "salom"
#             )
#         }
#     ]
# print(get_response_from_server(data))



# async def main():
#     result = await chatgpt_text_generator("mavzu", [{"role": "user", "content": "mening ismim amirjon"}])
#     print(result)
# asyncio.run(main())
