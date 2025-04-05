

import grpc
import sounddevice as sd
import numpy as np
import concurrent.futures
import time
from concurrent import futures

# Import generated gRPC modules
import audio_streaming_pb2
import audio_streaming_pb2_grpc

class AudioStreamerServicer(audio_streaming_pb2_grpc.AudioStreamerServicer):
    def __init__(self):
        # The stream will be created when the first audio chunk is received
        self.audio_stream = None
        self.stream_active = False
        self.sample_rate = None
        self.channels = None
        self.dtype = None
        
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
            
            # Map format string to numpy dtype
            dtype_map = {
                "int16": np.int16,
                "int32": np.int32,
                "float32": np.float32
            }
            dtype = dtype_map.get(format_str, np.int16)
            
            # Initialize audio stream if it's not already created
            if not self.stream_active:
                self.sample_rate = sample_rate
                self.channels = channels
                self.dtype = dtype
                self.stream_active = True
                print(f"Starting audio playback: {sample_rate}Hz, {channels} channels, format: {format_str}")
                
                # Start the audio stream in a non-blocking callback mode
                def audio_callback(outdata, frames, time, status):
                    if status:
                        print(f"Audio status: {status}")
                    
                self.audio_stream = sd.OutputStream(
                    samplerate=sample_rate,
                    channels=channels,
                    dtype=dtype.__name__,
                    callback=audio_callback
                )
                self.audio_stream.start()
            
            # Convert bytes to numpy array and play
            if len(audio_chunk) > 0:
                # Convert bytes to numpy array
                if dtype == np.int16:
                    samples_per_frame = len(audio_chunk) // (2 * channels)
                    audio_array = np.frombuffer(audio_chunk, dtype=dtype).reshape(samples_per_frame, channels)
                elif dtype == np.int32:
                    samples_per_frame = len(audio_chunk) // (4 * channels)
                    audio_array = np.frombuffer(audio_chunk, dtype=dtype).reshape(samples_per_frame, channels)
                elif dtype == np.float32:
                    samples_per_frame = len(audio_chunk) // (4 * channels)
                    audio_array = np.frombuffer(audio_chunk, dtype=dtype).reshape(samples_per_frame, channels)
                
                # Play the audio directly
                sd.play(audio_array, sample_rate, blocking=False)
            
        # Clean up
        if self.audio_stream:
            self.audio_stream.stop()
            self.audio_stream.close()
            self.audio_stream = None
            self.stream_active = False
            
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