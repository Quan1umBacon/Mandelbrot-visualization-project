# Mandelbrot & Julia Set Explorer

An interactive Python visualizer for the Mandelbrot Set and its associated Julia Sets. Two implementations available: a NumPy-vectorized version and a Numba-optimized version with ~40x speedup.

---

## Features

- **Interactive zoom** – left-click to zoom in
- **Live Julia Set** – Julia Set updates in real time as you move the cursor over the Mandelbrot Set (numba version)
- **Dynamic iteration scaling** – `max_iter` increases automatically with zoom depth
- **Color map cycling** – press `c` to cycle through color maps
- **Reset** – press `r` to return to the full default view

---

## Files

| File | Description |
|---|---|
| `mandelbrot_numba.py` | Numba-optimized version – recommended |
| `mandelbrot_numpy.py` | NumPy vectorized version – reference implementation |

---

## Requirements & Setup
```bash
pyenv local 3.11.3
python -m venv .venv
source .venv/Scripts/activate  # Git-Bash on Windows
python -m pip install --upgrade pip
pip install numpy matplotlib numba
python mandelbrot_numba.py
```

At startup: enable/disable Julia Set panel and set render resolution (600–1900 recommended).

---

## Controls

| Input | Action |
|---|---|
| Left click | Zoom into clicked point |
| Mouse move | Live Julia Set for point under cursor (if enabled) |
| `c` | Cycle color maps |
| `r` | Reset to full view |

---

## How It Works

For each point `c` in the complex plane, we iterate `z_(n+1) = z_n² + c` and count steps until `|z| > 2`. The iteration count determines pixel color. Points that never escape belong to the Mandelbrot Set.

Julia Sets use the same iteration with a fixed `c` and varying start values `z_0` – every point in the Mandelbrot Set corresponds to a unique Julia Set.

**NumPy version** uses boolean masking to process all points simultaneously. **Numba version** compiles the iteration loop to machine code and parallelizes across all CPU cores via `prange`, achieving ~40x speedup (~0.07s per render at 1000px width).

---

## Parameters

Defined at the top of each script:

| Parameter | Default | Description |
|---|---|---|
| `max_iter` | `600` | Base maximum iterations |
| `zoom_factor` | `4` | Zoom multiplier per click |
| `dynamic_iterations` | `'on'` | Scale `max_iter` with zoom depth |
| `julia_width` | `600` | Julia Set panel resolution |
| `throttle_ms` | `130` | Minimum ms between Julia Set renders |

---

## Backlog

- Smooth coloring
- Zoom history / undo
- Zoom video / animation
- Fractal dimension & entropy analysis