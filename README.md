# Distributed Clock Synchronization — Mini Project

A simple Streamlit simulation of clock synchronization using a Berkeley-style algorithm.

## Features
- Simulates 3–7 independent clock nodes.
- Lets you choose the coordinator.
- Lets you set each node's clock offset.
- Calculates average offset and per-node corrections.
- Shows before/after clock values and a comparison chart.
- Includes an explanation of the algorithm.

## Requirements
- Python 3.9 or newer
- Internet access for the first installation of the Python packages (if not already installed)

## Run on Windows
1. Extract the ZIP file.
2. Open Command Prompt in the extracted `clock_synchronization_project` folder.
3. Create a virtual environment (recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the application:

   ```bash
   streamlit run app.py
   ```

6. Open the local URL shown in the terminal, usually `http://localhost:8501`.

## How to demonstrate
1. Keep the default offsets and show that the clocks differ.
2. Click **Synchronize clocks**.
3. Explain that the coordinator calculates the average offset and sends each node a correction.
4. Change one node's offset to a large value and run the simulation again.
5. Explain that this is a simulation; it does not change the computer's real system clock.

## Algorithm
Let the clock offsets be `o1, o2, ..., on`.

Average offset:

`average = (o1 + o2 + ... + on) / n`

Correction for node `i`:

`correction_i = average - o_i`

Final offset for each simulated node:

`o_i + correction_i = average`

This is a simplified Berkeley-style simulation. It does not model network latency, clock drift, or unavailable nodes.
