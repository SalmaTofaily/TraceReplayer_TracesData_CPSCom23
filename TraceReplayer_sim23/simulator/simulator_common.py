power_measurement_resolution=6

def apply_power_measurement_resolution(n): 
    # no rounding, but panda rounds when it calculates
    return float(format(float(n), "." + str(power_measurement_resolution) + "f"))