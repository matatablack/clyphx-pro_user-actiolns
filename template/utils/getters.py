import re
import random
import string

def generate_id():
    return ''.join([random.choice(string.ascii_letters+string.digits+'-_') for ch in range(8)])

def get_quantization_number_value(self):
    qt = self.live.song().clip_trigger_quantization
    dictionary = {
        'q_bar': 1,
        'q_2_bars': 2,
        'q_4_bars': 4,
        'q_8_bars': 8
    }
    return dictionary.get(str(qt))

def get_clip_id(s):
    search = re.search(r'\[(.*?)\]',s)
    return search.group(1) if search else None