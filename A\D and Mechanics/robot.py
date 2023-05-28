#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep


class Robot:
    """
    -- TEMPLATE --
    This class provides logic for moving the sensor and scrolling the bar code cards
    """

    def sensor_step(self):
        """
        Moves the sensor one step to read the next bar code value
        """
        m = ev3.LargeMotor('outA')
        m.reset()
        m.stop_action = "brake"
        m.speed_sp = 120  # 120 0.3
        m.command = "run-forever"
        sleep(0.3)
        m.stop()

    def sensor_reset(self):
        """
        Resets the sensor position
        """
        m = ev3.LargeMotor('outA')
        m.reset()
        m.stop_action = "brake"
        m.speed_sp = -120
        m.command = "run-forever"
        sleep(3.45)
        m.stop()

    def scroll_step(self):
        """
        Moves the bar code card to the next line.
        """
        m = ev3.LargeMotor('outB')
        m.reset()
        m.stop_action = "brake"
        m.speed_sp = -30  # old page -30.4
        m.command = "run-forever"
        sleep(3.18)  # old page 3.0
        m.stop()

    def read_value(self) -> str:
        """
        Reads a single value, converts it and returns the binary expression
        :return: int
        """
        color_sensor = ev3.ColorSensor('in1')
        color_sensor.mode = "COL-REFLECT"
        color_value = color_sensor.reflected_light_intensity
        if color_value >= 45:
            return '0'
        else:
            return '1'

    def read_touch(self) -> int:
        """
        Reads a single value, 1 = pressed : 0 = not pressed
        :return: int
        """
        touch_sensor = ev3.TouchSensor('in2')
        touch_value: int = touch_sensor.value()
        return touch_value

    def raw_data(self) -> int:
        color_sensor = ev3.ColorSensor('in1')
        color_sensor.mode = "COL-REFLECT"
        color_value = color_sensor.reflected_light_intensity
        return color_value

    pass

    def text_to_speach(self, word):
        text_sound = ev3.Sound()
        text_sound.speak(word).wait()
