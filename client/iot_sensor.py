import socket
import json
import random
import time

SOCKET_PATH = "/tmp/iot_anomaly.sock"

# 1. Generate Simulated Data (100 readings)
print("[SENSOR] Booting up and collecting data...")
sensor_data = [random.uniform(60.0, 80.0) for _ in range(97)]
sensor_data.extend([98.4, 102.1, 96.5]) 
random.shuffle(sensor_data)

client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
# Give the server a moment to ensure it is listening
time.sleep(2) 

try:
    print(f"[SENSOR] Connecting to Edge Node. Offloading {len(sensor_data)} parameters...")
    client.connect(SOCKET_PATH)
    
    # Start offloading timer
    start_time = time.time()
    
    # Send the raw data
    client.sendall(json.dumps(sensor_data).encode('utf-8'))

    # Wait for the ultimate decision from the edge
    response = client.recv(8192).decode('utf-8')
    
    # End offloading timer
    end_time = time.time()
    offloading_time = end_time - start_time
    
    edge_report = json.loads(response)
    
    # Display the results
    print("\n--- Edge Processing Report Received ---")
    print(f"STATUS:  {edge_report['status']}")
    print(f"MESSAGE: {edge_report['message']}")
    print(f"OFFLOADING TIME: {offloading_time:.5f} seconds") # This is what you need for the report!
    
    if edge_report['anomalies_found'] > 0:
        print(f"Total Anomalies: {edge_report['anomalies_found']}")
        for anomaly in edge_report['details']:
            print(f" -> Index {anomaly['reading_index']} spiked to {anomaly['temperature']}°C")

finally:
    client.close()
