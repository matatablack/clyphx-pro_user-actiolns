import re
import random
import string
import log_utils as log

def generate_id():
    return ''.join([random.choice(string.ascii_letters+string.digits+'-_') for ch in range(8)])

def quantization_number_value(self):
    qt = self.live.song().clip_trigger_quantization
    dictionary = {
        'q_bar': 1,
        'q_2_bars': 2,
        'q_4_bars': 4,
        'q_8_bars': 8
    }
    return dictionary.get(str(qt))

def clip_id(s):
    search = re.search(r'\[(.*?)\]',s)
    return search.group(1) if search else None

def selected_track(self, should_log = False):
    track = self.live.song().view.selected_track
    if should_log:
        log.obj(self, track)
    return track

def selected_device(self, should_log = False):
    dev = selected_track(self).view.selected_device
    if should_log:
        log.obj(self, dev)
    return dev

def track_prefix(self):
    track = selected_track(self)
    prefix = track.name.split()[0]
    return prefix


