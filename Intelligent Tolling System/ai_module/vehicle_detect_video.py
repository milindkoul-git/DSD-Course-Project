"""
vehicle_detect_video.py
-----------------------
Performs vehicle detection, tailgating detection, and video annotation using a pre-trained YOLOv5 model.
The script processes each frame of a video (or webcam stream), identifies vehicles,
detects tailgating based on bounding box distance, and saves the annotated output video.

Author: Milind Koul
Project: FPGA-Integrated Deep Learning Tolling System
Date: October 2025
"""

import torch
import cv2
import os
import warnings
warnings.filterwarnings("ignore")  # Suppress PyTorch and OpenCV warnings

# Optional: run UART/FPGA linkage at the end
import subprocess  

# -------- CONFIGURATION --------
SOURCE = "data/videos/sample.mp4"   # Path to input video, or use "0" for webcam
CONFIDENCE_THRESHOLD = 0.4          # Minimum confidence for detection
OUTPUT_DIR = "runs/detect/video_out"
# --------------------------------

# Load YOLOv5 pretrained model from Ultralytics Hub
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True, trust_repo=True)
model.conf = CONFIDENCE_THRESHOLD

print(f"\n🚗 Running video detection on: {SOURCE}\n")

# Open video capture source
cap = cv2.VideoCapture(SOURCE if SOURCE != "0" else 0)
if not cap.isOpened():
    print("❌ Error: Could not open video source.")
    exit()

# Get video properties for output file
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Prepare output directory and writer
os.makedirs(OUTPUT_DIR, exist_ok=True)
output_path = os.path.join(OUTPUT_DIR, "output.mp4")
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_path, fourcc, fps if fps > 0 else 20.0, (width, height))

frame_count = 0
vehicle_classes = ["car", "bus", "truck", "motorcycle"]

# -------------------- MAIN LOOP --------------------
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame_count += 1

    # Perform YOLOv5 object detection
    results = model(frame)
    df = results.pandas().xyxy[0]

    # --- VEHICLE DETECTION ---
    vehicle_detected = any(df["name"].isin(vehicle_classes))

    # --- TAILGATING DETECTION ---
    tailgate_detected = False
    vehicle_boxes = df[df["name"].isin(vehicle_classes)][["xmin", "xmax"]].values

    for i in range(len(vehicle_boxes)):
        for j in range(i + 1, len(vehicle_boxes)):
            dist = abs(vehicle_boxes[i][0] - vehicle_boxes[j][0])
            avg_width = (vehicle_boxes[i][1] - vehicle_boxes[i][0] +
                         vehicle_boxes[j][1] - vehicle_boxes[j][0]) / 2
            if dist < avg_width * 0.5:  # Vehicles closer than half average width → tailgating
                tailgate_detected = True

    # Print summary for each frame
    print(f"Frame {frame_count:04d} | Vehicle Detected: {vehicle_detected} | Tailgating: {tailgate_detected}")

    # Annotate and write frame
    annotated = results.render()[0]
    annotated_bgr = cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR)
    out.write(annotated_bgr)

# -------------------- CLEANUP --------------------
cap.release()
out.release()
print(f"\n✅ Process complete! Annotated video saved to: {output_path}")
