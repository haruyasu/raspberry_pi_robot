import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from gpiozero import Motor
from gpiozero.pins.pigpio import PiGPIOFactory

PIN_AIN1 = 19
PIN_AIN2 = 26
PIN_BIN1 = 17
PIN_BIN2 = 27


class ListenerNode(Node):
    def __init__(self):
        super().__init__("joy_sub_raspi_move")
        self.create_subscription(Joy, "joy", self.callback, 10)
        factory = PiGPIOFactory()

        self.motor_back = Motor(
            forward=PIN_AIN2,
            backward=PIN_AIN1,
            pin_factory=factory
        )

        self.motor_front = Motor(
            forward=PIN_BIN1,
            backward=PIN_BIN2,
            pin_factory=factory
        )

    def callback(self, joy_msg):
        axes_0 = float(joy_msg.axes[0])
        axes_1 = float(joy_msg.axes[1])
        axes_3 = float(joy_msg.axes[3])
        axes_4 = float(joy_msg.axes[4])

        if axes_1 > 0:
            self.motor_back.value = 1.0
            if axes_3 > 0:
                self.motor_front.value = -1.0
            elif axes_3 < 0:
                self.motor_front.value = 1.0
            else:
                self.motor_front.value = 0.0
        elif axes_1 < 0:
            self.motor_back.value = -1.0
            if axes_3 > 0:
                self.motor_front.value = -1.0
            elif axes_3 < 0:
                self.motor_front.value = 1.0
            else:
                self.motor_front.value = 0.0
        else:
            self.motor_back.value = 0.0

        # if axes_0 == 0 and axes_1 == 1:
        #     print('front')
        #     self.motor_back.value = 1.0
        #     self.motor_front.value = 0.0
        # elif axes_0 < 0 and axes_1 > 0:
        #     print('front right')
        #     self.motor_back.value = 1.0
        #     self.motor_front.value = 1.0
        # elif axes_0 > 0 and axes_1 > 0:
        #     print('front left')
        #     self.motor_back.value = 1.0
        #     self.motor_front.value = -1.0
        # elif axes_0 == -1 and axes_1 == 0:
        #     print('right')
        #     self.motor_back.value = 1.0
        #     self.motor_front.value = 1.0
        # elif axes_0 == 1 and axes_1 == 0:
        #     print('left')
        #     self.motor_back.value = 1.0
        #     self.motor_front.value = -1.0
        # elif axes_0 < 0 and axes_1 < 0:
        #     print('back right')
        #     self.motor_back.value = -1.0
        #     self.motor_front.value = 1.0
        # elif axes_0 > 0 and axes_1 < 0:
        #     print('back left')
        #     self.motor_back.value = -1.0
        #     self.motor_front.value = -1.0
        # elif axes_0 == 0 and axes_1 == -1:
        #     print('back')
        #     self.motor_back.value = -1.0
        #     self.motor_front.value = 0.0
        # else:
        #     self.motor_back.value = 0
        #     self.motor_front.value = 0


def main():
    rclpy.init()
    node = ListenerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('Cancel')
    rclpy.shutdown()
    print('End')
