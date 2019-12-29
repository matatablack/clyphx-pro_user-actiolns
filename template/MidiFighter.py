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
            # self.trigger(rgb_brightness(3, 30))
            # self.trigger(ind_brightness(16, 80))
            # self.trigger(color(12, 20))
            # self.trigger(color(6, 78))
            # self.trigger(rgb_pulse(13, 90))
            self.trigger("""
                bind mf_b1_e1 "DrumAut"/dev("Sends") p1;
                bind mf_b1_e5 "DrumAut"/dev("Sends") p5;
                bind mf_b1_e9 "DrumAut"/dev("Customs") p1;
                bind mf_b1_e13 "DrumAut"/dev("Customs") p5;
                bind mf_b1_e2 "DrumAut"/dev("Sends") p2;
                bind mf_b1_e6 "DrumAut"/dev("Sends") p6;
                bind mf_b1_e10 "DrumAut"/dev("Customs") p2;
                bind mf_b1_e14 "DrumAut"/dev("Customs") p6;
                bind mf_b1_e3 "DrumAut"/dev("Sends") p3;
                bind mf_b1_e7 "DrumAut"/dev("Sends") p7;
                bind mf_b1_e11 "DrumAut"/dev("Customs") p3;
                bind mf_b1_e15 "DrumAut"/dev("Customs") p7;
                bind mf_b1_e4 "DrumAut"/dev("Sends") p4;
                bind mf_b1_e8 "DrumAut"/dev("Sends") p8;
                bind mf_b1_e12 "DrumAut"/dev("Customs") p4;
                bind mf_b1_e16 "DrumAut"/dev("Customs") p8;
            """)
        except BaseException as e:
            self.log('ERROR: ' + str(e))

        
