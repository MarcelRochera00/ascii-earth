# ASCII Earth: An ASCII 3D World Map with live solar illumination

An ASCII-rendered 3D rotating globe built in Python using Pygame and NumPy. It features real-time solar tracking, seasonal tilt variations, land/ocean shading, and live world clocks. Make sure to check out the Typescript version in my profile! ([ascii-earth-web](https://github.com/MarcelRochera00/ascii-earth-web))

![ASCII Globe Demo](globe_rotation.gif)

---
## Features
 
- **Real-time solar illumination**: the sun's position is derived from the current UTC time and the day of the year.
- **Seasonal tilt**: the Earth's 23.44° axial tilt is simulated, so summer and winter change how the globe is lit.
- **Live world clocks**: UTC, London, New York and Tokyo, with the current season colour-coded.
- **Single-file project**: the 180×360 world map is embedded in the script as compressed Base64 (zlib), so there are no image or data files to download.
- **Fast rendering**: the ray-sphere intersection and lighting are fully vectorised with NumPy, with no per-pixel Python loops.

---

## Customization Parameters (CLI)

You can customize the globe directly from your terminal using command-line arguments:

| Parameter | Description | Default | Example |
| :--- | :--- | :--- | :--- |
| `--speed` | Controls the rotation speed of the globe. | `0.025` | `python ascii_earth.py --speed 0.08` |
| `--no-map` | Starts without land/ocean textures (lighting only). | `False` | `python ascii_earth.py --no-map` |
| `--land-color` | Custom land color in RGB format (`R,G,B`). | `70,220,100` | `python ascii_earth.py --land-color "220,80,50"` |
| `--water-color` | Custom ocean color in RGB format (`R,G,B`). | `50,110,255` | `python ascii_earth.py --water-color "0,20,80"` |

## How it works
 
Every frame a ray is cast from a virtual camera through every character cell and tested against a sphere. Where it hits, the surface normal is rotated by the Earth's tilt and spin, compared against the sun vector to get a brightness value, and converted back to latitude and longitude to look up whether that point is land or water. Brightness is then mapped to an ASCII character.
 
The full write-up of the techniques and decisions (Base64 + zlib map storage, reverse ray-tracing, solar declination, glyph caching) is in [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Limitations and ideas
 
- The map resolution is 180×360, so small islands and coastlines are approximate.
- No clouds, city lights or terrain relief yet.
- The solar position uses a simple declination approximation, not a full astronomical model.
- Possible next steps: configurable time zones, a time-travel mode to travel through the year, and a toggle night-side city lights or clouds layer.

---

## Requirements
Make sure you have Python 3 and the required packages installed:

```bash
pip install pygame numpy
```

## Run it yourself

```bash
python ascii_earth.py
```
