#  FPGA-Integrated Deep Learning Tolling Framework

A complete **software-simulated intelligent tolling system** combining **Deep Learning (YOLOv5)** for real-time vehicle and tailgating detection with an **FPGA-based Finite State Machine (FSM)** implemented in **Verilog HDL**.

This project demonstrates how AI-driven decision-making can be integrated into hardware-level control through **UART-based communication**, forming a foundation for future **smart highway infrastructure**.

---

##  Overview

Modern tolling systems often depend on manual or semi-automatic methods that lead to congestion and human error.  
This project bridges **AI-based visual detection** with **digital FSM logic** for fully automated, secure toll management — all simulated in software.

| Subsystem | Technology | Function |
|------------|-------------|-----------|
|  Deep Learning | YOLOv5 (PyTorch) | Detects vehicles, tailgating, and EVs in video |
| Hardware Simulation | Verilog (ModelSim) | Controls gate, lights, and alerts via FSM |
| Communication | UART Simulation | Transfers AI decisions to FSM |
| Integration Type | Software-only Co-Simulation | Python ↔ Verilog over text-based UART log |

---


---

## 🧰 How to Run

### 1️⃣ Run Vehicle Detection

Place your input video inside `data/videos/` and run:

```bash
python vehicle_detect_video.py


