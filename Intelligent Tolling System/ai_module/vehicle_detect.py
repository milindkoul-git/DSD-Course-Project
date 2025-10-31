# vehicle_detect.py
# Detect vehicles using pretrained YOLOv5 model
# Works on image or video inputs
import os
import torch
import cv2
import sys
import warnings
warnings.filterwarnings("ignore")
# -------- CONFIG --------
SOURCE = "data/images/bus.jpg"   # change to your own image or video path
CONFIDENCE_THRESHOLD = 0.4
# ------------------------

# Load pretrained YOLOv5 model (CPU will be used automatically)
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True,trust_repo=True)
model.conf = CONFIDENCE_THRESHOLD

# Run inference
print(f"Running detection on: {SOURCE}")
results = model(SOURCE)

# Parse detections
df = results.pandas().xyxy[0]
print(df[["name", "confidence"]])

# Determine logical flags
vehicle_classes = ["car", "bus", "truck", "motorcycle"]
vehicle_detected = any(df["name"].isin(vehicle_classes))

# Placeholder logic for EV and tailgating
is_ev = False
tailgate_detected = False

# If multiple vehicles detected, flag possible tailgating
if len(df[df["name"].isin(vehicle_classes)]) > 1:
    tailgate_detected = True

# Display results
print("\n--- Detection Summary ---")
print(f"Vehicle Detected: {vehicle_detected}")
print(f"Possible Tailgating: {tailgate_detected}")
print(f"Is EV Vehicle: {is_ev} (placeholder logic)\n")

# Save output image(s)
# Save output image(s)
results.save()

# Optional: show image window (safely)
try:
    # results.save_dir isn't available in some versions — find the exp folder manually
    save_dir = str(results.files[0]).split("\\")[-1].split("/")[-1]
    latest_run = sorted(os.listdir("runs/detect"))[-1]
    output_path = os.path.join("runs/detect", latest_run, save_dir)
    
    img = cv2.imread(output_path)
    cv2.imshow("Detection Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
except Exception as e:
    print("Display skipped:", e)

