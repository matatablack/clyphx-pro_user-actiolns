from utils.log_utils import dumpobj,str2bool
import threading

class TemplateBase:
    
    _target_clip = None
    _target_track = None
    current_action_exec = None
    current_action_is_waiting_for_targets = False
    current_action_targets = []
    continue_execution = None
    # are_targets_available = threading.Event()
    

    def _do_init(self, live):
        self.log = live.canonical_parent.log_message
        self.live = live


    def dump(self):
        try:
            self._init_func('dump')
            source_clip = self._get_clip()
            source_track = source_clip.canonical_parent.canonical_parent
            def on_target_selection():
                target_track = self._get_track(self.current_action_targets[0].name)
                self.log('SOURCE CLIP NAME: %s' % source_clip.name)
                self.log('TARGET TRACK: %s' % target_track.name)
                self.log('INPUT ROUTING %s' % target_track.current_input_routing)
                # -> preserve state of things im changing (snap actions?)

                self.trigger('"%s"/IN "%s"; "Test"/ARM ON; "Gen"/MUTE;' % (target_track.name, source_track.name))
                # self.trigger('"%s"/ARM ON' % (target_track.name))
                # self.trigger('SRECFIX %s' % (source_clip.length / 4))

                self._clean_action_exec()
                


            self.collect_targets(on_target_selection)
        except BaseException as e:
            self.log('ERROR: ' + str(e))


            

    def on_selected_track_changed(self):
        try:
            track = self.live.song().view.selected_track
            if self.current_action_is_waiting_for_targets:
                self.current_action_targets.append(track)
                self.continue_execution()
        except BaseException as e:
            self.log('ERROR: ' + str(e))

    def on_selected_scene_changed(self):
        self.log('selected scene changed')
        
    #track utils
    def set_target_track(self, track):
        if track:
            self._target_track = track
        else:
            self._target_track = None
    
    def _get_track(self, track_name = False):
        target = 'SEL' if not track_name else '"%s"' % track_name
        self.trigger('%s/get_track' % target)
        # self.log('selected track name: %s' % getattr(self._target_track, "name", "No target track"))
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
        # self.log('selected clip name: %s' % getattr(self._target_clip, "name", "No target clip"))
        return self._target_clip

     #action utils
    def _init_func(self, action_name):
        if self._is_executing_other_action(action_name): pass
        self.current_action_exec = action_name
        return self._clean_action_exec

    def _clean_action_exec(self):
        self.current_action_exec = None
        self.current_action_is_waiting_for_targets = False
        self.current_action_targets = []
        self.continue_execution = None
        self.log('Finished %s action execution' % self.current_action_exec)

    def _is_executing_other_action(self, action_name = ''):
        if self.current_action_exec != None:
            self.log('Attempted to call %s while %s was executing' % (action_name, self.current_action_exec))
            return True
        else:
            return False

    def collect_targets(self, callback):
        self.current_action_is_waiting_for_targets = True
        self.continue_execution = callback

    #general
    def dispatch(self, args, trigger):
        def trig_and_log(action):
                trigger(action)
                self.log('TRIGGER %s' % action)
        self.trigger = trig_and_log
        if not args:
            self.log('Dispatch called without method name')
        else:
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
        
