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

    def set_color_schema(self, control_mode_color_schema):
        try:
            for color_def in control_mode_color_schema:
                self.trigger(color(color_def[0], color_def[1]))
                self.trigger(rgb_brightness(color_def[0], color_def[2])) #not working!
                self.trigger(ind_brightness(color_def[0], color_def[3]))
        except BaseException as e:
            self.log('ERROR: ' + str(e))

        
