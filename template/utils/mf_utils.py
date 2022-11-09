def color(enc, val):
    #todo -> accept hex
    # return "MIDI NOTE 1 %s %s;" % (int(enc) - 1, val)
    #  return "MIDI CC 2 %s %s" % (int(enc) - 1, val)
    return "MIDI CC 2 %s %s;" % (int(enc) - 1, val)

def rgb_brightness(enc, val):
#     return _build_light_change_midi_message(enc, val, [17, 47])
    return "MIDI CC 6 %s %s" % (int(enc) - 1, _apply_percentage(val, [17, 47]))

def rgb_pulse(enc, val):
    #todo -> accept time division e.j. 1/4 when effects depends on tempo
    # return _build_light_change_midi_message(enc, val, [9, 16]
    return "MIDI CC 6 %s %s" % (int(enc) - 1, _apply_percentage(val, [9, 16]))

def ind_brightness(enc, val):
    # return _build_light_change_midi_message(enc, val, [65, 95])
    return "MIDI CC 3 %s %s" % (int(enc) - 1, _apply_percentage(val, [65, 95]))

def _build_light_change_midi_message(enc, val, valrange):
    return "MIDI CC 3 %s %s" % (int(enc) - 1, _apply_percentage(val, valrange))

def _apply_percentage(val, valrange):
    return int(round(valrange[0] + int(val)  * (valrange[1] - valrange[0]) / 100))