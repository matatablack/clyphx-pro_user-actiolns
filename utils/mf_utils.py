def color(enc, val):
    return "MIDI CC 2 %s %s;" % (int(enc) - 1, val)


def rgb_brightness(enc, val):
    return "MIDI CC 6 %s %s;" % (int(enc) - 1, _apply_percentage(val, [17, 47]))


def rgb_pulse(enc, val):
    return "MIDI CC 6 %s %s;" % (int(enc) - 1, val + 8)


def rgb_strobe(enc, val):
    return "MIDI CC 6 %s %s;" % (int(enc) - 1, val)


def rgb_animation_off(enc):
    return "MIDI CC 6 %s %s;" % (int(enc) - 1, "0")


def ind_brightness(enc, val):
    return "MIDI CC 3 %s %s;" % (int(enc) - 1, _apply_percentage(val, [65, 95]))


def ind_pulse(enc, val):
    return "MIDI CC 3 %s %s;" % (int(enc) - 1, 56 + val)


def ind_strobe(enc, val):
    return "MIDI CC 3 %s %s;" % (int(enc) - 1, 48 + val)


def ind_animation_off(enc):
    return "MIDI CC 3 %s %s;" % (int(enc) - 1, "0")


def _apply_percentage(val, valrange):
    return int(round(valrange[0] + int(val) * (valrange[1] - valrange[0]) / 100))