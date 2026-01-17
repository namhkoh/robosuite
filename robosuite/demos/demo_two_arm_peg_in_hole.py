import argparse
import cv2
import numpy as np
import robosuite as suite
from robosuite.controllers import load_composite_controller_config

ROBOTS = ["Panda", "Sawyer", "IIWA", "Jaco", "Kinova3", "UR5e", "Baxter"]
CONTROLLERS = ["BASIC", "WHOLE_BODY_IK"]
CONFIGURATIONS = ["opposed", "parallel"]
CAMERAS = ["frontview", "agentview", "sideview", "birdview"]

def parse_args():
    parser = argparse.ArgumentParser(description="TwoArmPegInHole demo with video recording")
    parser.add_argument("--robot1", type=str, default="Panda", choices=ROBOTS)
    parser.add_argument("--robot2", type=str, default="Panda", choices=ROBOTS)
    parser.add_argument("--controller", type=str, default="BASIC", choices=CONTROLLERS)
    parser.add_argument("--config", type=str, default="opposed", choices=CONFIGURATIONS)
    parser.add_argument("--camera", type=str, default="frontview", choices=CAMERAS)
    parser.add_argument("--steps", type=int, default=500)
    parser.add_argument("--output", type=str, default="demo_two_arm_peg_in_hole.mp4")
    parser.add_argument("--reward_shaping", action="store_true", help="Enable dense reward shaping")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    print(f"Welcome to robosuite v{suite.__version__}!")
    print(f"Robots: {args.robot1}, {args.robot2}")
    print(f"Controller: {args.controller}")
    print(f"Configuration: {args.config}")
    print(f"Camera: {args.camera}")
    print(f"Reward shaping: {args.reward_shaping}")

    controller_config = load_composite_controller_config(controller=args.controller)

    env = suite.make(
        "TwoArmPegInHole",
        robots=[args.robot1, args.robot2],
        gripper_types=None,
        controller_configs=controller_config,
        env_configuration=args.config,
        has_renderer=False,
        has_offscreen_renderer=True,
        ignore_done=True,
        use_camera_obs=True,
        camera_names=args.camera,
        camera_heights=480,
        camera_widths=640,
        control_freq=20,
        horizon=args.steps,
        reward_shaping=args.reward_shaping,
    )
    env.reset()

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(args.output, fourcc, 20, (640, 480))

    print(f"Recording {args.steps} steps to {args.output}...")

    for i in range(args.steps):
        low, high = env.action_spec
        action = np.random.uniform(low, high)
        obs, reward, done, _ = env.step(action)

        frame = obs[f"{args.camera}_image"]
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.flip(frame, 0)
        video_writer.write(frame)

        if (i + 1) % 100 == 0:
            print(f"Step {i + 1}/{args.steps}, reward: {reward:.4f}")

    video_writer.release()
    env.close()
    print(f"Video saved to {args.output}")
