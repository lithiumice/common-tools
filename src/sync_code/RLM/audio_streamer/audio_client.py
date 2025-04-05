


import grpc
import sounddevice as sd
import numpy as np
import time
import argparse
import threading
import queue

# Import generated gRPC modules
import audio_streaming_pb2
import audio_streaming_pb2_grpc

def record_and_stream(server_address="localhost:50051", chunk_size=1024, sample_rate=44100, channels=1):
    """
    Record audio from the microphone and stream it to the server
    """
    # Create a gRPC channel
    with grpc.insecure_channel(server_address) as channel:
        stub = audio_streaming_pb2_grpc.AudioStreamerStub(channel)
        
        # Create a queue for audio chunks
        audio_queue = queue.Queue()
        
        # Define the callback function for the audio input stream
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Input status: {status}")
            # Put the audio data in the queue
            audio_queue.put(bytes(indata))
        
        # Create an input stream
        stream = sd.InputStream(
            samplerate=sample_rate,
            channels=channels,
            dtype='int16',
            blocksize=chunk_size,
            callback=audio_callback
        )
        
        print(f"Connected to server at {server_address}")
        print(f"Recording audio: {sample_rate}Hz, {channels} channels, chunk size: {chunk_size}")
        print("Press Ctrl+C to stop recording")
        
        # Start the stream
        stream.start()
        
        try:
            # Create a generator to stream audio requests
            def generate_requests():
                while True:
                    try:
                        # Get audio data from the queue (with timeout to check for interrupts)
                        audio_data = audio_queue.get(timeout=1.0)
                        
                        # Create and yield the request
                        yield audio_streaming_pb2.AudioRequest(
                            audio_chunk=audio_data,
                            sample_rate=sample_rate,
                            channels=channels,
                            format="int16"
                        )
                    except queue.Empty:
                        # No audio data available, check if we should continue
                        if not stream.active:
                            break
                        continue
            
            # Stream the audio to the server
            response = stub.StreamAudio(generate_requests())
            print(f"Streaming complete: {response.message}")
            
        except KeyboardInterrupt:
            print("Streaming interrupted by user")
        except grpc.RpcError as e:
            print(f"RPC error: {e.code()}: {e.details()}")
        finally:
            # Clean up
            stream.stop()
            stream.close()
            print("Audio client stopped")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audio streaming client")
    parser.add_argument("--server", default="localhost:50051", 
                        help="Server address in format host:port")
    parser.add_argument("--rate", type=int, default=44100, 
                        help="Audio sample rate in Hz")
    parser.add_argument("--channels", type=int, default=1, 
                        help="Number of audio channels (1 for mono, 2 for stereo)")
    parser.add_argument("--chunk", type=int, default=1024, 
                        help="Audio chunk size in samples")
    
    args = parser.parse_args()
    
    record_and_stream(
        server_address=args.server, 
        sample_rate=args.rate, 
        channels=args.channels,
        chunk_size=args.chunk
    )