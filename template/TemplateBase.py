from utils.log_utils import dumpobj

class TemplateBase:
    
    _prev_track = []
    # _prev_clip = []
    # _prev_scene = []

    def _do_init(self, live):
        self.log = live.canonical_parent.log_message
        self.live = live
        # self.dump_object = lambda obj:self.log(dumpobj(obj))
        # self.trigger = live.canonical_parent.clyphx_pro_component.trigger_action_list

    def dispatch(self, args):
        if not args:
            self.log('Dispatch called without arguments')
        else:
            self.log('Dispatch arguments: %s' % args)
            splited_args = args.split()
            method_name = splited_args[0]
            method = getattr(self, method_name, lambda: self.log("Method %s not found" % method_name))
            return method(splited_args[1])

    def dump(self):
        self.log('dump action start')
        
    
    def set_selected_track(self, track):
        if len(self._prev_track) < 2: 
            self._prev_track.append(track.name)
        else:
            del self._prev_track[0]
            self._prev_track.append(track.name)


    def get_previous_track(self, log):
        self.log('prev track: %s' % self._prev_track[0:1])
        #   return self._prev_track[0:1]

    def selected_track(self, log):
        self.log('selected_track called')
        if log:
            self.log_obj(self.live.song().view.selected_track, True)

    def log_obj(self, obj, show_callable):
        self.log(dumpobj(obj, show_callable))