# FPGA-Integrated Deep Learning Tolling System 

## Overview
This project demonstrates a **fully software-based FPGA-Integrated Deep Learning Tolling System**, combining **YOLOv5-based vehicle detection** with a **Verilog Finite State Machine (FSM)** simulation.  
The system intelligently detects vehicles, identifies tailgating behavior, and integrates UART-based AI-to-FPGA communication — all simulated in software without physical hardware.

---

##  Key Components

###  Deep Learning (Python)
- **Model:** YOLOv5 (pretrained on COCO dataset)
- **Scripts:**
  - `detect_vehicle_video.py` → Detects vehicles and tailgating in videos  
  - `ai_to_fpga_sim.py` → Simulates UART communication between AI and FPGA
- **Output:** Annotated video (`runs/detect/video_out/output.mp4`)  
  with per-frame detection summary in the console

###  FPGA Simulation (Verilog)
- **Modules:**
  - `toll_controller.v` → FSM controlling gate, alerts, and EV discount
  - `uart_rx_sim.v` → Reads UART data or simulates it from text input
  - `testbench.v` → Runs the simulation in ModelSim
- **Outputs:**
  - Simulated gate and alert signals
  - Waveform confirming FSM behavior
  - Optional UART file input (`uart_sim.txt`) for AI-driven simulation

---

##  Running the Project

###  Step 1 — Deep Learning Detection
#### 1. Place your video in:
yolov5/data/videos/sample.mp4
#### 2. From inside the `yolov5` folder run:
```bash
python detect_vehicle_video.py
```
#### 3.Result:

  Annotated output video saved to:
  ```bash
  runs/detect/video_out/output.mp4
  ```
  
  Console prints per-frame detection summaries:
  
  Frame 0001 | Vehicle Detected: True | Tailgating: False
### Step 2 — AI → FPGA Communication (Generate uart_sim.txt)

From inside the yolov5 folder, run:
```bash
python ai_to_fpga_sim.py
```

This script converts AI detections into 3-bit lines and writes them to:
```bash
yolov5/uart_sim_project/uart_sim.txt
```

Format (one line per frame):
100 → Vehicle detected (bit2),
010 → Tailgating (bit1),
001 → EV detected (bit0), etc
### 🧩 Step 3 — Verilog Simulation (ModelSim)

1. **Copy or `cd` into:**
```bash
yolov5/uart_sim_project/
```

2. **Compile Verilog modules:**
```bash
vlog uart_rx_sim.v
vlog toll_controller.v
vlog testbench.v
```
3. **Run the simulation GUI:**
```bash
vsim -gui work.testbench
```

4.**In ModelSim GUI or console, execute:**
```bash
run -all


(or run for a specific simulation time)

run 1ms
```

5.**Observe the following:**

Waveform signals showing UART data and FSM outputs:

uart_data → received from uart_sim.txt
gate_open
tailgate_alert
ev_discount

Console messages from uart_rx_sim confirming each line read from the file.
