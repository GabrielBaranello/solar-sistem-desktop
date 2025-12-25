import time, math, keyboard 

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
    icons: tuple = tuple(()),
    radius: int,
    mouse_speed_control: String = "ctrl",
):
    cx, cy = center
    a, b = semiaxes
    planet_r2 = int(radius) * int(radius)

    # Base speeds
    speed_base = 0.3        # rad/s (legacy / fallback)
    speed_far = 0.6         # rad/s when mouse is far
    speed_min = 0.12        # rad/s near the planet radius
    speed_inside = 0.1     # rad/s when inside the planet
    slow_band = 220         # px outside the radius where slowdown applies

    fps = 60.0
    dt_target = 1.0 / fps

    # Where to hide icons (ListView client coordinates)
    HIDE_X, HIDE_Y = -5000, -5000

    t0 = time.perf_counter()
    last_t = t0
    phase = 0.0

    while True:
        count = get_item_count()
        if count <= 0:
            print("No icons")
            return

        now = time.perf_counter()
        dt = now - last_t
        last_t = now

        # --- Phase update ---
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
                # smoothstep
                tnorm = tnorm * tnorm * (3.0 - 2.0 * tnorm)
                cur_speed = speed_min + (speed_far - speed_min) * tnorm

            phase += cur_speed * dt
        elif mouse_speed_control == "none":
            # Original behaviour (time-based)
            t = now - t0
            phase = speed_base * t
        elif mouse_speed_control == "ctrl":
            t = now - t0
            phase = speed_base * t
            phase += keyboard.is_pressed("Ctrl") * 5
        else:
            print("Entrada de comportamiento invalida...")
            print("Calores validos: none, ctrl y dist.")
            print(f"Valor introducido: {mouse_speed_control}.")
            print("Modo constante iniciado")
            t = now - t0
            phase = speed_base * t
        # --- Icon placement ---
        for i in range(count):
            base = (2.0 * math.pi) * (i / count)
            ang = base + phase
            if not icons == null:
                it_has_to_display = get_icon_name(i) in icons
            else:
                it_has_to_display = True             x = cx + a * math.cos(ang)
            y = cy + b * math.sin(ang)

            # “Behind” the planet: back half of the orbit
            behind = math.sin(ang) < 0.0

            # Occlusion by the planet disk
            dx = x - cx
            dy = y - cy
            occluded = (dx * dx + dy * dy) <= planet_r2

            if behind and occluded:
                move_icon(i, HIDE_X, HIDE_Y)
            elif not it_has_to_display:
                move_icon(i, HIDE_X, HIDE_Y)
            else:
                move_icon(i, x, y)

        time.sleep(dt_target)

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

    animate_planet((cx, cy), (a, b), 300)
