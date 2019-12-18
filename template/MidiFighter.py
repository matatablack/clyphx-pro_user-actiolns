from utils.log_utils import dumpobj,str2bool

class MidiFighter:
    
    def _do_init(self, live, trigger):
        self.live = live
        self.log = live.canonical_parent.log_message
        self.trigger = trigger

    def change_bank(self):
        self.log('change_bank CALLED')
        try:
            self.trigger('msg "hello!!!! from the other"')
        except BaseException as e:
            self.log('ERROR: ' + str(e))

    def bind(self, bindings):
        self.log('BIND CALLED')
        try:
            self.trigger('msg "about to bind bindings template"')
        except BaseException as e:
            self.log('ERROR: ' + str(e))

        
