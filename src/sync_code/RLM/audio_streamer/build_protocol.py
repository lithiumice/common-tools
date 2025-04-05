from grpc_tools import protoc
import os
import sys

def generate_proto_code():
    """
    Generate Python code from the .proto file
    """
    print("Generating protocol code from audio_streaming.proto...")
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the .proto file
    proto_file = os.path.join(current_dir, 'audio_streaming.proto')
    
    # Check if the file exists
    if not os.path.exists(proto_file):
        print(f"Error: {proto_file} not found!")
        return False
    
    # Protocol buffer compiler command
    protoc_command = [
        'grpc_tools.protoc',
        f'--proto_path={current_dir}',
        f'--python_out={current_dir}',
        f'--grpc_python_out={current_dir}',
        proto_file
    ]
    
    # Execute the command
    if protoc.main(protoc_command) != 0:
        print("Error: Failed to generate protocol buffer code")
        return False
    
    print("Successfully generated:")
    print(f"  - {os.path.join(current_dir, 'audio_streaming_pb2.py')}")
    print(f"  - {os.path.join(current_dir, 'audio_streaming_pb2_grpc.py')}")
    
    return True

if __name__ == "__main__":
    generate_proto_code()