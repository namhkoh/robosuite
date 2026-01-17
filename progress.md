# Robosuite Setup and Dual Arm Simulation Guide

## 1. Create Conda Environment

```bash
conda create -n robosuite python=3.10 -y
conda activate robosuite
```

## 2. Install Robosuite

```bash
cd /ext_hdd2/nhkoh/robosuite
pip install -e .
```

This installs all dependencies from `setup.py`:
- numpy, scipy, numba
- mujoco>=3.3.0
- opencv-python, Pillow
- pynput, termcolor, tqdm, pytest

## 3. Install OSMesa for Headless Rendering

```bash
conda install -c conda-forge mesalib -y
```

## 4. Run Dual Arm Peg-In-Hole Simulation

Basic run with default settings (two Panda robots, opposed configuration):

```bash
MUJOCO_GL=osmesa python robosuite/demos/demo_two_arm_peg_in_hole.py
```

### Available Options

| Argument | Default | Options |
|----------|---------|---------|
| `--robot1` | Panda | Panda, Sawyer, IIWA, Jaco, Kinova3, UR5e, Baxter |
| `--robot2` | Panda | same as above |
| `--controller` | BASIC | BASIC, WHOLE_BODY_IK |
| `--config` | opposed | opposed, parallel |
| `--camera` | frontview | frontview, agentview, sideview, birdview |
| `--steps` | 500 | any integer |
| `--output` | demo_two_arm_peg_in_hole.mp4 | any path |
| `--reward_shaping` | False | flag to enable dense rewards |

### Example Commands

```bash
# Two Sawyer robots in parallel configuration
MUJOCO_GL=osmesa python robosuite/demos/demo_two_arm_peg_in_hole.py \
  --robot1 Sawyer --robot2 Sawyer --config parallel

# With reward shaping and different camera
MUJOCO_GL=osmesa python robosuite/demos/demo_two_arm_peg_in_hole.py \
  --reward_shaping --camera agentview

# Longer simulation with custom output
MUJOCO_GL=osmesa python robosuite/demos/demo_two_arm_peg_in_hole.py \
  --steps 1000 --output my_simulation.mp4
```

## 5. Output

The script records video to the specified output file (default: `demo_two_arm_peg_in_hole.mp4`).

## Notes

- `MUJOCO_GL=osmesa` enables software rendering for headless servers
- If you have GPU access, try `MUJOCO_GL=egl` instead for faster rendering
- The simulation uses random actions by default (not a trained policy)
- Enable `--reward_shaping` to see non-zero intermediate rewards
