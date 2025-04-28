import requests
import json
import time
def do(promt):
    url = 'https://chat.chatgptdemo.net/chat_api_stream'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36'
    }
    data = {
    "question": promt,
    "chat_id": "671de410f71af65b487f69b3",
    "timestamp": int(time.time() * 1000),  # current timestamp in milliseconds
    "retry": False
}

# Send the request with streaming enabled
    response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
    
    # Check if the request was successful
    if response.status_code == 200:
        
        # Iterate over the streamed chunks
        for chunk in response.iter_content(chunk_size=None):
            if chunk: 
                try:
                    print(json.loads(chunk.decode('utf-8')[5:])["choices"][0]["delta"]["content"], end="")
                except:
                    print("", end="")
                time.sleep(0.1) # Print the data as it arrives
    else:
        print("", end="")
    print()
        
        
while 1:
    prompt = input('Message GPT >>> ')
    do(prompt)