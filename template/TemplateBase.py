from utils.log_utils import dumpobj,str2bool

class TemplateBase:
    
    _prev_track_helper = []
    _selected_clip = None

    def _do_init(self, live):
        self.log = live.canonical_parent.log_message
        self.live = live


    def dump(self):
        self.log('dump action start')
        self._get_clip()
        # self.trigger('"Production"/SEL')
        
    #track utils
    def set_selected_track(self, track):
        if len(self._prev_track_helper) < 2: 
            self._prev_track_helper.append(track)
        else:
            del self._prev_track_helper[0]
            self._prev_track_helper.append(track)

    def _previously_selected_track(self):
        self.log('previous_track name: %s' % self._prev_track_helper[0:1][0].name )
        self.log_obj(self._prev_track_helper[0:1][0], False)
        #   return self._prev_track[0:1]

    def _selected_track(self):
        return self.live.song().view.selected_track


    #clip utils
    def set_clip(self, clip):
        if clip:
            self._selected_clip = clip
        else:
            self._selected_clip = None


    def _get_detail_clip(self):
        return self._get_clip('DETAIL')
    
    def _get_clip(self, target = 'SEL'):
        self.trigger("user_clip(%s) get_clip" % target) #ojo con esto, puede que trigger este definido porque se define en dispatch
        self.log('selected clip name: %s' % getattr(self._selected_clip, "name", "No clip selected"))
        return self._selected_clip

    #general
    def dispatch(self, args, trigger):
        self.trigger = trigger
        if not args:
            self.log('Dispatch called without arguments')
        else:
            self.log('Dispatch arguments: %s' % args)
            splited_args = args.split()
            method_name = splited_args[0]
            method = getattr(self, method_name, "notfound")
            if method == 'notfound':
                return self.log('Method not found')
            if len(splited_args) > 1:
                return method(splited_args[1])
            else:
                return method()

    def log_obj(self, obj, show_callable = False):
        should_show_callable = str2bool(show_callable) if isinstance(show_callable, str) else show_callable
        self.log(dumpobj(obj, should_show_callable))