# Solar Desktop

![Solar Sistem Desktop Demo](assets/showcase.gif)

Animates Windows desktop icons to orbit like Saturn's rings in multiple planets.

## Requirements

- Windows 10 or later
- If you have python installed, you have to install  `keyboard` package:
   ```bash
   pip install keyboard
   ```

## Usage

1. Right-click on desktop → View → Uncheck "Align icons to grid"

2. Change "False" to "True" in [`main.py`](main.py) line 90 to enable mouse speed control:
   ```python
   mouse_speed_control=True,
   ```

3. Adjust the planet center coordinates in [`main.py`](main.py) line 221:
   ```python
   center=(650, 400),
   ```

4. Adjust the orbit size in [`main.py`](main.py) line 222:
   ```python
   semiaxes=(400, 80),
   ```

5. Run the [`Test.bat`](Test.bat) file and repatt steps 2, 3 and 4 until you are satisfied with the result.

6. When you adjusted the values to your liking, run the [`Install.bat`](Install.bat) file.

## Controls

- Rotation speed changes based on mouse position
- Closer to the center = slower rotation
- Change within the planets with key F8

## Notes

- The [`Install.bat`](Install.bat) file creates a scheduled task to run the script at user login so tou have to ru it with
- Icons passing "behind" the planet are temporarily hidden
- I highly recommend taking a screenshot of your desktop before running the script because the icons won't be restored to their original positions when the script ends.

## License

This project is a derivative work based on: [Saturn-desktop](https://github.com/linkfy/saturn-desktop)

Original Author: Antonio Cuenca Garcia (Linkfy)  
License: MIT No Commercial License  

Original license text: [Original lisense](https://github.com/linkfy/saturn-desktop/blob/main/LICENSE)
