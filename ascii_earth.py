import base64
from datetime import datetime, timezone, timedelta
import sys
import zlib

import numpy as np
import pygame
import math
import argparse

# ---------------------------------------------------------------------------
# World matrix: 180 rows (lat 89.5° --> -89.5°) x 360 columns (lon -179.5° --> 179.5°)
# 1 = land, 0 = water. Resolution of 1°. Compressed with zlib + base64.
# ---------------------------------------------------------------------------

WORLD_B64 = (
    "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"
    "+Q8XkoF0"
)


def load_world():
    # Decodes base64, decompresses zlib, and unpacks bits into a boolean grid
    clean_b64 = "".join(WORLD_B64.split())
    raw = zlib.decompress(base64.b64decode(clean_b64))
    bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8))[: 180 * 360]
    return bits.reshape(180, 360).astype(bool)


WORLD = load_world()

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

WIDTH, HEIGHT = 1280, 720
X_SEP, Y_SEP = 6, 12
COLS, ROWS = WIDTH // X_SEP, HEIGHT // Y_SEP

RADIUS = 290.0
CAM_DIST = 1100.0
FOCAL = 1100.0

CHARS = " .:;!i%&$8S@WM"
AMBIENT = 0.08

OCEAN_RGB = np.array([50, 110, 255])
LAND_RGB = np.array([70, 220, 100])


# ---------------------------------------------------------------------------
# Real time sun position (UTC and season)
# ---------------------------------------------------------------------------


def get_sun_vector():
    now = datetime.now(timezone.utc)
    utc_hours = now.hour + now.minute / 60.0 + now.second / 3600.0

    day_of_year = now.timetuple().tm_yday
    declination = -23.44 * math.cos(math.radians(360 * (day_of_year + 10) / 365.0))
    dec_rad = math.radians(declination)

    solar_lon = 15.0 * (12.0 - utc_hours)
    lon_rad = math.radians(solar_lon)

    sx = math.cos(dec_rad) * math.sin(lon_rad)
    sy = math.sin(dec_rad)
    sz = math.cos(dec_rad) * math.cos(lon_rad)

    light = np.array([sx, sy, sz])
    return light / np.linalg.norm(light)


def get_current_season():
    now = datetime.now(timezone.utc)
    doy = now.timetuple().tm_yday
    if 80 <= doy < 172:
        return "SPRING"
    elif 172 <= doy < 265:
        return "SUMMER"
    elif 265 <= doy < 355:
        return "AUTUMN"
    else:
        return "WINTER"


# ---------------------------------------------------------------------------
# Static geometry
# ---------------------------------------------------------------------------


def build_static_geometry():
    cols, rows = np.meshgrid(np.arange(COLS), np.arange(ROWS))
    px = cols * X_SEP + X_SEP / 2 - WIDTH / 2
    py = -(rows * Y_SEP + Y_SEP / 2 - HEIGHT / 2)

    d = np.stack([px, py, np.full_like(px, FOCAL, dtype=float)], axis=-1).astype(
        float
    )
    d /= np.linalg.norm(d, axis=-1, keepdims=True)

    d[..., 2] *= -1
    o = np.array([0.0, 0.0, CAM_DIST])
    b = d @ o
    c = o @ o - RADIUS**2
    disc = b * b - c
    hit = disc > 0
    t = -b - np.sqrt(np.where(hit, disc, 0.0))
    p = o + t[..., None] * d
    n = p / RADIUS

    return hit, n[hit], np.argwhere(hit)


HIT, N_HIT, CELLS = build_static_geometry()


# ---------------------------------------------------------------------------
# World data and lighting
# ---------------------------------------------------------------------------


def get_surface_data(spin, tilt):
    # Rotating surface normals every frame using tilt and spin given
    nx, ny, nz = N_HIT[:, 0], N_HIT[:, 1], N_HIT[:, 2]

    wy = np.cos(tilt) * ny + np.sin(tilt) * nz
    wz = -np.sin(tilt) * ny + np.cos(tilt) * nz
    wx = nx

    cos_s = np.cos(spin)
    sin_s = np.sin(spin)
    X = wx * cos_s - wz * sin_s
    Y = wy
    Z = wx * sin_s + wz * cos_s

    light = get_sun_vector()

    diffuse = np.clip(X * light[0] + Y * light[1] + Z * light[2], 0.0, 1.0)
    lum = AMBIENT + (1 - AMBIENT) * diffuse ** 0.85

    # Smoothing the lines
    lum_grid = np.zeros((ROWS, COLS), dtype=float)
    r_idx = CELLS[:, 0]
    c_idx = CELLS[:, 1]
    lum_grid[r_idx, c_idx] = lum

    # Horizontal smoothing
    lum_grid = (
        0.5 * lum_grid
        + 0.25 * np.roll(lum_grid, 1, axis=1)
        + 0.25 * np.roll(lum_grid, -1, axis=1)
    )
    lum = lum_grid[r_idx, c_idx]

    # Inverse trig to convert 3D points back to flat 2D map coordinates
    lat = np.degrees(np.arcsin(np.clip(Y, -1, 1)))
    lon = np.degrees(np.arctan2(wx, wz) - spin)

    row = np.clip((90.0 - lat).astype(int), 0, 179)
    col = ((lon + 180.0).astype(int)) % 360
    land = WORLD[row, col]

    return land, lum


