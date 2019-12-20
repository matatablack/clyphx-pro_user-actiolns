from utils.log_utils import dumpobj,str2bool
from utils.mf_utils import rgb_brightness, color,rgb_pulse, ind_brightness

class MidiFighter:
    
    def _do_init(self, live, trigger):
        self.live = live
        self.log = live.canonical_parent.log_message
        self.trigger = trigger

    def change_bank(self, bank):
        try:
            bank_number = int(bank) - 1
            self.trigger('MIDI CC 4 %s 127' % bank_number)
        except BaseException as e:
            self.log('ERROR: ' + str(e))

    def bind(self):
        s = "BIND CALLED"
        self.log(s)            
        try:
            self.trigger('msg %s' % s)
            self.trigger(rgb_brightness(3, 30))
            self.trigger(ind_brightness(16, 80))
            self.trigger(color(12, 20))
            self.trigger(color(6, 78))
            self.trigger(rgb_pulse(13, 90))
        except BaseException as e:
            self.log('ERROR: ' + str(e))

        
