import display
import utime
import leds
import buttons

class Rainbow(object):
    def __init__(self):
        pass

    def loop(self):
        sleep_ms = 20
        speed = 20
        offset = 0
        button = 0
        button_counter = 0
        brightness_pressed = False
        brightness_change = 0.5 * sleep_ms / 1000
        brightness = 1.
        while True:
            pressed = buttons.read(buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT)
            if pressed in [ buttons.BOTTOM_LEFT, buttons.BOTTOM_RIGHT ]:
                if button != pressed:
                    button = pressed
                    button_counter = 0

                button_counter = button_counter + 1
                button_time = button_counter * sleep_ms
                delta_v = (5 + (0 if button_counter < 1000 else 15*(button_counter-1000)/5000 if button_counter < 6000 else 15)) * sleep_ms / 1000

                if button == buttons.BOTTOM_LEFT:
                    speed = speed - delta_v
                else:
                    speed = speed + delta_v
            else:
                button = 0
            
            pressed = buttons.read(buttons.TOP_RIGHT)
            if pressed:
                brightness_pressed = True
                brightness += brightness_change
                if brightness > 1:
                    brightness = 1
                    brightness_change = -brightness_change
                elif brightness < 0:
                    brightness = 0
                    brightness_change = -brightness_change
            elif brightness_pressed:
                brightness_change = -brightness_change
                brightness_pressed = False

            leds.set_all_hsv([[(offset + 360*i/11) % 360, 1., brightness] for i in range(11)])
            offset = (offset + speed) % 360
            utime.sleep_ms(20)

with display.open() as disp:
    disp.clear().update()

rb = Rainbow()
rb.loop()
