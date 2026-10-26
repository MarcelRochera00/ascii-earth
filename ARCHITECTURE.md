# Architecture

This file is a summary of the things I learned and the decisions I took whilst building this project. I made it to be able to come back and remember the methods, libraries and strategies I used for this project, so it's not required for you to read it.

To understand what this code does, I've decided to divide it the following sections:

## 1. World map storage method (base64, zlib, numpy)

To keep everything in a single script, the $180 \times 360$ world map is compressed and stored as a string using **Base64** and **Zlib**. The map is stored as a binary matrix: 1 represents land, 0 represents water.

1. **Base64 Decoding (`base64.b64decode`)**: Turns the ASCII characters back into raw binary bytes.
2. **Zlib Decompression (`zlib.decompress`)**: Unpacks the binary bytes back into the original dataset.
3. **NumPy Bit Unpacking (`np.frombuffer` & `np.unpackbits`)**: Reads the bytes as 8-bit unsigned integers and unpacks each byte into 8 individual bits.
4. **Reshaping (`.reshape`)**: Reshapes the array of bits into a 2D boolean grid ($180 \times 360$).

Never used base64 or zlib, so it was good to learn a new way to store data into code.

## 2. 3D Geometry and Reverse ray-tracing

How the engine projects a 3D mathematical sphere onto a 2D screen grid using ray-tracing and vector math using NumPy.

1. **Screen Grid (`np.meshgrid`)**: Generates a coordinate grid for all character cells, centering the coordinate system origin `(0, 0)` at the middle of the window.
2. **Ray Direction (`d`)**: Creates a normalized vector pointing from the virtual camera through each screen pixel into 3D space.
3. **Ray-Sphere Intersection (`disc`, `t`)**: Solves the ray-sphere intersection equation. If the discriminant is greater than zero, the ray hits the earth.
4. **Surface Normals (`n = p / RADIUS`)**: Calculates the normal vector pointing outward from the center of the sphere at each hit point (needed for lighting).

I already knew the theory of how ray-tracing works from a past C++ (OpenGL) University class, but I needed A.I help setting up the NumPy vector equations to make it run fast in Python without slow loops.

## 3. Real-time astronomy and Sun illumination

How the engine calculates the sun's position in 3D space dynamically based on the real-world's UTC time and seasons.

1. **UTC Time (`datetime.now`)**: Grabs the current global time and converts it into decimal hours.
2. **Seasonal Declination (`declination`)**: Approximates the earth's axial tilt ($ 23.44^\circ$) based on the day of the year to simulate seasons.
3. **Solar Longitude (`solar_lon`)**: Computes where the sun is directly overhead longitudinally, since earth rotates $15^\circ$ per hour.
4. **Sun Vector (`np.linalg.norm`)**: Converts these angles into a normalized 3D Cartesian vector $(sx, sy, sz)$.


## 4. Surface data, Rotation and Map sampling

How the static geometry is rotated, lit, and mapped to geographic coordinates every frame.

1. **Rotations (`tilt` and `spin`)**: Applies 3D rotation math to the surface normals to animate the Earth's axial tilt and rotation.
2. **Diffuse Lighting (`diffuse`)**: Computes the dot product between the rotated normals and the sun vector to get a shade value from darkness to bright sunlight.
3. **Lat/Lon Conversion (`lat`, `lon`)**: Uses inverse trigonometry to translate 3D points back into real-world geographic coordinates.
4. **Matrix Lookup (`WORLD[row, col]`)**: Queries the decompressed world matrix to check if a pixel points to land or water.

## 5. ASCII rendering and UI

How the lighting values are translated into visual characters and wrapped in a final interface.

1. **Character Density Ramp (`CHARS`)**: Maps continuous luminosity values to an ASCII string ordered by ink density (from space to `M`).
2. **Glyph Caching (`_glyph_cache`)**: Stores rendered font surfaces in memory to prevent performance drops.
3. **Multi-Colored UI & Timezones**: Dynamically calculates UTC, London, New York, and Tokyo times, and color-codes the current season (Spring, Summer, Autumn, Winter).
