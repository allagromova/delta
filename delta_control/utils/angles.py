from math import atan, cos, sin, sqrt
from typing import Optional, Tuple

import utils.const as const


def calculate_forward(theta1, theta2, theta3) -> Optional[Tuple[float, float, float]]:
    """
    Прямая кинематика.
    :return: (x0, y0, z0)
    """
    t = (const.f - const.e) * const.tan30 / 2
    dtr = const.pi / 180.0

    theta1 *= dtr
    theta2 *= dtr
    theta3 *= dtr

    y1 = -(t + const.rf * cos(theta1))
    z1 = -const.rf * sin(theta1)

    y2 = (t + const.rf * cos(theta2)) * const.sin30
    x2 = y2 * const.tan60
    z2 = -const.rf * sin(theta2)

    y3 = (t + const.rf * cos(theta3)) * const.sin30
    x3 = -y3 * const.tan60
    z3 = -const.rf * sin(theta3)

    dnm = (y2 - y1) * x3 - (y3 - y1) * x2

    w1 = y1 * y1 + z1 * z1
    w2 = x2 * x2 + y2 * y2 + z2 * z2
    w3 = x3 * x3 + y3 * y3 + z3 * z3

    # x = (a1 * z + b1) / dnm
    a1 = (z2 - z1) * (y3 - y1) - (z3 - z1) * (y2 - y1)
    b1 = -((w2 - w1) * (y3 - y1) - (w3 - w1) * (y2 - y1)) / 2.0

    # y = (a2 * z + b2) / dnm
    a2 = -(z2 - z1) * x3 + (z3 - z1) * x2
    b2 = ((w2 - w1) * x3 - (w3 - w1) * x2) / 2.0

    # a * z^2 + b * z + c = 0
    a = a1 * a1 + a2 * a2 + dnm * dnm
    b = 2 * (a1 * b1 + a2 * (b2 - y1 * dnm) - z1 * dnm * dnm)
    c = (b2 - y1 * dnm) * (b2 - y1 * dnm) + b1 * b1 + dnm * dnm * (z1 * z1 - const.re * const.re)

    # дискриминант
    d = b * b - 4.0 * a * c
    if d < 0:
        return  # несуществующая позиция

    z0 = -0.5 * (b + sqrt(d)) / a
    x0 = (a1 * z0 + b1) / dnm
    y0 = (a2 * z0 + b2) / dnm
    return x0, y0, z0


def calculate_angle_yz(x0, y0, z0) -> Optional[int]:
    """
    Обратная кинематика.
    Вспомогательная функция, расчет угла theta1 (в плоскости YZ).
    :return: theta1
    """
    y1 = -0.5 * 0.57735 * const.f  # f / 2 * tg 30
    y0 -= 0.5 * 0.57735 * const.e  # сдвигаем центр к краю
    # z = a + b * y
    a = (x0 * x0 + y0 * y0 + z0 * z0 + const.rf * const.rf - const.re * const.re - y1 * y1) / (2 * z0)
    b = (y1 - y0) / z0
    # дискриминант
    d = -(a + b * y1) * (a + b * y1) + const.rf * (b * b * const.rf + const.rf)
    if d < 0:
        return  # несуществующая точка
    yj = (y1 - a*b - sqrt(d))/(b*b + 1)  # выбираем внешнюю точку
    zj = a + b*yj
    if yj > 0:
        return 180.0 * atan(-zj / (y1 - yj)) / const.pi + 180.0
    return 180.0 * atan(-zj / (y1 - yj)) / const.pi + 0.0


def calculate_inverse(x0, y0, z0) -> Optional[Tuple[float, float, float]]:
    """
    Обратная кинематика.
    :return: (theta1, theta2, theta3)
    """
    theta1 = calculate_angle_yz(x0, y0, z0)
    theta2, theta3 = 0, 0
    if theta1 is not None:
        # rotate coords to +120 deg
        theta2 = calculate_angle_yz(x0 * const.cos120 + y0 * const.sin120, y0 * const.cos120 - x0 * const.sin120, z0)
    elif theta2 is not None:
        # rotate coords to -120 deg
        theta3 = calculate_angle_yz(x0 * const.cos120 - y0 * const.sin120, y0 * const.cos120 + x0 * const.sin120, z0)
    else:
        return
    return theta1, theta2, theta3
