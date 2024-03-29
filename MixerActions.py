
from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
from utils.log_utils import dumpobj
import re
import sys


class MixerActions(UserActionsBase):

    def create_actions(self):
        self.add_global_action('mixer_add', self.add)
        self.add_track_action('mixer_assign', self.assign)
        self.add_track_action('mixer_unassign', self.unassign)
        self.add_global_action('mixer_unbind', self.unbind_all)
        self.add_track_action('mixer_arm_assigned', self.arm_assigned)
        self.add_global_action('set_target_bus', self.set_target_bus)
        self.add_global_action('left_channel_mono_utility', self.left_channel_mono_utility)
        self.add_global_action('set_mixer_midi_volumes_binding', self.set_mixer_midi_volumes_binding)
        self.add_global_action('stop_playing', self.stop_playing)
        self.add_global_action('mixer_finish_execution', self.finish_execution)
        self.canonical_parent.log_message("ABLETON PYTHON Current Version: ------>>>>>", sys.version)

    dumpobj = dumpobj

    track_name_by_channel = {
        "1": "Kick",
        "2": "Minitaur",
        "3/4": "Drums",
        "5": "V. Bass",
        "6": "SH01A",
        "7": "TB3",
        "8": "Grandmother",
        "9/10": "Deepmind",
        "11/12": "Kurz",
        "13/14": "Yamaha",
        "15": "GTR",
        "16": "MIC",
        "17/18": "MASTER",
        "19/20": "Space",
        "21/22": "Timefactor",
        "23/24": "Deluge",
        "25/26":  "Pitchfactor"
    }

    group_by_knob = {
        "KNOB_1": "[KICK]",
        "KNOB_2": "[BASS]",
        "KNOB_3": "[DRUMS]",
        "KNOB_4": "[HITS]",
        "KNOB_5": "[MUSIC]",
        "KNOB_6": "[VOX]",
        "KNOB_7": "[ATMOSPHERE]",
        "KNOB_8": "[FX]",
        "KNOB_9": "[ALIENS]",
        "KNOB_10": "[UP]",
        "KNOB_11": "[REFERENCE]",
        "KNOB_12": "SEL/SEND"
    }

    bus_by_channel = {
        "1/2": "1",
        "3/4": "2",
        "5/6": "3",
        "7/8": "4",
        "9/10": "5",
        "11/12": "6",
        "13/14": "7",
        "15/16": "8",
        "midi": "midi"
    }

    is_execution_blocked = False
    current_action = None
    log = None
    trigger = None

    def check_thread_avalability_and_block(self, action_to_execute, args, dont_block=False):
        self.log = self.canonical_parent.log_message
        self.trigger = self.canonical_parent.clyphx_pro_component.trigger_action_list
        action = "%s %s" % (action_to_execute, args)
        self.canonical_parent.log_message('trying to execute ---> [%s]' % action)
        if dont_block:
            return
        if self.is_execution_blocked:
            msg = "Blocked, still executing [%s] action" % (
                self.current_action)
            self.canonical_parent.clyphx_pro_component.trigger_action_list(
                'msg "%s"' % msg)
            raise Exception(msg)
        else:
            self.current_action = action
            self.is_execution_blocked = True

    def finish_execution(self, action_def, args):
        self.is_execution_blocked = False
        self.current_action = None
        self.canonical_parent.log_message('Unblocking...')
        return

    def set_mixer_midi_volumes_binding(self, action_def, args):
        try:
            self.check_thread_avalability_and_block('set_mixer_midi_volumes_binding', args)

            self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC STR custom/global/action "set_mixer_midi_volumes_binding"')
            mixer_daw_volumes = """
                BIND FADER_1 "Kick"/VOL;
                BIND FADER_2 "Minitaur"/VOL;
                BIND FADER_3 "Drums"/VOL;
                BIND FADER_4 "Omni 1"/VOL;
                BIND FADER_5 "V. Bass"/VOL;
                BIND FADER_6 "SH01A"/VOL;
                BIND FADER_7 "TB3"/VOL;
                BIND FADER_8 "Grandmother"/VOL;
                BIND FADER_9 "Deepmind"/VOL;
                BIND FADER_10 "Omni 2"/VOL;
                BIND FADER_11 "GTR VOX"/VOL;
                BIND FADER_12 "BASS COMP"/VOL;
                BIND FADER_13 "Yamaha"/VOL;
                BIND FADER_14 "Omni 3"/VOL;
                BIND FADER_15 "GTR"/VOL;
                BIND FADER_16 "MIC"/VOL;
                BIND FADER_MIDI_1 "Omni 4"/VOL;
                BIND FADER_MIDI_2 "Deluge"/VOL;
                BIND FADER_MIDI_3 "Space"/VOL;
                BIND FADER_MIDI_4 "Timefactor"/VOL;
                mixer_finish_execution;
            """
            self.canonical_parent.clyphx_pro_component.trigger_action_list(mixer_daw_volumes)

        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))

    is_adding_midi = False

    def set_add_midi(self, action_def, args):
        args = args.split()
        value = args[0]
        self.is_adding_midi = True if value == "1" else False

        """
        @MidiFighter
        change MF control mode (defs.py)
    """

    def add(self, action_def, args):
        try:
            self.check_thread_avalability_and_block('add', args)
            args = args.split()
            channel = args[0]
            self.canonical_parent.clyphx_pro_component.trigger_action_list(
                'OSC STR custom/global/action "mixer_add %s"' % channel)

            if not self.is_adding_midi:
                output_track = self.get_output_track_by_channel(
                    channel)
                dictionary = {
                    'track_name': self.track_name_by_channel[channel],
                    'track_channel': channel,
                    'output': output_track.get("name"),
                    'color_index': output_track.get("color_index") + 1
                }

                actions = '''
                    OSC STR custom/global/msg 'Add {track_name}';
                    ADDAUDIO;
                    WAIT 1;
                    SEL/NAME "{track_name}";
                    SEL/IN "Ext. In";
                    WAIT 1;
                    SEL/INSUB "{track_channel}";
                    WAIT 1;
                    SEL/MON OFF;
                    SEL/COLOR {color_index};
                    SEL/ARM;
                    mixer_finish_execution;
                    OSC STR custom/global/msg "---";
                '''.format(**dictionary)

                self.canonical_parent.log_message(actions)
                self.canonical_parent.clyphx_pro_component.trigger_action_list(
                    actions)
            else:
                output_track = self.get_tracks_if_name_contains(
                    "(%s)(midi)" % channel)[0]
                dictionary = {
                    'track_name': self.track_name_by_channel[channel] + " [m]",
                    'track_channel': channel,
                    'output': output_track.get("name"),
                    'color_index': output_track.get("color_index") + 1
                }

                actions = '''
                    OSC STR custom/global/msg 'Add {track_name}';
                    ADDAUDIO;
                    WAIT 1;
                    SEL/NAME "{track_name}";
                    SEL/IN "Ext. In";
                    WAIT 1;
                    SEL/INSUB "{track_channel}";
                    WAIT 1;
                    SEL/MON OFF;
                    SEL/COLOR {color_index};
                    SEL/ARM;
                    mixer_finish_execution;
                    OSC STR custom/global/msg "---";
                '''.format(**dictionary)

                self.canonical_parent.log_message(actions)
                self.canonical_parent.clyphx_pro_component.trigger_action_list(
                    actions)

        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))

    """
    ASSIGN
    """

    def assign(self, action_def, args):
        try:
            self.check_thread_avalability_and_block('assign', args)
            track = action_def['track']
            track_idx = list(self.song().tracks).index(track) + 1
            args = args.split()
            channel = args[0].strip()
            is_midi = args[0] == "midi"

            self.canonical_parent.log_message(
                'channel---> %s' % channel)
            if args and channel:
                self.canonical_parent.clyphx_pro_component.trigger_action_list(
                    'OSC STR custom/global/action "mixer_assign %s"' % self.bus_by_channel[channel])

            if '[->>' in track.name and not is_midi:
                msg = 'Track Already Assigned'
                self.canonical_parent.log_message(msg)
                self.canonical_parent.clyphx_pro_component.trigger_action_list(
                    'mixer_finish_execution; msg "%s"; show_msg "%s";' % (msg, msg))
                return

            if not is_midi:
                if '[->' in track.name:
                    msg = 'Track Already Assigned'
                    self.canonical_parent.log_message(msg)
                    self.canonical_parent.clyphx_pro_component.trigger_action_list(
                        'mixer_finish_execution; msg "%s"; show_msg "%s";' % (msg, msg))
                    return

            if is_midi:
                fader_num = int(args[1])
                assigned_to = '[->> midi %s]' % fader_num
                tracks = self.get_tracks_if_name_contains(assigned_to)
                if len(tracks) > 0:
                    msg = 'Channel Already Assigned to %s -> Unassigning' % tracks[0].name
                    self.canonical_parent.log_message(msg)
                    self.canonical_parent.clyphx_pro_component.trigger_action_list(
                        'msg "%s"; show_msg "%s"' % (msg, msg))
                    self.canonical_parent.clyphx_pro_component.trigger_action_list(
                        'mixer_finish_execution; mixer_unassign midi %s;' % fader_num)
                    return
                elif '[->' in track.name:
                    self.canonical_parent.clyphx_pro_component.trigger_action_list(
                        'mixer_finish_execution;')
                    return

                dictionary = {
                    'track_idx': track_idx,
                    'track_name': ("%s %s" % (track.name.split(assigned_to)[0], assigned_to)).strip(),
                    'fader_num': fader_num,
                    'knob_3_index': fader_num,
                    'knob_2_index': fader_num + 4,
                    'knob_1_index': fader_num + 8
                }
                actions = '''
                    SEL/MUTE OFF;
                    SEL/NAME "{track_name}";
                    BIND FADER_MIDI_{fader_num} "{track_name}"/VOL;
                    BIND lp_arm_MIDI_{fader_num} "{track_name}"/ARM;
                    BIND lp_solo_MIDI_{fader_num} "{track_name}"/SOLO;
                    BIND lp_track_mute_MIDI_{fader_num} "{track_name}"/MUTE;
                    BIND lp_track_mono_util_MIDI_{fader_num} "{track_name}"/DEV("UtilityOnlyLeftChannel") "Device On";
                    BIND KNOB_{knob_1_index} "{track_name}"/PAN;
                    BIND KNOB_{knob_2_index} "{track_name}"/SEND B;
                    BIND KNOB_{knob_3_index} "{track_name}"/SEND A;
                    mixer_finish_execution;
                '''.format(**dictionary)
                self.canonical_parent.log_message(actions)
                self.canonical_parent.clyphx_pro_component.trigger_action_list(
                    actions)
            else:
                assigned_to = '[->%s]' % channel
                tracks = self.get_tracks_if_name_contains(assigned_to)
                if len(tracks) > 0:
                    msg = 'Channel Already Assigned to %s' % tracks[0].name
                    self.canonical_parent.log_message(msg)
                    self.canonical_parent.clyphx_pro_component.trigger_action_list(
                        'msg "%s"; mixer_finish_execution;' % msg)
                    return

                track_name = ("%s %s" % (track.name.split(
                    assigned_to)[0], assigned_to)).strip()
                dictionary = {
                    'track_idx': track_idx,
                    'track_name': track_name,
                    'channel': channel,
                    'dev_name': ("ToMixer%s.adv" % (channel.split('/')[0])),
                    'channel_first': channel.split('/')[0],
                    'origin_track_color_index': track.color_index + 1,
                    'return_track_name': '>' + track_name.split('[->')[0] + '[->>' + channel + ']'
                }
                actions = '''
                    SEL/MUTE ON;
                    SEL/NAME "{track_name}";
                    LOADUSER "{dev_name}";
                    WAIT 2;
                    INSAUDIO;
                    WAIT 3;
                    SEL/COLOR {origin_track_color_index};
                    SEL/INSUB "Post FX";
                    SEL/NAME "{return_track_name}";
                    BIND lp_arm_{channel_first} "{return_track_name}"/ARM;
                    BIND lp_solo_{channel_first} "{return_track_name}"/SOLO;
                    BIND lp_track_mute_{channel_first} "{return_track_name}"/MUTE;
                    BIND lp_track_mono_util_{channel_first} "{return_track_name}"/DEV("UtilityOnlyLeftChannel") "Device On";
                    BIND FADER_{channel_first} "{return_track_name}"/VOL;
                    mixer_finish_execution
                '''.format(**dictionary)
                self.canonical_parent.log_message(actions)
                self.canonical_parent.clyphx_pro_component.trigger_action_list(
                    actions)

        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))

    def unassign(self, action_def, args):
        try:
            self.check_thread_avalability_and_block('unassign', args)
            # self.canonical_parent.clyphx_pro_component.trigger_action_list('OSC STR custom/global/action "mixer_unassign %s"' % args)
            track = action_def['track']
            args = args.split() if args else []
            channel = args[0] if args else None
            if channel:
                self.canonical_parent.clyphx_pro_component.trigger_action_list(
                    'OSC STR custom/global/action "mixer_unassign %s"' % self.bus_by_channel[channel])

            assigned_prefix = '[->'
            assigned_prefix_2 = '[->>'

            channel = args[0].strip() if args else None
            is_midi = True if channel == "midi" else False
            midi_fader = args[1] if len(args) > 1 else None
            channel = ' ' + channel + ' %s' % midi_fader if is_midi else channel

            if channel:
                self.canonical_parent.log_message(
                    'PREFIX--> %s' % assigned_prefix + channel)
                tracks = self.get_tracks_if_name_contains(
                    assigned_prefix + channel)
                tracks = tracks + \
                    self.get_tracks_if_name_contains(
                        assigned_prefix_2 + channel)

            else:
                tracks = self.get_tracks_if_name_contains(
                    assigned_prefix)
            self.canonical_parent.log_message(
                'tracks qty: %s' % len(tracks))

            if len(tracks) == 0:
                self.canonical_parent.clyphx_pro_component.trigger_action_list(
                    "mixer_finish_execution;")

            for track in tracks:
                self.canonical_parent.log_message(
                    'unassining track %s' % track.name)
                search = re.search(r'\[->(.*?)\]', track.name)
                channel = search.group(1) if search else None
                is_midi = True if "midi" in channel else False

                self.canonical_parent.log_message(
                    'CHANNEL %s' % channel)

                channel_first = channel.split(
                    '/')[0].strip() if not is_midi else channel[-1]
                to_mixer_dev_name = 'ToMixer%s' % channel_first

                track_idx = list(self.song().tracks).index(track) + 1

                knob_1_message = ""
                knob_2_message = ""
                knob_3_message = ""
                if is_midi:
                    knob_3_index = int(channel_first) + 0
                    knob_2_index = int(channel_first) + 4
                    knob_1_index = int(channel_first) + 8
                    knob_3_message = 'BIND KNOB_%s "%s"/VOL;' % (
                        knob_3_index, self.group_by_knob['KNOB_%s' % knob_3_index])
                    knob_2_message = 'BIND KNOB_%s "%s"/VOL;' % (
                        knob_2_index, self.group_by_knob['KNOB_%s' % knob_2_index])
                    knob_1_message = 'BIND KNOB_%s "%s"/VOL;' % (
                        knob_1_index, self.group_by_knob['KNOB_%s' % knob_1_index])

                dictionary = {
                    'track_idx': track_idx,
                    'track_name': track.name.split(assigned_prefix)[0].strip(),
                    'dev_name': to_mixer_dev_name,
                    'channel': channel,
                    'channel_first': channel_first,
                    'is_midi_suffix': "MIDI_" if is_midi else "",
                    'knob_1_message': knob_1_message,
                    'knob_2_message': knob_2_message,
                    'knob_3_message': knob_3_message,
                }

                actions = '''
                    {track_idx}/NAME "{track_name}";
                    {track_idx}/DEV("{dev_name}") DEL;
                    {track_idx}/ARM OFF;
                    WAIT 1;
                    {knob_1_message}
                    {knob_2_message}
                    {knob_3_message}
                    WAIT 1;
                    BIND FADER_{is_midi_suffix}{channel_first} NONE;
                    BIND lp_arm_{is_midi_suffix}{channel_first} NONE;
                    BIND lp_solo_{is_midi_suffix}{channel_first} NONE;
                    BIND lp_track_mute_{is_midi_suffix}{channel_first} NONE;
                    BIND lp_track_mono_util_{is_midi_suffix}{channel_first} NONE;
                    mixer_finish_execution;
                '''.format(**dictionary)

                self.canonical_parent.log_message(actions)
                self.canonical_parent.clyphx_pro_component.trigger_action_list(
                    actions)

        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))

    def unbind_all(self, action_def, args):
        try:
            self.check_thread_avalability_and_block(
                'unbind_all', args)
            self.canonical_parent.clyphx_pro_component.trigger_action_list(
                'OSC STR custom/global/action "mixer_unbind %s"' % args)
            dictionary = {
                'track_idx': 0,
            }
            actions = '''
                    BIND KNOB_1 "[KICK]"/VOL
                    BIND KNOB_2 "[BASS]"/VOL
                    BIND KNOB_3 "[DRUMS]"/VOL
                    BIND KNOB_4 "[HITS]"/VOL
                    BIND KNOB_5 "[MUSIC]"/VOL
                    BIND KNOB_6 "[VOX]"/VOL
                    BIND KNOB_7 "[ATMOSPHERE]"/VOL
                    BIND KNOB_8 "[FX]"/VOL
                    BIND KNOB_9 "[ALIENS]"/VOL
                    BIND KNOB_10 "[UP]"/VOL
                    BIND KNOB_11 "[REFERENCE]"/VOL
                    BIND KNOB_12 SEL/SEND A;

                    BIND FADER_1 NONE;
                    BIND FADER_2 NONE;
                    BIND FADER_3 NONE;
                    BIND FADER_4 NONE;
                    BIND FADER_5 NONE;
                    BIND FADER_6 NONE;
                    BIND FADER_7 NONE;
                    BIND FADER_8 NONE;
                    BIND FADER_9 NONE;
                    BIND FADER_10 NONE;
                    BIND FADER_11 NONE;
                    BIND FADER_12 NONE;
                    BIND FADER_13 NONE;
                    BIND FADER_14 NONE;
                    BIND FADER_15 NONE;
                    BIND FADER_16 NONE;

                    BIND FADER_MIDI_1 NONE;
                    BIND FADER_MIDI_2 NONE;
                    BIND FADER_MIDI_3 NONE;
                    BIND FADER_MIDI_4 SEL/VOL;

                    BIND lp_arm_1 NONE;
                    BIND lp_arm_3 NONE;
                    BIND lp_arm_5 NONE;
                    BIND lp_arm_7 NONE;
                    BIND lp_arm_9 NONE;
                    BIND lp_arm_11 NONE;
                    BIND lp_arm_13 NONE;
                    BIND lp_arm_15 NONE;
                    BIND lp_arm_MIDI_1 NONE;
                    BIND lp_arm_MIDI_2 NONE;
                    BIND lp_arm_MIDI_3 NONE;
                    BIND lp_arm_MIDI_4 SEL/ARM;

                    BIND lp_solo_1 "[KICK]"/SOLO ;
                    BIND lp_solo_3 "[BASS]"/SOLO;
                    BIND lp_solo_5 "[DRUMS]"/SOLO;
                    BIND lp_solo_7 "[HITS]"/SOLO;
                    BIND lp_solo_9 "[MUSIC]"/SOLO;
                    BIND lp_solo_11 "[VOX]"/SOLO;
                    BIND lp_solo_13 "[ATMOSPHERE]"/SOLO;
                    BIND lp_solo_15 "[FX]"/SOLO;
                    BIND lp_solo_MIDI_1 NONE;
                    BIND lp_solo_MIDI_2 NONE;
                    BIND lp_solo_MIDI_3 NONE;
                    BIND lp_solo_MIDI_4 SEL/SOLO;

                    BIND lp_track_mute_1 NONE;
                    BIND lp_track_mute_3 NONE;
                    BIND lp_track_mute_5 NONE;
                    BIND lp_track_mute_7 NONE;
                    BIND lp_track_mute_9 NONE;
                    BIND lp_track_mute_11 NONE;
                    BIND lp_track_mute_13 NONE;
                    BIND lp_track_mute_15 NONE;
                    BIND lp_track_mute_MIDI_1 NONE;
                    BIND lp_track_mute_MIDI_2 NONE;
                    BIND lp_track_mute_MIDI_3 NONE;
                    BIND lp_track_mute_MIDI_4 SEL/MUTE;

                    BIND lp_track_mono_util_1 NONE;
                    BIND lp_track_mono_util_3 NONE;
                    BIND lp_track_mono_util_5 NONE;
                    BIND lp_track_mono_util_7 NONE;
                    BIND lp_track_mono_util_9 NONE;
                    BIND lp_track_mono_util_11 NONE;
                    BIND lp_track_mono_util_13 NONE;
                    BIND lp_track_mono_util_15 NONE;
                    BIND lp_track_mono_util_MIDI_4 SEL/DEV("UtilityOnlyLeftChannel") "Device On";

                    mixer_finish_execution;
            '''.format(**dictionary)

            self.canonical_parent.log_message(actions)
            self.canonical_parent.clyphx_pro_component.trigger_action_list(
                actions)

        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))

    def arm_assigned(self, action_def, args):
        try:
            self.check_thread_avalability_and_block(
                'arm_assigned', args)
            self.canonical_parent.clyphx_pro_component.trigger_action_list(
                'OSC STR custom/global/action "arm_all_assigned"')
            track = action_def['track']

            args = args.split()
            assigned_prefix = '[->>'
            tracks = self.get_tracks_if_name_contains(assigned_prefix)
            self.canonical_parent.log_message(
                'tracks qty: %s' % len(tracks))

            for track in tracks:
                track_idx = list(self.song().tracks).index(track) + 1
                dictionary = {'track_idx': track_idx}
                actions = '''
                    {track_idx}/ARM ON;
                '''.format(**dictionary)

                self.canonical_parent.log_message(actions)
                self.canonical_parent.clyphx_pro_component.trigger_action_list(
                    actions)

            self.canonical_parent.clyphx_pro_component.trigger_action_list(
                'mixer_finish_execution;')

        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))

    target_bus = None

    def set_target_bus(self, action_def, args):
        try:
            self.check_thread_avalability_and_block(
                'set_target_bus', args)
            channel = args.split()[0] if args else None
            self.target_bus = str(channel)
            self.canonical_parent.clyphx_pro_component.trigger_action_list(
                'OSC STR custom/global/action "set_target_bus %s"' % self.bus_by_channel[channel])
            self.canonical_parent.log_message(
                'TARGET BUS -----> %s' % channel)
            tracks = self.get_tracks_if_name_contains(
                '[->>%s' % channel)
            actions = ""
            if len(tracks) > 0:
                track_idx = list(self.song().tracks).index(
                    tracks[0]) + 1
                dictionary = {'track_idx': track_idx}
                actions = '''
                    {track_idx}/SEL;
                '''.format(**dictionary)
                self.canonical_parent.clyphx_pro_component.trigger_action_list(
                    actions)

            self.canonical_parent.clyphx_pro_component.trigger_action_list(
                'mixer_finish_execution;')

        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))

    def left_channel_mono_utility(self, action_def, args):
        try:
            self.check_thread_avalability_and_block(
                'left_channel_mono_utility', args)
            self.canonical_parent.clyphx_pro_component.trigger_action_list(
                'OSC STR custom/global/action "left_channel_mono_utility"')

            self.canonical_parent.log_message(
                '---TARGET BUS FROM MONO UTIL----> %s' % self.target_bus)
            tracks = self.get_tracks_if_name_contains(
                '[->>%s' % self.target_bus)
            actions = ""
            if len(tracks) > 0:
                track = tracks[0]
                track_idx = list(self.song().tracks).index(track) + 1
                track_was_mono = None

                for device in track.devices:
                    if device.name == "UtilityOnlyLeftChannel":
                        track_was_mono = True  # if device.is_active else None

                load_or_delete = '/DEV("UtilityOnlyLeftChannel") DEL;' if track_was_mono else '/DEV("UtilityOnlyLeftChannel") DEL; LOADUSER "UtilityOnlyLeftChannel.adv";'
                dictionary = {'track_idx': track_idx, 'load_or_delete': load_or_delete,
                              'channel_first': self.target_bus.split('/')[0]}
                actions = '''
                    {track_idx}/SEL;
                    {track_idx}{load_or_delete};
                    WAIT 2;
                    BIND lp_track_mono_util_{channel_first} {track_idx}/DEV("UtilityOnlyLeftChannel") "Device On";
                    mixer_finish_execution;
                '''.format(**dictionary)

                self.canonical_parent.clyphx_pro_component.trigger_action_list(
                    'show_msg "%s BUS -> MONO %s"' %
                    (self.bus_by_channel[self.target_bus],
                     'OFF' if track_was_mono else 'ON'))

                self.target_bus = None
                self.canonical_parent.log_message(actions)
                self.canonical_parent.clyphx_pro_component.trigger_action_list(
                    actions)
            else:
                self.canonical_parent.log_message(
                    '---> no track found for target bus -> %s ---' % self.target_bus)
                self.canonical_parent.clyphx_pro_component.trigger_action_list(
                    'mixer_finish_execution')

        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))

    def get_track_channel(self, track):
        search = re.search(r'\[(.*?)\]', track.name)
        return search.group(1) if search else None

    def get_track_prev_channel(self, track):
        search = re.search(r'--(.*?)--', track.name)
        return search.group(1) if search else None

    def get_tracks_if_name_contains(self, string):
        track_list = list(self.song().tracks)
        result_tracks = []
        for track in track_list:
            if string in track.name:
                result_tracks.append(track)
        return result_tracks

    def get_output_track_by_channel(self, channel):
        input_tracks_names_and_colors = {
            '1': {'name': 'Kick', 'color_index': 17},
            '2': {'name': 'Minitaur', 'color_index': 69},
            '3/4': {'name': 'Drums', 'color_index': 17},
            '5': {'name': 'V. Bass', 'color_index': 27},
            '6': {'name': 'SH01A', 'color_index': 50},
            '7': {'name': 'TB3', 'color_index': 9},
            '8': {'name': 'Grandmother', 'color_index': 25},
            '9/10': {'name': 'Deepmind', 'color_index': 65},
            '11/12': {'name': 'Kurz', 'color_index': 48},
            '13/14': {'name': 'Yamaha', 'color_index': 28},
            '15': {'name': 'GTR', 'color_index': 29},
            '16': {'name': 'MIC', 'color_index': 47},
            '17/18': {'name': 'MASTER', 'color_index': 64},
            '19/20': {'name': 'Timefactor', 'color_index': 0},
            '21/22': {'name': 'Pitchfactor', 'color_index': 63},
            '23/24': {'name': 'Deluge', 'color_index': 38},
            '25/26': {'name':  'Space', 'color_index': 22},
        }
        result = input_tracks_names_and_colors.get(channel)
        self.canonical_parent.log_message(dumpobj(result))
        return result

    def stop_playing(self, action_def, args):
        try:
            self.check_thread_avalability_and_block('stop_playing', args)
            self.song().stop_playing()
        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))

    def on_track_list_changed(self):
        self.canonical_parent.log_message('Track list changed..')
        track_list = list(self.song().tracks)
        # result_tracks = []
        # for track in track_list:
        #     if "Grandmother" in track.group_track.name:
        #          self.canonical_parent.log_message(dumpobj(track))
