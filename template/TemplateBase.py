TPL_PREFIX = "tpl"



class TemplateBase:
    

    def doInit(self, live):
        self.log = live.canonical_parent.log_message
        # self.trigger = live.canonical_parent.clyphx_pro_component.trigger_action_list

    def dispatch(self, args):
        self.log('%s handler exec and val:' % TPL_PREFIX)

    def dump(self):
        self.log('dump action start')

    def set_selected_track(self, track):
        self.log(track.name)

