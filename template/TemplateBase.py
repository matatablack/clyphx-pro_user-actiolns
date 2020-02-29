import re
import utils.log_utils as log
import utils.getters as get
from utils.defs import drum_machine_names_mapping_array, control_modes_defs
from MidiFighter import MidiFighter
import time

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

    def _select_process_step_track(self, process_step):
        self.trigger('"%s"/SEL' % (get.track_prefix(self) + ' ' + process_step.capitalize()))
   
    """
        @over any source group
        Trigger record on selected process step in selected source group and take snapshot
    """
    snap_id = ""
    is_recording = False
    def record(self, process_step):
        self._init_func('record', debug=True)
        try:
            # select track
            self._select_process_step_track(process_step)
            self.snap_id = get.generate_id()
            # take snap
            self.trigger("[%s] SEL/SNAP DEV(ALL.ALL);" % self.snap_id)
            #TODO -> exit if has other clip in slot else self.recording = True

            # prepare track and start recording
            self.trigger('SEL/STOP NQ; SEL/ARM ON; METRO ON; SREC ON')
            #TODO -> match clip color with track color
            self._stop_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))

    """
        @over clip
        Stop session recoding and write snapshot id on clip name
    """
    def stop_recording_and_write_snap_id(self):
        self._init_func('stop_recording_and_write_snap_id', debug=True)
        try:
            self.trigger('METRO OFF; SREC OFF; OVER OFF; SEL/ARM OFF')
            selected_clip = self._get_clip()
            self._apply_snap_id_to_clip_name(selected_clip, self.snap_id)
            self.snap_id = ""
            self._stop_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))

    def _apply_snap_id_to_clip_name(self, target_clip, snap_id):
        self._init_func('_apply_snap_id_to_clip_name', debug=True)
        try:
            clip_id = get.clip_id(target_clip.name)
            new_clip_name = ""
            if clip_id:
                # replace id in clip name, returns clip
                new_clip_name = re.sub(r'\[(.*?)\]', '['+clip_id+']', target_clip.name)
            else:
                # concatenate clip id in name
                new_clip_name = target_clip.name + '   [%s]' % snap_id
            self.trigger('WAIT 1; SEL/CLIP NAME "%s"' % new_clip_name)
            self._stop_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))
        

    def _take_snapshot(self, snap_id):
        self.trigger("WAIT 1; [%s] SEL/SNAP DEV(ALL.ALL);" % snap_id)

    """
        @over clip
        Delete target clip and snapshot if present
    """
    def delete_clip(self):
        self._init_func('delete_clip', debug=True)
        try:
            target_clip = self._get_clip()
            snap_id = get.clip_id(target_clip.name)
            self.trigger("SNAPDEL %s;SEL/CLIP(SEL) DEL" % snap_id)
            self._stop_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))


    """
        @over clip
        Take or override snapshot and save id on target clip
    """
    def take_or_override_snap(self):
        self._init_func('take_or_override_snap', debug=True)
        try:
            target_clip = self._get_clip()
            snap_id_in_clip = get.clip_id(target_clip.name)
            snap_id = snap_id_in_clip if snap_id_in_clip else get.generate_id()
            self._take_snapshot(snap_id)
            self._apply_snap_id_to_clip_name(target_clip, snap_id)
            self._stop_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))
    
    """
        @over clip
        Duplicate clip in new scene. If has snap id duplicate snapshot with new id
    """
    def duplicate(self):
        self._init_func('duplicate', debug=True)
        try:
            target_clip = self._get_clip()
            old_clip_snap_id = get.clip_id(target_clip.name)
            new_snap_id = get.generate_id()
            self.trigger("recallsnap %s" % old_clip_snap_id)
            self._take_snapshot(new_snap_id)
            self.trigger("ADDSCENE; WAIT 3; KEY UP; WAIT 2; SEL/CLIP(SEL) DUPE; WAIT 2; KEY DOWN; WAIT 5; tpl duplicate_apply_snap_id %s" % new_snap_id)

            self._stop_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))

    def duplicate_apply_snap_id(self, new_snap_id):
        duplicated_clip = self._get_clip()
        duplicated_clip.name = re.sub(r'\[(.*?)\]', '['+new_snap_id+']', duplicated_clip.name)


    """
        @over clip
        Trigger session overdub 
    """
    def overdub(self):
        self._init_func('overdub', debug=True)
        try:
            self.trigger('SEL/arm; SREC;')
            self._stop_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))


    """
        @over clip
        Recall snapshot if clip has snap id
    """
    def recall(self):
        self._init_func('recall', debug=True)
        try:
            source_clip = self._get_clip()
            clip_id = get.clip_id(source_clip.name)
            self.trigger("SETSTOP; SEL/STOP NQ; recallsnap %s; WAIT 4; SATMR; SEL/PLAY;" % clip_id)
            self._stop_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))


    def dump(self, record_length, process_step = "dump"):
        self._init_func('dump', debug=True)
        try:
            clip = self._get_clip()
            clip_slot_index = None
            if not clip:
                self.log('Attempted to dump over empty slot')
                self._stop_action_exec()
                return False
            else:
                clip_slots = get.selected_track(self).clip_slots
                for index, clip_slot in enumerate(clip_slots):
                    if clip_slot.clip and clip_slot.clip._live_ptr == clip._live_ptr:
                        self.log('clip slot index found: %s' % str(index))
                        clip_slot_index = index

                self._select_process_step_track(process_step)

                d = { 
                    'scene_index': clip_slot_index + 1,
                    'group_track_name': get.track_prefix(self),
                    'length': record_length,
                    'wait_time': int(record_length) + get.quantization_number_value(self),
                }
    
                actions = '''
                    "{group_track_name} Dump"/ARM ON;
                    "{group_track_name} Group"/STOP NQ;
                    "{group_track_name} Group"/PLAY {scene_index};
                    SRECFIX {length};
                    WAITS {wait_time}B;
                    "{group_track_name} Dump"/ARM OFF;
                    "{group_track_name} Group"/STOP NQ;
                '''.format(**d)
 
                #todo -> consider change resulting clip name (add "dump id" ?)
                self.trigger(actions)

            self._stop_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))

    
    """
        @over clip
        @targets: [track / clipSlot]
        Resample clip in target. 
        Takes an snapshot and write snapshot id into both clip names. 
    """
    def dump_with_target(self):

        try:
            self._init_func('dump', debug=True)
            source_clip = self._get_clip()
            source_track = source_clip.canonical_parent.canonical_parent
            def on_target_selection():
                target_track = self.current_action_targets[0]
                if not target_track: return self._stop_action_exec('Target track not found')

                #generate id. Write in clip name and snapshot 
                clip_id = get.clip_id(source_clip.name)
                dump_id = clip_id if clip_id else get.generate_id()
                if not clip_id:
                    source_clip.name = source_clip.name + '   [%s]' % dump_id

                d = { 
                    'target': target_track.name,
                    'source': source_track.name,
                    'length': source_clip.length / 4,
                    'wait_time': source_clip.length / 4 + get.quantization_number_value(self),
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

    """
        @over clip
        Recall snapshot if clip has id.
    """
    def record_automation(self, rec_fix):
        try:
            self._init_func('record_automation', debug=True)

            source_track = self.live.song().view.selected_track

            snap_id = source_track.name + '_' + get.generate_id()

            d = { 
                'rec_fix': rec_fix,
                'wait_time': int(rec_fix) + get.quantization_number_value(self),
                'snap_id': snap_id,
                'new_clip_name': "process [%s]" % snap_id
            }

            self.trigger('$select_process_chain$')
            self.trigger('''WAIT 4; [{snap_id}] SEL/SNAP DEV(ALL.ALL);'''.format(**d))

            actions = '''
                WAIT 5;
                ALL/ARM OFF;
                SEL/ARM ON;
                SEL/DEV("Gen") SEL;
                tpl change_bank 1;
                tpl bind default_binding;
                WAIT 2;
                SRECFIX {rec_fix};
                WAITS {wait_time}B;
                SEL/ARM OFF;
                SEL/CLIP(SEL) NAME "{new_clip_name}"
            '''.format(**d)

            self.trigger(actions)

            self._stop_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))
    
    """
        @over clip
        Override snapshot if clip has snap id
    """
    def override_process_snap(self):
        try:
            self._init_func('override_snap', debug=True)
            source_clip = self._get_clip()
            snap_id = get.clip_id(source_clip.name)
            if snap_id:
                self.trigger('[%s] SEL/SNAP DEV(ALL.ALL);' % snap_id)
            else:
                self.log('No clip id, gato')
            self._stop_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))


    def bind(self, control_mode_name):
        try:
            self._init_func('bind', debug=True)
            if control_modes_defs[control_mode_name]:
                self.trigger(control_modes_defs[control_mode_name]["binding"])
                self.mf.set_color_schema(control_modes_defs[control_mode_name]["color_schema"])
            self._stop_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))

    current_view = "session"
    def change_view(self):
        try:
            self._init_func('change_view', debug=True)
            if self.current_view == "session":
                self.trigger('TGLMAIN; "GEN","Dump","Process","Bucket"/FOLD ON; "Production"/FOLD OFF')
                self.current_view = "arrangement"
            else:
                self.trigger('TGLMAIN; "GEN","Dump","Process","Bucket"/FOLD OFF; "Production"/FOLD ON')    
                self.current_view = "session"
            self._stop_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))

    def bidule_arrangement_navigation_helper(self, active):
        try:
            self._init_func('drum_machine', debug=True)
            if active == '1':
                """ self.trigger('''
                    %bidule_1% = KEY DOWN;
                    %bidule_2% = KEY UP;
                    msg "bidule_arrangement_navigation_helper 1";
                ''') """
                self.trigger('''
                    KEY SHIFT DN;
                    %bidule_1% = KEY LEFT;
                    %bidule_2% = KEY RIGHT;
                    msg "bidule_arrangement_navigation_helper 1";
                ''')
            else:
                self.trigger('''
                    KEY FLUSH;
                    %bidule_1% = LEFT; 
                    %bidule_2% = RIGHT;
                    msg "bidule_arrangement_navigation_helper 2"
                ''')
            self._stop_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))




    def change_bank(self, bank):
        self.mf.change_bank(bank)

    def drum_machine(self, slot):
        try:
            self._init_func('drum_machine', debug=True)
            if drum_machine_names_mapping_array[int(slot)-1]:
                name = drum_machine_names_mapping_array[int(slot)-1]
                self.trigger('"{name}"/sel'.format(name=name))
                self._stop_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))

    def hot_swap(self):
        try:
            if not self._init_func('hot_swap', debug=True):
                return False
            dev = get.selected_device(self)
            self.trigger('[snare] "Snare"/SNAP DEV(1)')
            self.trigger('WAIT 1; "Snare"/DEV(1) SEL; WAIT 1; SWAP')
        except BaseException as e:
            self.log('ERROR: ' + str(e))

    def continue_hot_swap(self, snap_name = "snare"):
        try:
            self.trigger("KEY ENTER; wait 2; SWAP; wait 4;")
            self.trigger("wait 4; recallsnap %s" % snap_name)
            self._stop_action_exec()
        except BaseException as e:
            self.log('ERROR: ' + str(e))           
            



    #esto sirve, no more manitos

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
        return self._target_clip

     #action utils
    def _init_func(self, action_name, debug=False):
        if self._is_executing_other_action(action_name): return False
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

        
