# Mandelbrot & Julia Set Explorer

An interactive Python visualizer for the Mandelbrot Set and its associated Julia Sets, built with NumPy and Matplotlib.

---

## Features

- **Interactive zoom** – left-click to zoom in
- **Julia Set rendering** – right-click any point to render its Julia Set side by side
- **Dynamic iteration scaling** – `max_iter` increases automatically with zoom depth
- **Color map cycling** – press `c` to cycle through color maps
- **Reset** – press `r` to return to the full default view

---

## Requirements & Setup


For WindowsOS: Open Git-Bash CLI (opt: as an administrator)
```bash
pyenv local 3.11.3
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
pip install numpy matplotlib
```

At startup: enable/disable Julia Set panel and set render resolution (600–1200 recommended).

---

## Controls

| Input | Action |
|---|---|
| Left click | Zoom into clicked point |
| Right click | Render Julia Set for clicked point |
| `c` | Cycle color maps |
| `r` | Reset to full view |

---

## How It Works

For each point `c` in the complex plane, we iterate `z_(n+1) = z_n² + c` and count steps until `|z| > 2`. The iteration count determines pixel color. Points that never escape belong to the Mandelbrot Set.

Julia Sets use the same iteration with a fixed `c` and varying start values `z_0` – every point in the Mandelbrot Set corresponds to a unique Julia Set.

Both computations use NumPy boolean masking to process all ~480,000 points simultaneously rather than looping over each individually.

---

## Parameters

Defined at the top of `mandelbrot.py`:

| Parameter | Default | Description |
|---|---|---|
| `max_iter` | `400` | Base maximum iterations |
| `zoom_factor` | `6` | Zoom multiplier per click |
| `dynamic_iterations` | `'on'` | Scale `max_iter` with zoom depth |

---

## Backlog

- Smooth coloring
- Zoom history / undo
- Zoom video / animation
- Performance optimization with Numba
- Fractal dimension & entropy analysis