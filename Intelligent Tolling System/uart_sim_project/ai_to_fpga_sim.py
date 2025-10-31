# ai_to_fpga_sim.py
# Run YOLO detection (image/video) and write simulated UART messages to uart_sim.txt
import warnings
warnings.filterwarnings("ignore")
import torch, os, time, cv2

# CONFIG - change SOURCE to your video or 0 for webcam
SOURCE = "../data/videos/sample.mp4"   # relative to this folder (yolov5/..)
CONFIDENCE_THRESHOLD = 0.4
OUTFILE = "uart_sim.txt"

# load model (uses cached weights)
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True, trust_repo=True)
model.conf = CONFIDENCE_THRESHOLD

# vehicle classes
vehicle_classes = ["car", "bus", "truck", "motorcycle"]

# open video
cap = cv2.VideoCapture(SOURCE)
if not cap.isOpened():
    print("Warning: Cannot open video source:", SOURCE)
    # If you want to run on a single image, you can do single inference below.
    # For now exit.
    exit()

# open output file
f = open(OUTFILE, "w")

frame = 0
while True:
    ret, img = cap.read()
    if not ret:
        break
    frame += 1
    results = model(img)
    df = results.pandas().xyxy[0]

    # vehicle detection
    vehicle_detected = int(any(df["name"].isin(vehicle_classes)))

    # tailgating: refined approach - bounding boxes close horizontally
    tailgate = 0
    vehicle_boxes = df[df["name"].isin(vehicle_classes)][["xmin", "xmax"]].values
    for i in range(len(vehicle_boxes)):
        for j in range(i+1, len(vehicle_boxes)):
            dist = abs(vehicle_boxes[i][0] - vehicle_boxes[j][0])
            avg_width = (vehicle_boxes[i][1]-vehicle_boxes[i][0] + vehicle_boxes[j][1]-vehicle_boxes[j][0]) / 2.0
            if avg_width > 0 and dist < avg_width * 0.5:
                tailgate = 1

    # is_ev (placeholder) - set 0 for now
    is_ev = 0

    # write ascii line for UART simulation: e.g. "101\n"
    line = f"{vehicle_detected}{tailgate}{is_ev}\n"
    f.write(line)
    f.flush()

    # optionally print to console
    print(f"Frame {frame:04d} | Sent: {line.strip()}")

    # small delay to simulate real-time (optional)
    # time.sleep(0.01)

f.close()
cap.release()
print("Done. uart file written to:", OUTFILE)
