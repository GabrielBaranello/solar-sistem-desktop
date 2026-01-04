# Derived from:
# https://github.com/linkfy/saturn-desktop/blob/main/main.py
#
# Original Author: Antonio Cuenca Garcia (Linkfy)
# License: MIT No Commercial License
# Original license:
# https://github.com/linkfy/saturn-desktop/blob/main/LICENSE
#
# Modifications by Gabriel Guido Baranello (2025)

import time, math, threading, keyboard, ctypes, win32gui, win32con, win32api, os

from desktop_interact import (
    get_icon_name,
    move_icon,
    get_item_count,
    disable_snap_to_grid
)

from mouse_interact import (
    get_mouse_screen_pos,
)

# WALLPAPER
# ======================================================

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


def get_current_wallpaper() -> str:
    SPI_GETDESKWALLPAPER = 0x0073
    buffer = ctypes.create_unicode_buffer(260)

    ctypes.windll.user32.SystemParametersInfoW(
        SPI_GETDESKWALLPAPER,
        260,
        buffer,
        0
    )
    return buffer.value


# ======================================================
# ICON GROUPS (10 por página)
# ======================================================

def build_icon_groups(group_size: int = 10):
    groups = []
    current = []

    for i in range(get_item_count()):
        current.append(get_icon_name(i))
        if len(current) == group_size:
            groups.append(tuple(current))
            current = []

    if current:
        groups.append(tuple(current))

    return groups


# ======================================================
# SCENE CONTROLLER (F9)
# ======================================================

def scene_controller(scenes, state, stop_event):
    while not stop_event.is_set():
        keyboard.wait("f8")

        state["index"] = (state["index"] + 1) % len(scenes)
        scene = scenes[state["index"]]

        set_wallpaper(scene["wallpaper"])
        state["icons"] = scene["icons"]
        time.sleep(0.3)  # anti rebote


# ======================================================
# ANIMATION (10 slots fijos)
# ======================================================

def animate_planet(
    center: tuple[int, int],
    semiaxes: tuple[int, int],
    radius: int,
    state: dict,
    stop_event: threading.Event,
    mouse_speed_control: bool = False,
):
    cx, cy = center
    a, b = semiaxes
    planet_r2 = radius * radius

    VISIBLE_SLOTS = 10
    HIDE_X, HIDE_Y = -5000, -5000

    speed_base = 0.3
    speed_far = 0.6
    speed_min = 0.12
    speed_inside = 0.1
    slow_band = 220

    fps = 60.0
    dt_target = 1.0 / fps

    t0 = time.perf_counter()
    last_t = t0
    phase = 0.0

    while not stop_event.is_set() and not keyboard.is_pressed("esc"):
        now = time.perf_counter()
        dt = now - last_t
        last_t = now

        # ---- velocidad ----
        if mouse_speed_control == True:
            mx, my = get_mouse_screen_pos()
            dist = math.hypot(mx - cx, my - cy)

            if dist <= radius:
                cur_speed = speed_inside
            else:
                t = min(1.0, max(0.0, (dist - radius) / slow_band))
                t = t * t * (3 - 2 * t)
                cur_speed = speed_min + (speed_far - speed_min) * t

            phase += cur_speed * dt

        else:
            phase = speed_base * (now - t0)

        # ---- ocultar todo ----
        visible_names = set(state["icons"])
        for i in range(get_item_count()):
            if get_icon_name(i) not in visible_names:
                move_icon(i, HIDE_X, HIDE_Y)

        # ---- mostrar 10 slots fijos ----
        for slot in range(VISIBLE_SLOTS):
            if slot >= len(state["icons"]):
                break

            name = state["icons"][slot]

            # buscar índice real del icono
            for i in range(get_item_count()):
                if get_icon_name(i) == name:
                    icon_index = i
                    break
            else:
                continue

            ang = (2.0 * math.pi) * (slot / VISIBLE_SLOTS) + phase
            x = cx + a * math.cos(ang)
            y = cy + b * math.sin(ang)

            behind = math.sin(ang) < 0.0
            dx, dy = x - cx, y - cy
            occluded = (dx * dx + dy * dy) <= planet_r2

            if behind and occluded:
                move_icon(icon_index, HIDE_X, HIDE_Y)
            else:
                move_icon(icon_index, x, y)

        time.sleep(dt_target)


# ======================================================
# MAIN
# ======================================================

if __name__ == "__main__":
    if not disable_snap_to_grid():
        exit()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    WALLPAPERS = [
        os.path.join(BASE_DIR, "assets", "mercurio.jpg"),
        os.path.join(BASE_DIR, "assets", "venus.jpg"),
        os.path.join(BASE_DIR, "assets", "tierra.jpg"),
        os.path.join(BASE_DIR, "assets", "marte.jpg"),
        os.path.join(BASE_DIR, "assets", "jupiter.jpg"),
        os.path.join(BASE_DIR, "assets", "saturno.jpg"),
        os.path.join(BASE_DIR, "assets", "urano.jpg"),
        os.path.join(BASE_DIR, "assets", "neptuno.jpg")
    ]

    ICON_GROUPS = build_icon_groups(10)

    SCENES = []
    for i, icons in enumerate(ICON_GROUPS):
        SCENES.append({
            "wallpaper": WALLPAPERS[i % len(WALLPAPERS)],
            "icons": icons
        })

    state = {
        "index": 0,
        "icons": SCENES[0]["icons"]
    }

    stop_event = threading.Event()
    original_wallpaper = get_current_wallpaper()

    set_wallpaper(SCENES[0]["wallpaper"])

    try:
        t = threading.Thread(
            target=scene_controller,
            args=(SCENES, state, stop_event),
            daemon=True
        )
        t.start()

        animate_planet(
            center=(650, 400),
            semiaxes=(400, 80),
            radius=300,
            state=state,
            stop_event=stop_event
        )

    finally:
        stop_event.set()
        set_wallpaper(original_wallpaper)
