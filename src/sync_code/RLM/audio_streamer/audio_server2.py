import grpc
import pyaudio
import numpy as np
import concurrent.futures
import time
from concurrent import futures

# Import generated gRPC modules
import audio_streaming_pb2
import audio_streaming_pb2_grpc

class AudioStreamerServicer(audio_streaming_pb2_grpc.AudioStreamerServicer):
    def __init__(self):
        # Initialize PyAudio
        self.p = pyaudio.PyAudio()
        # The stream will be created when the first audio chunk is received
        self.audio_stream = None
        
    def StreamAudio(self, request_iterator, context):
        """
        Receive streaming audio data from client and play it on the server's audio output
        """
        print("Client connected. Waiting for audio stream...")
        
        for request in request_iterator:
            # Get audio parameters from the request
            audio_chunk = request.audio_chunk
            sample_rate = request.sample_rate
            channels = request.channels
            format_str = request.format
            
            # Map format string to PyAudio format
            format_map = {
                "int16": pyaudio.paInt16,
                "int24": pyaudio.paInt24,
                "int32": pyaudio.paInt32,
                "float32": pyaudio.paFloat32
            }
            audio_format = format_map.get(format_str, pyaudio.paInt16)
            
            # Initialize audio stream if it's not already created
            if self.audio_stream is None:
                print(f"Starting audio playback: {sample_rate}Hz, {channels} channels, format: {format_str}")
                self.audio_stream = self.p.open(
                    format=audio_format,
                    channels=channels,
                    rate=sample_rate,
                    output=True,
                    frames_per_buffer=len(audio_chunk) // (2 if format_str == "int16" else 4)  # Adjust buffer size
                )
            
            # Play the received audio chunk
            self.audio_stream.write(audio_chunk)
            
        # Clean up
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.audio_stream = None
            
        print("Audio stream ended")
        
        return audio_streaming_pb2.AudioResponse(
            success=True,
            message="Audio stream completed successfully"
        )

def serve(address="[::]:50051"):
    """Start the gRPC server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    audio_streaming_pb2_grpc.add_AudioStreamerServicer_to_server(
        AudioStreamerServicer(), server
    )
    server.add_insecure_port(address)
    server.start()
    print(f"Server started, listening on {address}")
    
    try:
        # Keep the server running until interrupted
        while True:
            time.sleep(86400)  # Sleep for one day
    except KeyboardInterrupt:
        server.stop(0)
        print("Server stopped")

if __name__ == "__main__":
    serve()