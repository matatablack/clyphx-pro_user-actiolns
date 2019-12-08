from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
from template.utils.log_utils import dumpobj,str2bool

class Template(UserActionsBase):

    # tpl = TemplateBase()
    _target_clip = None
    _target_track = None
    current_action_exec = None
    current_action_is_waiting_for_targets = False
    current_action_targets = []
    continue_execution = None

    def __init__(self, cx_core, *a, **k):
        super(Template, self).__init__(cx_core, *a, **k)
        # self._do_init(self)
        self.log = self.canonical_parent.log_message

    def create_actions(self):
        self.add_global_action('tpl', self.entry_point_handler)
        self.add_clip_action('get_clip', self.get_clip)
        self.add_track_action('get_track', self.get_track)

    def entry_point_handler(self, _, args):
        trigger = self.canonical_parent.clyphx_pro_component.trigger_action_list
        self.dispatch(args, trigger)

    def get_clip(self, action_def, args):
        clip = action_def['clip']
        self.set_target_clip(clip)

    def set_target_clip(self, clip):
        if clip:
            self._target_clip = clip
        else:
            self._target_clip = None

    def _get_clip(self, target = 'SEL'):
        self.trigger("user_clip(%s) get_clip" % target)
        # self.log('selected clip name: %s' % getattr(self._target_clip, "name", "No target clip"))
        return self._target_clip

    def get_track(self, action_def, args):
        track = action_def['track']
        self.set_target_track(track)

    def on_selected_track_changed(self):
        try:
            track = self.song().view.selected_track
            if self.current_action_is_waiting_for_targets:
                self.current_action_targets.append(track)
                self.continue_execution()
        except BaseException as e:
            self.log('ERROR: ' + str(e))
    
    def on_selected_scene_changed(self):
        self.on_selected_scene_changed()

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

    def dump(self):
        self.log('dump called %s' % self.song().view.selected_track.name)
        # try:
        #     self.log_obj(self.song().tracks[2])
        #     self.song().tracks[2].arm = True
        #     # self.song().tracks[0].arm = True
        #     # self.log_obj(self.song().tracks[0])
        # except BaseException as e:
        #     self.log('ERROR: ' + str(e))
        
        
        self._init_func('dump')
        self.current_action_targets.append(self._get_clip())     
        self.collect_targets(self.on_target_selection)
            
    def on_target_selection(self):
        self.song().tracks[2].arm = True
        try:
            source_clip = self.current_action_targets[0]
            source_track = source_clip.canonical_parent.canonical_parent
            target_track = self.current_action_targets[1]
            
            self.log('SOURCE CLIP NAME: %s' % source_clip.name)
            self.log('TARGET TRACK: %s' % target_track.name)
            self.log('INPUT ROUTING %s' % target_track.current_input_routing)
            # -> preserve state of things im changing (snap actions?)
            # self.trigger('"%s"/IN "%s"; "Test"/ARM ON; "Gen"/MUTE;' % (target_track.name, source_track.name))
            # self.trigger('"%s"/ARM ON' % (target_track.name))
            # self.trigger('SRECFIX %s' % (source_clip.length / 4))

            self._clean_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))
      
