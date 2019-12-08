from utils.log_utils import dumpobj,str2bool

class TemplateBase:
    
    _target_clip = None
    _target_track = None

    def _do_init(self, live):
        self.log = live.canonical_parent.log_message
        self.live = live


    def dump(self):
        self.log('dump action start')
        self._get_track()
        # self.trigger('"Production"/SEL')
        
    #track utils
    def set_target_track(self, track):
        if track:
            self._target_track = track
        else:
            self._target_track = None
    
    def _get_track(self, track_name = False):
        target = 'SEL' if not track_name else '"%s"' % track_name
        self.trigger('%s/get_track' % target)
        self.log('selected track name: %s' % getattr(self._target_track, "name", "No target track"))
        return self._target_track


    #clip utils
    def set_target_clip(self, clip):
        if clip:
            self._target_clip = clip
        else:
            self._target_clip = None


    def _get_detail_clip(self):
        return self._get_clip('DETAIL')
    
    def _get_clip(self, target = 'SEL'):
        self.trigger("user_clip(%s) get_clip" % target)
        self.log('selected clip name: %s' % getattr(self._target_clip, "name", "No target clip"))
        return self._target_clip

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