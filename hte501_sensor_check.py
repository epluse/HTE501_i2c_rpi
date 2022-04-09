# -*- coding: utf-8 -*-
"""
Example script reading measurement values from the HTE501 Sensor via I2c interface.

Copyright 2021 E+E Elektronik Ges.m.b.H.

Disclaimer:
This application example is non-binding and does not claim to be complete with regard
to configuration and equipment as well as all eventualities. The application example
is intended to provide assistance with the HTE501 sensor module design-in and is provided "as is".
You yourself are responsible for the proper operation of the products described.
This application example does not release you from the obligation to handle the product safely
during application, installation, operation and maintenance. By using this application example,
you acknowledge that we cannot be held liable for any damage beyond the liability regulations
described.

We reserve the right to make changes to this application example at any time without notice.
In case of discrepancies between the suggestions in this application example and other E+E
publications, such as catalogues, the content of the other documentation takes precedence.
We assume no liability for the information contained in this document.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Attention!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
This programme should only be used if the conditions reamin the same,
otherwise incorrect results will be obtained.

"""




import time
import math
from hte501_i2c_library import HTE501


def variance_calculation(t_cc, rh_cc):
    """Calculate the the error propagation"""
    if((t_cc >= 15) and (t_cc <= 80)):
        delta_temp = 0.3
    if t_cc < 15:
        delta_temp = (0.2/55)*(15 - t_cc) + 0.3
    if t_cc > 85:
        delta_temp = (0.2/55)*(t_cc - 85) + 0.3
    delta_humi = (0.5/100*rh_cc) + 2.5
    derivative_temp = (pow(243.12,2)*pow(17.62,2))/(pow((math.log(rh_cc/100)*t_cc-243.12*17.62+math.log(rh_cc/100)*243.12),2))
    derivative_hum = (243.12*17.62*pow((243.12 + t_cc),2))/(pow(((t_cc+243.12)*math.log(rh_cc/100)-243.12*17.62),2)*rh_cc)
    result = derivative_temp * delta_temp + derivative_hum * delta_humi
    return result


HTE_501 = HTE501(0x40)

# read device identification
try:
    print("identification: " + ''.join('{:02x}'.format(x) for x in HTE_501.read_identification()))

except Warning as exception:
    print("Exception: " + str(exception))


HTE_501.change_heater_current(20)
HTE_501.heater_on()
try:
    temperature_heater_off,humidity_heater_off = HTE_501.get_single_shot_temp_hum()
    dewpoint_heater_off = HTE_501.get_dewpoint()

except Warning as exception:
    print("Exception: " + str(exception))
time.sleep(5)
i = 0
dewpoint_heater_on_old = 0
while i < 1:
    try:
        temperature_heater_on,humidity_heater_on = HTE_501.get_single_shot_temp_hum()
        dewpoint_heater_on = HTE_501.get_dewpoint()

    except Warning as exception:
        print("Exception: " + str(exception))
    if abs(dewpoint_heater_on_old-dewpoint_heater_on)<=0.02:
        i = 1
    else:
        dewpoint_heater_on_old = dewpoint_heater_on
    time.sleep(1)
delta = variance_calculation(temperature_heater_off,humidity_heater_off) + variance_calculation(temperature_heater_on,humidity_heater_on)
if abs(dewpoint_heater_on - dewpoint_heater_off) < delta:
    print("Sensor is okay")
else:
    print("Sensor is faulty")
HTE_501.heater_off()
