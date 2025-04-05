#!/usr/bin/env python

import asyncio
import uvicorn
import websockets
import os
import numpy as np
import requests
import torch
import torchaudio
import sounddevice as sd

from fastapi import FastAPI

app = FastAPI()

DEBUG = False


@app.post("/text2audio")
def tts_and_play(text: str) -> str:
    print("text: ", text)

    
    # Prepare API request
    # url = f"http://{server_ip}:{server_port}/inference_instruct2_yuzhidi"
    
    # url = os.environ["TTS_API_URL"]
    url =  "http://10.11.106.128:50000/inference_instruct2_liang"
    # url =  "http://10.11.106.128:50000/inference_instruct2_yuzhidi"
    
    payload = {
        'tts_text': text,
        'instruct_text': "中文女",
    }

    # Make the API request
    response = requests.request("GET", url, data=payload, stream=True)
    response.raise_for_status()  # Raise an exception for bad status codes

    # Process the response
    target_sr = 22050
    tts_audio = b''
    for r in response.iter_content(chunk_size=16000):
        tts_audio += r
        
    tts_speech = torch.from_numpy(np.array(np.frombuffer(tts_audio, dtype=np.int16))).unsqueeze(dim=0)

    if DEBUG:
        # for debug
        output_path = "debug/tts.wav"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        torchaudio.save(output_path, tts_speech, target_sr)
    
    audio_array = tts_speech[0]
    sd.play(audio_array, samplerate=target_sr)

    return f"Converted"


# Simple message handler function
async def message_handler(websocket):
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            
            tts_and_play(message)

            # Echo the message back to the client
            response = f"Server received: {message}"
            await websocket.send(response)
            
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

# Start the WebSocket server
async def start_server():
    PORT = 50001
    async with websockets.serve(message_handler, "localhost", PORT):
        print(f"WebSocket server started at ws://localhost:{PORT}")
        # Keep the server running indefinitely
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    if 0:
        # Run the server
        asyncio.run(start_server())
    else:
        uvicorn.run(app, host="0.0.0.0", port=50002)