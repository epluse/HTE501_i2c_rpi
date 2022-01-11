# -*- coding: utf-8 -*-
"""
Example script reading measurement values from the HTE501 Sensor via I2c interface.

Copyright 2021 E+E Elektronik Ges.m.b.H.

Disclaimer:
This application example is non-binding and does not claim to be complete with regard
to configuration and equipment as well as all eventualities. The application example
is intended to provide assistance with the EE894 sensor module design-in and is provided "as is".
You yourself are responsible for the proper operation of the products described.
This application example does not release you from the obligation to handle the product safely
during application, installation, operation and maintenance. By using this application example,
you acknowledge that we cannot be held liable for any damage beyond the liability regulations
described.

We reserve the right to make changes to this application example at any time without notice.
In case of discrepancies between the suggestions in this application example and other E+E
publications, such as catalogues, the content of the other documentation takes precedence.
We assume no liability for the information contained in this document.
"""



import time
from hte501_i2c_library import HTE501


# Definition
CSV_DELIMETER = ","


HTE_501 = HTE501(0x40)

# read device identification
try:
    print("identification: " + ''.join('{:02x}'.format(x) for x in HTE_501.read_identification()))
    HTE_501.change_periodic_measurment_time(5000)
    print("periodic measurment time interval is: "+str(HTE_501.read_periodic_measurment_time()) +
          " s")
except Warning as exception:
    print("Exception: " + str(exception))

HTE_501.start_periodic_measurment()
# print csv header
print("temperature", CSV_DELIMETER,
      "relative humidity", CSV_DELIMETER,
      "dewpoint")

for i in range(300):

    try:
        if HTE_501.new_measurment_ready():
            temperature,humidity = HTE_501.get_periodic_measurment_temp_hum()
            dewpoint = HTE_501.get_dewpoint()

            print('%0.2f °C' % temperature, CSV_DELIMETER,
                  '%0.2f %%RH' % humidity, CSV_DELIMETER,
                  '%0.2f °C' % dewpoint)

    except Warning as exception:
        print("Exception: " + str(exception))

    finally:
        time.sleep(0.1)
HTE_501.end_periodic_measurment()
