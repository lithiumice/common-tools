#!/usr/bin/env python

import asyncio
import os
import numpy as np
import requests
import torch
import torchaudio
import sounddevice as sd
import uvicorn
import websockets
import hydra
from hydra.core.config_store import ConfigStore
from dataclasses import dataclass
from typing import Optional
from omegaconf import DictConfig, OmegaConf
from fastapi import FastAPI


# @dataclass
# class TTSConfig:
#     api_url: str = "http://10.11.106.128:50000/inference_instruct2_liang"
#     instruct_text: str = "冷静闷骚高冷酷女"
#     target_sr: int = 22050
#     debug: bool = False
#     debug_dir: str = "debug"


# @dataclass
# class ServerConfig:
#     websocket_port: int = 50001
#     websocket_host: str = "localhost"
#     fastapi_port: int = 50002
#     fastapi_host: str = "0.0.0.0"
#     run_websocket: bool = False
#     run_fastapi: bool = True


# @dataclass
# class AppConfig:
#     tts: TTSConfig = TTSConfig()
#     server: ServerConfig = ServerConfig()


# cs = ConfigStore.instance()
# cs.store(name="config", node=AppConfig)


class TTSServer:
    def __init__(self, config):
        self.config = config
        self.app = FastAPI()
        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/text2audio")
        def tts_and_play(text: str) -> str:
            print("text: ", text)
            return self.process_tts(text)

    def process_tts(self, text: str) -> str:
        # Prepare API request
        url = self.config.tts.api_url
        
        payload = {
            'tts_text': text,
            'instruct_text': self.config.tts.instruct_text,
        }

        # Make the API request
        response = requests.request("GET", url, data=payload, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Process the response
        target_sr = self.config.tts.target_sr
        tts_audio = b''
        for r in response.iter_content(chunk_size=16000):
            tts_audio += r
            
        tts_speech = torch.from_numpy(np.array(np.frombuffer(tts_audio, dtype=np.int16))).unsqueeze(dim=0)

        if self.config.tts.debug:
            # for debug
            output_path = os.path.join(self.config.tts.debug_dir, "tts.wav")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            torchaudio.save(output_path, tts_speech, target_sr)
        
        audio_array = tts_speech[0]
        sd.play(audio_array, samplerate=target_sr)

        return f"Converted"

    # Simple message handler function for WebSocket
    async def message_handler(self, websocket):
        try:
            async for message in websocket:
                print(f"Received message: {message}")
                
                self.process_tts(message)

                # Echo the message back to the client
                response = f"Server received: {message}"
                await websocket.send(response)
                
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")

    # Start the WebSocket server
    async def start_websocket_server(self):
        host = self.config.server.websocket_host
        port = self.config.server.websocket_port
        
        async with websockets.serve(self.message_handler, host, port):
            print(f"WebSocket server started at ws://{host}:{port}")
            # Keep the server running indefinitely
            await asyncio.Future()  # Run forever
    
    def start_fastapi_server(self):
        host = self.config.server.fastapi_host
        port = self.config.server.fastapi_port
        
        uvicorn.run(self.app, host=host, port=port)


@hydra.main(config_path="conf", config_name="tts", version_base=None)
def main(cfg) -> None:
    print(OmegaConf.to_yaml(cfg))
    
    server = TTSServer(cfg)
    
    if cfg.server.run_websocket:
        asyncio.run(server.start_websocket_server())
    else:
        server.start_fastapi_server()


if __name__ == "__main__":
    main()