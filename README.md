# Creature Walking (Python)

A 2D physics simulation of a two-legged creature learning to walk. The creature
is built from rigid body segments (bones) connected by joints and spring-based
muscles, simulated with [Pymunk](https://www.pymunk.org/). A small neural network
policy is trained with a policy-gradient method to contract the muscles and move
the creature forward.

## Features

- **Physics-based creature** – a hip, two thighs, and two shins, joined with pin
  joints and angle limits. Muscles are damped springs whose rest length is
  controlled by the policy.
- **Custom mini engine** – `pyengine` provides the game loop, camera, debug
  overlay (toggle with `F3`), and simple UI helpers on top of Pygame.
- **Interactive scene** – click and drag body parts with the mouse to poke at
  the creature.
- **Reinforcement learning** – a two-hidden-layer MLP outputs muscle
  contractions; training uses Gaussian policy gradients with reward
  normalization, entropy regularization, and gradient clipping.
- **Checkpointing** – the best model is saved to `walking_model.pt`, and a
  reward plot is written to `rewards.png` during training.

## Project structure

```
main.py                      Entry point for the interactive scene
pyengine/                    Minimal game engine (loop, camera, UI, debug overlay)
src/
  objects/skeleton.py        Bone abstraction: joints, angle limits, muscles
  scenes/main_scene.py       Interactive pymunk scene with mouse dragging
  training/model.py          Policy network (MLP)
  training/sim.py            Headless walking simulation, observations, reward
  training/training.py       Training loop and reward plotting
  util/creatures.py          Builds the two-legged creature
  util/joints.py             Helpers for bones, joints, and muscles
walking_model.pt             Saved policy/optimizer checkpoint
rewards.png                  Reward history plot from training
```

## Requirements

- Python 3.10 (see `.python-version`)
- `pygame`
- `pymunk`
- `torch`
- `numpy`
- `matplotlib`

Create a virtual environment and install the dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install pygame pymunk torch numpy matplotlib
```

## Usage

### Interactive scene

```bash
python main.py
```

A window opens with the creature standing on the floor. Click and drag any body
part to pull it around. Press `F3` to toggle the debug overlay (FPS, delta time,
scene name, and custom debug lines).

### Training

```bash
python src/training/training.py
```

You will be asked whether to watch the training:

```
Would you like to watch? [y/N]
```

- Answer `y` to render each episode in a Pygame window (slower).
- Answer anything else (or press Enter) to train headlessly.

Training resumes automatically from `walking_model.pt` when the checkpoint
version matches; otherwise it starts from a fresh policy. A checkpoint is saved
whenever an episode beats the best reward so far, and `rewards.png` is updated
periodically and on exit (`Ctrl+C`).

## How it works

**Observation** – for every bone: angle and scaled angular velocity; plus the
root height and velocity, foot heights, foot offsets relative to the root, and
foot horizontal velocities.

**Action** – one value per muscle in `[-1, 1]`, where negative values lengthen
the muscle and positive values contract it (up to 25% of its rest length).

**Reward** – forward progress per step, a small survival bonus, and penalties
for poor posture and muscle effort. Falling ends the episode with an additional
penalty. Episodes are capped at 500 steps.

**Training** – the policy outputs the mean of a Gaussian distribution with fixed
standard deviation `0.2`. Actions are squashed with `tanh`, and the loss is the
negative log-probability weighted by normalized discounted returns, minus a
small entropy bonus. Gradients are clipped to a norm of `1.0`.

## Notes

- The simulation and checkpoint are CPU-friendly; `torch.load` uses
  `map_location="cpu"`.
- The `venv/` directory, `__pycache__/`, and compiled Python files are ignored
  by git.
