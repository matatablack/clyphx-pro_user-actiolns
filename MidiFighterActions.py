

from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
from utils.log_utils import dumpobj
from utils.defs import colors_by_name, control_modes_defs
from utils.mf_utils import rgb_brightness, color, rgb_pulse, rgb_strobe, ind_brightness, ind_pulse, ind_strobe, rgb_animation_off, ind_animation_off

NUM_X_CONTROLS = 34

modes = {
    "instrument_control_1": {
        "channels": {
            "Omni 1 [MIDI]": {
                "encoders": [1, 5],
                "lights_status": {
                    "5": "",
                    "1": ""
                }
            },
            "Omni 1": {
                "encoders": [9, 13],
                "lights_status": {
                    "13": "",
                    "9": ""
                }
            },
            "V. Bass [MIDI]": {
                "encoders": [2, 6],
                "lights_status": {
                    "6": "",
                    "2": ""
                }
            },
            "V. Bass": {
                "encoders": [10, 14],
                "lights_status": {
                    "14": "",
                    "10": ""
                }
            },
            "SH01A [MIDI]": {
                "encoders": [3, 7],
                "lights_status": {
                    "7": "",
                    "3": ""
                }
            },
            "SH01A": {
                "encoders": [11, 15],
                "lights_status": {
                    "15": "",
                    "11": ""
                }
            },
            "TB3 [MIDI]": {
                "encoders": [4, 8],
                "lights_status": {
                    "8": "",
                    "4": ""
                }
            },
            "TB3": {
                "encoders": [12, 16],
                "lights_status": {
                    "16": "",
                    "12": ""
                }
            }
        }
    },
    "instrument_control_2": {
        "channels": {
            "Grandmother [MIDI]": {
                "encoders": [1, 5],
                "lights_status": {
                    "5": "",
                    "1": ""
                }
            },
            "Grandmother": {
                "encoders": [9, 13],
                "lights_status": {
                    "13": "",
                    "9": ""
                }
            },
            "Deepmind": {
                "encoders": [2, 6],
                "lights_status": {
                    "6": "",
                    "2": ""
                }
            },
            "Deepmind [MIDI]": {
                "encoders": [10, 14],
                "lights_status": {
                    "14": "",
                    "10": ""
                }
            },
            "GTR VOX": {
                "encoders": [4, 8, 12, 16],
                "lights_status": {
                    "4": "",
                    "8": "",
                    "12": "",
                    "16": ""
                }
            },
            "Omni 2 [MIDI]": {
                "encoders": [3, 7],
                "lights_status": {
                    "7": "",
                    "3": ""
                }
            },
            "Omni 2": {
                "encoders": [11, 15],
                "lights_status": {
                    "15": "",
                    "11": ""
                }
            }
        }
    },
    "instrument_control_3": {
        "channels": {
            "BASS COMP": {
                "encoders": [1, 5, 9, 13],
                "lights_status": {
                    "13": "",
                    "9": "",
                    "5": "",
                    "1": ""


                }
            },
            "Yamaha [MIDI]": {
                "encoders": [2, 6],
                "lights_status": {
                    "6": "",
                    "2": ""
                }
            },
            "Yamaha": {
                "encoders": [10, 14],
                "lights_status": {
                    "14": "",
                    "10": ""
                }
            },
            "GTR Acus": {
                "encoders": [4, 8, 12, 16],
                "lights_status": {
                    "16": "",
                    "12": "",
                    "8": "",
                    "4": ""
                }
            },
            "Omni 3 [MIDI]": {
                "encoders": [3, 7],
                "lights_status": {
                    "7": "",
                    "3": ""
                }
            },
            "Omni 3": {
                "encoders": [11, 15],
                "lights_status": {
                    "15": "",
                    "11": ""
                }
            }
        }
    }
}

all_modes = list(modes.keys())
all_channels = []
for mode_key in all_modes:
    all_mode_channels = list(modes[mode_key]['channels'].keys())
    all_channels = all_channels + all_mode_channels

