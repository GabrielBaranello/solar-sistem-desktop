import time, math, keyboard, ctypes
import ctypes.wintypes as wt

# Utility functions to play with
from desktop_interact import (
    get_icon_name,
    move_first_icon,
    get_item_count,
    move_icon,
    disable_snap_to_grid
)
from mouse_interact import (
    get_mouse_pos_relative_to_icon,
    get_mouse_screen_pos,
    get_desktop_listview,
)


def animate_planet(
    center: tuple[int, int],
    semiaxes: tuple[int, int],
    radius: int,
    image: str,
    icons: tuple = (),
    mouse_speed_control: str = "ctrl",
):
    cx, cy = center
    a, b = semiaxes
    planet_r2 = radius * radius
    set_wallpaper(image)

    # Velocidades
    speed_base = 0.3
    speed_far = 0.6
    speed_min = 0.12
    speed_inside = 0.1
    slow_band = 220

    fps = 60.0
    dt_target = 1.0 / fps

    # Posición para ocultar íconos
    HIDE_X, HIDE_Y = -5000, -5000

    t0 = time.perf_counter()
    last_t = t0
    phase = 0.0

    while True:
        if keyboard.is_pressed("ctrl+q"):
            break
        count = get_item_count()
        if count <= 0:
            print("No icons")
            return

        now = time.perf_counter()
        dt = now - last_t
        last_t = now

        # --- Control de velocidad ---
        if mouse_speed_control == "dist":
            mx, my = get_mouse_screen_pos()
            dxm = mx - cx
            dym = my - cy
            dist = math.hypot(dxm, dym)

            if dist <= radius:
                cur_speed = speed_inside
            else:
                tnorm = (dist - radius) / slow_band
                tnorm = max(0.0, min(1.0, tnorm))
                tnorm = tnorm * tnorm * (3.0 - 2.0 * tnorm)  # smoothstep
                cur_speed = speed_min + (speed_far - speed_min) * tnorm

            phase += cur_speed * dt

        elif mouse_speed_control == "none":
            phase = speed_base * (now - t0)

        elif mouse_speed_control == "ctrl":
            phase = speed_base * (now - t0)
            if keyboard.is_pressed("ctrl"):
                phase += 5 * dt

        else:
            print("Entrada de comportamiento invalida")
            print("Valores validos: none, ctrl, dist")
            phase = speed_base * (now - t0)

        # --- Posicionamiento de íconos ---
        for i in range(count):
            base = (2.0 * math.pi) * (i / count)
            ang = base + phase

            if icons:
                it_has_to_display = get_icon_name(i) in icons
            else:
                it_has_to_display = True

            x = cx + a * math.cos(ang)
            y = cy + b * math.sin(ang)

            behind = math.sin(ang) < 0.0

            dx = x - cx
            dy = y - cy
            occluded = (dx * dx + dy * dy) <= planet_r2

            if (behind and occluded) or not it_has_to_display:
                move_icon(i, HIDE_X, HIDE_Y)
            else:
                move_icon(i, x, y)

        time.sleep(dt_target)

def get_current_wallpaper() -> str:
    SPI_GETDESKWALLPAPER = 0x0073
    MAX_PATH = 260

    buffer = ctypes.create_unicode_buffer(MAX_PATH)

    ctypes.windll.user32.SystemParametersInfoW(
        SPI_GETDESKWALLPAPER,
        MAX_PATH,
        buffer,
        0
    )
    return buffer.value

def set_wallpaper(image_path: str):
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 1
    SPIF_SENDCHANGE = 2

    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        image_path,
        SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    )

if __name__ == "__main__":
    ok = disable_snap_to_grid()
    if not ok:
        print("Error disabling snap to grid")
        exit()

    # Ring center (adjust to where the "planet" is in your wallpaper)
    cx, cy = 920, 500

    # Ring: circle or ellipse (ellipse recommended for a ring-like look)
    a = 420   # horizontal semiaxis (px)
    b = 100   # vertical semiaxis   (px)
    
    wall_paper = get_current_wallpaper() # geting wallpaper to change to it at the end of the script 
    try:
        while True: 
            if planet == 1:
                animate_planet((cx, cy), (a, b), 300)
            elif planet == 2: 
                animate_planet((cx, cy), (a, b), 300)
            elif planet == 3: 
                animate_planet((cx, cy), (a, b), 300)
            elif planet == 4: 
                animate_planet((cx, cy), (a, b), 300)
            elif planet == 5: 
                animate_planet((cx, cy), (a, b), 300)
            elif planet == 6:
                animate_planet((cx, cy), (a, b), 300)
            elif planet == 7: 
                animate_planet((cx, cy), (a, b), 300)
            else:
                planet = 1
            if keyboard.is_pressed("ctrl+q"):
                planet += 1
                time.sleep(500)
    finally:
        set_wallpaper(wall_paper)
        
