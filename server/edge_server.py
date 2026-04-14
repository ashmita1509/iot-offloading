import socket
import json
import os

SOCKET_PATH = "/tmp/iot_anomaly.sock"
CRITICAL_THRESHOLD = 95.0

if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
server.listen(1)

print("Edge Node Active: Listening for IoT sensor data...")

while True:
    conn, addr = server.accept()
    try:
        data = conn.recv(8192).decode('utf-8')
        if data:
            sensor_readings = json.loads(data)
            print(f"\n[EDGE] Received {len(sensor_readings)} readings. Processing...")
            
	    # Anomaly Detection Logic (The Offloaded Task)
            anomalies = []
            for i, temp in enumerate(sensor_readings):
                if temp > CRITICAL_THRESHOLD:
                    anomalies.append({"reading_index": i, "temperature": round(temp, 2)})
            
            if len(anomalies) > 0:
                print(f"[EDGE] DANGER: {len(anomalies)} anomalies detected!")
                report = {"status": "CRITICAL", "message": "Initiate shutdown.", "anomalies_found": len(anomalies), "details": anomalies}
            else:
                print("[EDGE] Normal. Sending OK.")
                report = {"status": "OK", "message": "Normal parameters.", "anomalies_found": 0, "details": []}
            
	    # Send the result back to Container 1
            conn.sendall(json.dumps(report).encode('utf-8'))
	    # Exit after one complete cycle for easy demonstration
            break 
    finally:
        conn.close()
