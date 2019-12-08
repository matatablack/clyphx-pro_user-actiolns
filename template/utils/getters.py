def get_quantization_number_value(self):
    qt = self.live.song().clip_trigger_quantization
    dictionary = {
        'q_bar': 1,
        'q_2_bars': 2,
        'q_4_bars': 4,
        'q_8_bars': 8
    }
    return dictionary.get(str(qt))