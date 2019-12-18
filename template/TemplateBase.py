from utils.log_utils import dumpobj,str2bool
from utils.getters import get_quantization_number_value,get_clip_id,generate_id
from MidiFighter import MidiFighter
import uuid

#tail log: tail -f -n100 "/Users/matata/Library/Preferences/Ableton/Live 10.1/Log.txt"

class TemplateBase:

    debug_mode = False
    _target_clip = None
    _target_track = None
    current_action_exec = None
    current_action_is_waiting_for_targets = False
    current_action_targets = []
    continue_execution = None
    # are_targets_available = threading.Event()

    mf = MidiFighter()
    

    def _do_init(self, live):
        self.log = live.canonical_parent.log_message
        self.live = live


    def dump(self):
        try:
            self._init_func('dump', debug=True)
            source_clip = self._get_clip()
            source_track = source_clip.canonical_parent.canonical_parent
            def on_target_selection():
                target_track = self.current_action_targets[0]
                if not target_track: return self._stop_action_exec('Target track not found')

                #generate id. Write in clip name and snapshot 
                clip_id = get_clip_id(source_clip.name)
                dump_id = clip_id if clip_id else generate_id()
                if not clip_id:
                    source_clip.name = source_clip.name + '   [%s]' % dump_id

                d = { 
                    'target': target_track.name,
                    'source': source_track.name,
                    'length': source_clip.length / 4,
                    'wait_time': source_clip.length / 4 + get_quantization_number_value(self),
                    'clip': source_clip.name,
                    'dump_id': dump_id
                }
                # -> preserve state of things im changing (snap actions?)             
                actions = '''
                    [{dump_id}] "{source}"/SNAP;
                    "{target}"/IN "{source}"; 
                    "{target}"/ARM ON;
                    "{source}"/STOP;
                    SRECFIX {length};
                    "{source}"/PLAY "{clip}";
                    WAITS {wait_time}B;
                    "{source}", "{target}"/ARM OFF;
                    "{source}"/STOP NQ;
                    "{target}"/MON AUTO;
                    "{target}"/CLIP(SEL) NAME "{clip}"
                '''.format(**d)

                self.trigger(actions)
                self._stop_action_exec()

            self.collect_targets(on_target_selection)
        except BaseException as e:
            self.log('ERROR: ' + str(e))

    def control(self):
        try:
            self._init_func('control', debug=True)
            """ 
                stop play, remember if playing and  arrangement locator (common?)
                arm (snap all others?) (common)


            """
            source_clip = self._get_clip()
            source_track = source_clip.canonical_parent.canonical_parent

            clip_id = get_clip_id(source_clip.name)
                    
            self.trigger("recallsnap %s" % clip_id)

            self._stop_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))

    def bind(self):
        self.mf.change_bank()

    
    

            

    def on_selected_track_changed(self):
        try:
            track = self.live.song().view.selected_track
            if self.current_action_is_waiting_for_targets:
                #todo => and self.current_action_targets_def para saber si es trakc clip device o que
                self.current_action_targets.append(track)
                self.live.canonical_parent.schedule_message(2, self.continue_execution)
        except BaseException as e:
            self.log('ERROR: ' + str(e))

    def on_selected_scene_changed(self):
        # self.log('selected scene changed')
        pass
        
    #track utils
    def set_target_track(self, track):
        if track:
            self._target_track = track
        else:
            self._target_track = None
    
    def _get_track(self, track_name = False):
        target = 'SEL' if not track_name else '"%s"' % track_name
        self.trigger('%s/get_track' % target)
        return self._target_track

        #[] OSC STR /track/name "testing!"
        #[] OSC int /k4/value 100


    #clip utils
    def set_target_clip(self, clip):
       self._target_clip = clip if clip else None


    def _get_detail_clip(self):
        return self._get_clip('DETAIL')
    
    def _get_clip(self, target = 'SEL'):
        self.trigger("user_clip(%s) get_clip" % target)
        # self.log('selected clip name: %s' % getattr(self._target_clip, "name", "No target clip"))
        return self._target_clip

     #action utils
    def _init_func(self, action_name, debug=False):
        if self._is_executing_other_action(action_name): pass
        self.debug_mode = True
        self.current_action_exec = action_name
        return self._stop_action_exec

    def _stop_action_exec(self, exception = ''):
        self.current_action_is_waiting_for_targets = False
        self.current_action_targets = []
        self.continue_execution = None
        if exception != '':
            self.log('STOP %s EXEC: %s' % (self.current_action_exec, exception))
        else:
            self.log('Finished %s action execution' % self.current_action_exec)
        self.log('\n\n\n\n')
        self.current_action_exec = None

    def _is_executing_other_action(self, action_name = ''):
        if self.current_action_exec != None:
            self.log('WARNING: Attempted to call %s while %s was executing' % (action_name, self.current_action_exec))
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
                if self.debug_mode:
                    self.log('TRIGGER %s' % action)
        self.trigger = trig_and_log
        self.mf._do_init(self.live, self.trigger)
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
        