# ---------------------------------------------------------------------------
# Paint
# ---------------------------------------------------------------------------

_glyph_cache = {}


def glyph(font, ch, rgb):
    key = (ch, rgb)
    s = _glyph_cache.get(key)
    if s is None:
        s = font.render(ch, True, rgb)
        _glyph_cache[key] = s
    return s


def draw_frame(surface, font, ui_font, spin, tilt, show_map, land_rgb, water_rgb):
    surface.fill((0, 0, 0))
    nchar = len(CHARS)

    land, lum = get_surface_data(spin, tilt)

    idx = (lum * (nchar - 0.01)).astype(int)

    if show_map:
        base = np.where(land[:, None], land_rgb, water_rgb)
    else:
        base = np.full((len(lum), 3), 255)

    shade = 0.30 + 0.70 * lum
    rgb = (base * shade[:, None]).astype(int)
    rgb_q = (rgb // 16) * 16 + 8

    for k in range(len(idx)):
        r, c = CELLS[k]
        surface.blit(
            glyph(font, CHARS[idx[k]], tuple(rgb_q[k])), (c * X_SEP, r * Y_SEP)
        )

  # ---------------------------------------------------------------------------
  # Header and UI
  # ---------------------------------------------------------------------------

    # Top Title
    title_surf = ui_font.render(
        "ASCII 3D WORLD MAP (LIVE SOLAR ILLUMINATION)", True, (255, 255, 255)
    )
    surface.blit(title_surf, (20, 15))

    # Top Clocks & Color-coded Season
    now_utc = datetime.now(timezone.utc)
    t_utc = now_utc.strftime("%H:%M UTC")
    t_ny = (now_utc + timedelta(hours=-4)).strftime("%H:%M NYC")
    t_lon = now_utc.strftime("%H:%M LON")
    t_tyo = (now_utc + timedelta(hours=9)).strftime("%H:%M TYO")

    season = get_current_season()
    season_colors = {
        "SPRING": (100, 255, 150),  # Green
        "SUMMER": (255, 220, 50),   # Yellow
        "AUTUMN": (255, 140, 70),   # Orange
        "WINTER": (100, 200, 255),  # Blue
    }
    s_col = season_colors.get(season, (255, 255, 255))

    # Render multi-colored info bar
    x_offset = 20
    y_pos = 38

    lbl_season = ui_font.render("SEASON: ", True, (160, 160, 160))
    surface.blit(lbl_season, (x_offset, y_pos))
    x_offset += lbl_season.get_width()

    val_season = ui_font.render(season, True, s_col)
    surface.blit(val_season, (x_offset, y_pos))
    x_offset += val_season.get_width()

    clocks_rest = ui_font.render(f"  |  {t_utc}  |  {t_lon}  |  {t_ny}  |  {t_tyo}", True, (100, 220, 255))
    surface.blit(clocks_rest, (x_offset, y_pos))

    # Bottom Controls HUD
    controls_surf = ui_font.render(
        "[M] Toggle Map  |  [SPACE] Pause  |  [UP/DOWN] Tilt Axis  |  [ESC] Exit",
        True,
        (150, 150, 150),
    )
    surface.blit(controls_surf, (20, HEIGHT - 28))


def main():
    
    parser = argparse.ArgumentParser(description="ASCII 3D WORLD MAP (LIVE SOLAR ILLUMINATION.")
    parser.add_argument("--speed", type=float, default=0.025, help="Globe rotation speed (by default: 0.025)")
    parser.add_argument("--no-map", action="store_true", help="Start without real earth texture")
    parser.add_argument("--land-color", type=str, default="70,220,100", help="Land color in R,G,B format (ex: 255,100,0)")
    parser.add_argument("--water-color", type=str, default="50,110,255", help="Water color in R,G,B format (ex: 0,50,150)")
    args = parser.parse_args()
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ASCII 3D WORLD MAP")

    font = pygame.font.SysFont(
        "couriernew,courier,dejavusansmono,monospace", 12, bold=True
    )
    ui_font = pygame.font.SysFont(
        "couriernew,courier,dejavusansmono,monospace", 13, bold=True
    )
    clock = pygame.time.Clock()

    land_rgb = np.array([int(x) for x in args.land_color.split(",")])
    water_rgb = np.array([int(x) for x in args.water_color.split(",")])
    spin, tilt = 0.0, 0.35
    show_map = not args.no_map
    paused, run = False, True

    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    run = False
                elif e.key == pygame.K_m:
                    show_map = not show_map
                elif e.key == pygame.K_SPACE:
                    paused = not paused
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            tilt = min(tilt + 0.02, 1.4)
        if keys[pygame.K_DOWN]:
            tilt = max(tilt - 0.02, -1.4)

        draw_frame(screen, font, ui_font, spin, tilt, show_map, land_rgb, water_rgb)
        pygame.display.flip()

        if not paused:
            spin += args.speed
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()