class MidiFighterActions(UserActionsBase):

    def create_actions(self):
        self.add_global_action('set_mf_binding', self.set_mf_binding)
        self.add_global_action('record', self.record)
        self.add_global_action('set_record_length', self.set_record_length)
        self.add_global_action('delete_last_clip', self.delete_last_clip)
        self.add_global_action('set_last_clip_for_switch', self.set_last_clip_for_switch)
        self.add_global_action('mf_shift_switches', self.mf_shift_switches)
        self.add_global_action('mf_finish_execution', self.finish_execution)
        self.add_global_action('mf_change_bank', self.mf_change_bank)
        self.add_global_action('mf_populate', self.populate_last_clip_by_channel)
        self.add_global_action('execute_mf_lights_actions', self.execute_mf_lights_actions)

    is_execution_blocked = False
    current_action = None
    log = None
    trigger = None

    def start_action(self, action_to_execute, args, block=False):
        self.log = self.canonical_parent.log_message

        def trigger(actions, log=True):
            if log:
                self.log(actions)
            self.canonical_parent.clyphx_pro_component.trigger_action_list(actions)
        self.trigger = trigger
        action = "%s %s" % (action_to_execute, args)
        self.log('Startin Action ---> [%s]' % action)

        if self.is_execution_blocked:
            msg = "Blocked, still executing [%s] action" % (self.current_action)
            self.trigger('msg "%s"' % msg)
            raise Exception(msg)
        elif block:
            self.current_action = action
            self.is_execution_blocked = True

    def finish_execution(self, action_def, args):
        self.is_execution_blocked = False
        self.current_action = None
        self.log('Unblocking...')
        return

    current_control_mode_name = ""
    prev_current_control_mode_name = ""
    mf_shift_switches = False

    def execute_mf_lights_actions(self, action_def, args):
        self.start_action('execute_mf_lights_actions', "")
        try:
            result = ""
            for channel_name in list(modes[self.current_control_mode_name]["channels"].keys()):
                channel_obj = modes[self.current_control_mode_name]["channels"][channel_name]
                self.log('CHANNEL %s' % channel_name)
                for enc_pos in channel_obj['encoders']:
                    self.log('enc_pos %s' % enc_pos)
                    lights = channel_obj['lights_status']
                    self.log(str(lights))
                    action = lights[str(enc_pos)]
                    self.log('action %s' % action);
                    if action: 
                        self.log("TRIGGGGERRRRR");
                        self.trigger(action);

            # self.trigger(result);
        except BaseException as e:
            self.canonical_parent.log_message('ERROR execute_mf_lights_actions: ' + str(e))

    def set_mf_binding(self, action_def, args):
        try:
            self.start_action('set_binding', args)
            args = args.split()
            control_mode_name = args[0]
            bank_number = str(args[1]) if len(args) > 1 else ""
            bank_suffix = "_bank" + bank_number
            is_shift = control_mode_name == 'shift'

            mode_name = ""
            is_current_mode_shifted = "_bank" in self.current_control_mode_name
            mode_name_without_bank_suffix = self.current_control_mode_name.split("_bank")[0]
            if is_shift:
                if is_current_mode_shifted:
                    mode_name = mode_name_without_bank_suffix
                else:
                    mode_name = self.current_control_mode_name + bank_suffix
            else:
                mode_name = control_mode_name
            self.prev_current_control_mode_name = self.current_control_mode_name 
            self.current_control_mode_name = mode_name

            self.trigger('OSC STR custom/global/action "set_binding";')

            if control_modes_defs[mode_name]:
                self.trigger(control_modes_defs[mode_name]["binding"])
                self.set_color_schema(control_modes_defs[mode_name]["color_schema"])

            self.log(' !!!!!!!!!!!!!!! populate_last_clip_by_channel !!!!!!!!!!!!!!!')
            # self.execute_mf_lights_actions(None, "")
            self.populate_last_clip_by_channel(None, "")

            self.log('ASSIGNING MACROS for %s' % mode_name)

            for i in xrange(1, NUM_X_CONTROLS):
                res = '${prefix}{index}$=${prefix}{index}_{footer}$'.format(
                    prefix="mf_b%s_s" % bank_number if is_shift and not is_current_mode_shifted else "mf_b1_s", index=i, footer=mode_name)
                # self.log(res)
                self.trigger(res, False)
            self.trigger("mf_finish_execution;")
        except BaseException as e:
            self.log('ERROR set_mf_binding: ' + str(e))

    def mf_shift_switches(self, action_def, args):
        try:
            args = args.split()
            state = args[0]
            if state == 'on':
                self.mf_shift_switches = True
            else:
                self.mf_shift_switches = False
        except BaseException as e:
            self.canonical_parent.log_message('ERROR mf_shift_switches: ' + str(e))

    record_length = 4

    def set_record_length(self, action_def, args):
        try:
            args = args.split()
            self.record_length = args[0]
        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))

    last_clip_by_channel = {}
    mf_clipslots_has_clip_callbacks = {}
    mf_clipslots_is_triggered_clip_callbacks = {}
    mf_clips_playing_status_callbacks = {}

    def populate_last_clip_by_channel(self, action_def, args):
        try:
            self.start_action('populate_last_clip_by_channel', args)

            def is_track_visible_in_current_mode(track_name):
                return True if modes[self.current_control_mode_name]['channels'] and modes[self.current_control_mode_name]['channels'][str(track_name)] else False
            def get_switch_position_by_track_name(track_name, clipslot):
                try:
                    position = modes[self.current_control_mode_name]['channels'][str(track_name)]['encoders'][clipslot]
                    return position
                except BaseException as e:
                    self.canonical_parent.log_message('ERROR get_switch_position_by_track_name: ' + str(e))

            tracklist = list(self.song().tracks)

            def get_track_by_name(name):
                try:
                    for t in tracklist:
                        if t.name == name:
                            return t
                except BaseException as e:
                    self.canonical_parent.log_message('ERROR: get_track_by_name' + str(e))

            def get_clip_playing_status_callback(trackname, track_index, clipslot_index, key, original_color):
                self.log('registering clip_playing_status_callback for %s %s %s ' % (track_index, trackname, clipslot_index))
                def clip_playing_status_callback():
                    track = get_track_by_name(trackname)
                    # if track.clip_slots[clipslot_index].has_clip:
                    #     clip = track.clip_slots[clipslot_index].clip
                    #     switch_position = get_switch_position_by_track_name(trackname, clipslot_index)
                    #     b = ""
                    #     a = ""
                    #     c = ""
                    #     if clip.is_recording:
                    #         self.log('IS RECORDING %s %s %s' % (track_index, trackname, clipslot_index))
                    #         b = rgb_brightness(switch_position, 100)
                    #         a = rgb_pulse(switch_position, 4)
                    #         c = color(switch_position, 83)
                    #     elif clip.is_playing:
                    #         self.log('IS PLAYINGGGG %s %s %s' % (track_index, trackname, clipslot_index))
                    #         b = rgb_brightness(switch_position, 90)
                    #         a = rgb_pulse(switch_position, 6)
                    #         c = color(switch_position, original_color)
                    #     else:
                    #         self.log('IS STOPPED %s %s %s' % (track_index, trackname, clipslot_index))
                    #         b = rgb_brightness(switch_position, 35)
                    #         a = rgb_pulse(switch_position, 0)
                    #         c = color(switch_position, original_color)

                    #     lights_status_action = b + a + c
                    #     if is_track_visible_in_current_mode(trackname):
                    #         self.trigger(lights_status_action)
                    #     try:
                    #         modes[self.current_control_mode_name]['channels'][trackname]['lights_status'][str(switch_position)] = lights_status_action
                    #     except BaseException as e:
                    #         self.canonical_parent.log_message('ERROR clip_playing_status_callback: ' + str(e))
                return clip_playing_status_callback

            def get_clip_slot_has_clip_callback(trackname, track_index, clipslot_index, key, original_color):
                self.log('registering clip_slot_has_clip for %s %s %s ' % (track_index, trackname, clipslot_index))
                def clip_slot_has_clip_callback():
                    clipslot = get_track_by_name(trackname).clip_slots[clipslot_index]
                    switch_position = get_switch_position_by_track_name(trackname, clipslot_index)

                    b = ""
                    a = ""
                    c = ""
                    if clipslot.has_clip:
                        self.log('HAS CLIP %s %s %s' % (track_index, trackname, clipslot_index))
                        if is_track_visible_in_current_mode(trackname):
                            self.log(switch_position)
                            b = rgb_brightness(switch_position, 100)
                        else:
                            self.log('Updated track not visible in current mode')

                    else:
                        self.log('NO CLIP %s' % trackname)
                        b = rgb_brightness(switch_position, 60)
                        a = rgb_strobe(switch_position, 0)
                        c = color(switch_position, original_color)
                    
                    lights_status_action = b + a + c
                    if is_track_visible_in_current_mode(trackname):
                        self.trigger(lights_status_action)
                    self.log(lights_status_action)
                    try:
                        modes[self.current_control_mode_name]['channels'][trackname]['lights_status'][str(switch_position)] = lights_status_action
                    except BaseException as e:
                        self.canonical_parent.log_message('ERROR clip_slot_has_clip_callback: ' + str(e))

                return clip_slot_has_clip_callback

            def get_clip_slot_is_triggered(trackname, track_index, clipslot_index, key, original_color):
                def clip_slot_is_triggered():
                    clipslot = tracklist[track_index].clip_slots[clipslot_index]
                    switch_position = get_switch_position_by_track_name(trackname, clipslot_index)
                    b = ""
                    a = ""
                    c = ""
                    if clipslot.is_triggered:
                        if clipslot.will_record_on_start:
                            self.log(' %s %s IS EMPTY ABOUT TO RECORD' % (trackname, clipslot_index))
                            b = rgb_brightness(switch_position, 80)
                            a = rgb_strobe(switch_position, 6)
                            c = color(switch_position, 80)

                        if clipslot.has_clip:
                            self.log(' %s %s HAS CLIP' % (trackname, clipslot_index))
                            b = rgb_brightness(switch_position, 100)
                            a = rgb_pulse(switch_position, 5)
                            c = color(switch_position, 42)
                        else:
                            self.log(' %s %s ABOUT TO START PLAYING or stop' % (trackname, clipslot_index))
                            b = rgb_brightness(switch_position, 80)
                            a = rgb_pulse(switch_position, 5)
                            c = color(switch_position, original_color)
                    lights_status_action = b + a + c
                    if is_track_visible_in_current_mode(trackname):
                            self.trigger(lights_status_action)
                    self.log(lights_status_action)
                    try:
                        modes[self.current_control_mode_name]['channels'][trackname]['lights_status'][str(switch_position)] = lights_status_action
                    except BaseException as e:
                        self.canonical_parent.log_message('ERROR clip_slot_is_triggered : ' + str(e))
                return clip_slot_is_triggered
                                


            self.log('CURRENT current_control_mode_name %s' % self.current_control_mode_name)
            if modes.get(self.current_control_mode_name):
                for t in tracklist:
                     #remove previous listener if has one
                    if self.prev_current_control_mode_name and modes.get(self.prev_current_control_mode_name):
                        if t.name in list(modes[self.prev_current_control_mode_name]['channels'].keys()):
                            self.log('Start Removing listeners for PREV controlled track %s' % t.name)
                            for clipslot_index in range(0, 2):
                                clipslot = t.clip_slots[clipslot_index]
                                name = str(t.name)
                                index = str(clipslot_index)
                                key = name + index
                                if self.mf_clipslots_has_clip_callbacks.get(key) and clipslot.has_clip_has_listener(self.mf_clipslots_has_clip_callbacks[key]):
                                    self.log('SUCCESSFULLy remove_has_clip_listener %s' % key)
                                    clipslot.remove_has_clip_listener(self.mf_clipslots_has_clip_callbacks[key])
                                    del self.mf_clipslots_has_clip_callbacks[key]
                                if self.mf_clipslots_is_triggered_clip_callbacks.get(key) and clipslot.is_triggered_has_listener(self.mf_clipslots_is_triggered_clip_callbacks[key]):
                                    self.log('SUCCESSFULLy remove_is_triggered_listener %s' % key)
                                    clipslot.remove_is_triggered_listener(self.mf_clipslots_is_triggered_clip_callbacks[key])
                                    del self.mf_clipslots_is_triggered_clip_callbacks[key]
                                if self.mf_clips_playing_status_callbacks.get(key) and clipslot.has_clip and clipslot.clip.playing_status_has_listener(self.mf_clips_playing_status_callbacks[key]):
                                    self.log('SUCCESSFULLy remove_playing_status_listener %s' % key)
                                    clipslot.clip.remove_playing_status_listener(self.mf_clips_playing_status_callbacks[key])
                                    del self.mf_clips_playing_status_callbacks[key]
                        
                    if t.name in list(modes[self.current_control_mode_name]['channels'].keys()):
                        self.log('Start Adding listeners to clipslot on track %s' % t.name)
                        original_color = colors_by_name[str(t.name.split("[MIDI]")[0].strip())]["default"]
                        for clipslot_index in range(0, 2):
                            clipslot = t.clip_slots[clipslot_index]
                            name = str(t.name)
                            index = str(clipslot_index)
                            key = name + index

                            switch_number = get_switch_position_by_track_name(t.name, clipslot_index)
                            self.trigger('set_last_clip_for_switch "%s" %s"%s";' % (t.name, switch_number - 1, clipslot_index + 1))
                            
                            new_has_clip_callback = get_clip_slot_has_clip_callback(t.name, tracklist.index(t), clipslot_index, key, original_color)
                            clipslot.add_has_clip_listener(new_has_clip_callback)
                            self.mf_clipslots_has_clip_callbacks[key] = new_has_clip_callback
                            new_has_clip_callback()

                            new_is_triggered_callback = get_clip_slot_is_triggered(t.name, tracklist.index(t), clipslot_index, key, original_color)
                            clipslot.add_is_triggered_listener(new_is_triggered_callback)
                            self.mf_clipslots_is_triggered_clip_callbacks[key] = new_is_triggered_callback
                            new_is_triggered_callback()

                            if clipslot.has_clip:
                                new_playing_status = get_clip_playing_status_callback(t.name, tracklist.index(t), clipslot_index, key, original_color)
                                clipslot.clip.add_playing_status_listener(new_playing_status)
                                self.mf_clips_playing_status_callbacks[key] = new_playing_status
                                new_playing_status()

        except BaseException as e:
            self.canonical_parent.log_message('ERROR: populate_last_clip_by_channel ' + str(e))

    def delete_last_clip(self, action_def, args):
        try:
            self.start_action('delete_last_clip', args)
            args = args.split('"')
            channel_name = args[1]
            switch_number = int(args[2])
            original_color = colors_by_name[str(channel_name.split("[MIDI]")[0].strip())]["default"]
            self.log(str(self.last_clip_by_channel))
            channel_switches = self.last_clip_by_channel[str(channel_name)] if self.last_clip_by_channel.get(channel_name) else None
            self.log("channel_switches: %s " % str(channel_switches))
            clipslot = channel_switches[str(switch_number)] if channel_switches else None
            self.log("ACTIVE CLIPSLOT FOR SWITCH: %s " % str(clipslot))

            dictionary = {
                'channel_name': channel_name,
                'clipslot': clipslot,
                'original_color': original_color
            }
            if clipslot:
                actions = '''"{channel_name}"/CLIP({clipslot}) DEL;'''.format(**dictionary)
                self.canonical_parent.clyphx_pro_component.trigger_action_list(actions)
                self.log(actions)
            else:
                self.log("No clip on %s switch %s" % (channel_name, switch_number))
        except BaseException as e:
            self.canonical_parent.log_message('Error delete_last_clip' + str(e))

    def record(self, action_def, args):
        try:
            self.start_action('record', args)
            args = args.split('"')
            channel_name = args[1]
            switch_number = int(args[2])
            original_color = colors_by_name[str(channel_name.split("[MIDI]")[0].strip())]["default"]

            tracklist = list(self.song().tracks)
            track = None
            for t in tracklist:
                if t.name == channel_name:
                    track = t

            track_index = tracklist.index(track) + 1
            cliplist = list(track.clip_slots)

            try:
                channel_switches = self.last_clip_by_channel[str(channel_name)] if self.last_clip_by_channel[str(channel_name)] else None
                clipslot = channel_switches[str(switch_number)] if channel_switches else None
                self.log("ACTIVE CLIPSLOT FOR SWITCH: %s " % str(clipslot))
                if track.clip_slots[int(clipslot) - 1].has_clip:
                    if self.mf_shift_switches:
                        return track.clip_slots[int(clipslot) - 1].delete_clip()
                    if track.clip_slots[int(clipslot) - 1].clip.is_playing:
                        return track.clip_slots[int(clipslot) - 1].stop()
                    else:
                        return track.clip_slots[int(clipslot) - 1].fire()
            except:
                self.log('no playing clip')

            for clip in track.clip_slots:
                if clip.has_clip:
                    self.log('clip exists')
                elif cliplist.index(clip) == 0:
                    clipslot = cliplist.index(clip)
                    break
                else:
                    clipslot = cliplist.index(clip) - 1
                    break

            if track.clip_slots[clipslot].is_recording:
                return track.clip_slots[clipslot].fire()
            elif track.clip_slots[clipslot].has_clip:
                self.log('not recording, start recording on next slot')
                clipslot += 1

            dictionary = {
                'channel_name': channel_name,
                'switch_index': switch_number - 1,
                'original_color': original_color,
                'rec_color': 79,
                'rec_color2': 83,
                'track_index': track_index,
                'clipslot': clipslot + 1,
                'switch_number': switch_number,
                'mon_auto_if_not_midi': '"%s"/MON AUTO;' % channel_name if not "[MIDI]" in channel_name else ""
            }

            actions = '''
                ## MIDI CC 2 {switch_index} {original_color};
                METRO ON;
                "{channel_name}"/SEL;
                "{channel_name}"/ARM ON;
                {mon_auto_if_not_midi}
                ## MIDI CC 2 {switch_index} {original_color};
                ## MIDI CC 6 {switch_index} 15;
                {track_index}/play {clipslot};
                ## MIDI CC 2 {switch_index} {original_color};
            '''.format(**dictionary)

            def merge_two_dicts(x, y):
                z = x.copy()   # start with keys and values of x
                z.update(y)    # modifies z with keys and values of y
                return z

            fixed_rec_bars = float(self.record_length)
            dict2 = {
                'fixed_rec_bars': fixed_rec_bars,
                'fixed_rec_bars_half': fixed_rec_bars / 2,
                'fixed_rec_bars_half_minus_16': fixed_rec_bars / 2 - fixed_rec_bars / 16,
            }

            def clip_slot_has_clip_callback():
                self.log('HAS CLIP')
                track.clip_slots[clipslot].clip.add_is_recording_listener(post_rec_callback)
                track.clip_slots[clipslot].remove_has_clip_listener(clip_slot_has_clip_callback)
                if track.clip_slots[clipslot].clip.is_recording:
                    # TODO avoid if cancelled
                    while_rec_actions = '''
                            ## MIDI CC 2 {switch_index} {rec_color};
                            ## MIDI CC 6 {switch_index} 6;
                            ## WAITS {fixed_rec_bars_half}B;
                            ## MIDI CC 2 {switch_index} {rec_color2};
                            ## MIDI CC 6 {switch_index} 7;
                            ## WAITS {fixed_rec_bars_half_minus_16}B;
                            ## {track_index}/play {clipslot};
                        '''.format(**merge_two_dicts(dictionary, dict2))
                    self.trigger(while_rec_actions)
                    self.log(while_rec_actions)

            def post_rec_callback():
                self.log('RECORDING STOPPED')
                if not track.clip_slots[clipslot].clip.is_recording:
                    post_rec_actions = '''
                        ## set_last_clip_for_switch "{channel_name}" {switch_number} "{clipslot}";
                        ## MIDI CC 2 {switch_index} {original_color};
                        ## MIDI CC 6 {switch_index} 0;
                        WAITS 1;
                        METRO OFF;
                        "{channel_name}"/ARM OFF;
                    '''.format(**merge_two_dicts(dictionary, dict2))
                    self.trigger(post_rec_actions)
                    self.log(post_rec_actions)
                else:
                    post_rec_actions = '''
                        ## MIDI CC 2 {switch_index} {original_color};
                        ## MIDI CC 6 {switch_index} 0;
                    '''.format(**merge_two_dicts(dictionary, dict2))
                    self.trigger(post_rec_actions)
                    self.log(post_rec_actions)
                track.clip_slots[clipslot].clip.remove_is_recording_listener(post_rec_callback)

            # track.clip_slots[clipslot].add_has_clip_listener(clip_slot_has_clip_callback)

            self.trigger(actions)
        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))

    def set_last_clip_for_switch(self, action_def, args):
        try:
            self.log('set_last_clip_for_switch')
            args = args.split('"')
            channel_name = args[1].strip()
            switch_number = int(args[2])
            clipslot = int(args[3])
            self.last_clip_by_channel[channel_name] = {}
            self.last_clip_by_channel[channel_name][str(switch_number)] = clipslot
        except BaseException as e:
            self.log('ERROR: ' + str(e))

    def mf_change_bank(self, action_def, args):
        try:
            self.start_action('change_bank', args)
            bank_number = int(args) - 1
            self.trigger('MIDI CC 4 %s 127' % bank_number)
        except BaseException as e:
            self.log('ERROR change_bank: ' + str(e))

    def set_color_schema(self, args):
        self.start_action('set_color_schema', "")
        try:
            control_mode_color_schema = args
            result = ""
            for color_def in control_mode_color_schema:
                result = result + color(color_def[0], color_def[1]) + "\n"
                self.trigger(rgb_brightness(color_def[0], color_def[2]))
                self.trigger(ind_brightness(color_def[0], color_def[3]))
            self.trigger(result)
        except BaseException as e:
            self.log('ERROR set_color_schema  : ' + str(e))
