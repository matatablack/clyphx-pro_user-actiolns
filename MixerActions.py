
from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
from utils.getters import selected_track 
from utils.log_utils import dumpobj
import re
import time

class MixerActions(UserActionsBase):

    def create_actions(self):
        self.add_global_action('mixer_add', self.add)
        self.add_global_action('mixer_monitor', self.monitor)
        self.add_global_action('daw_monitor', self.daw_monitor)
        self.add_track_action('mixer_assign', self.assign)
        self.add_track_action('mixer_unassign', self.unassign)
        self.add_track_action('mixer_unbind', self.unbind_all)


    dumpobj = dumpobj

    track_name_by_channel = { 
        "1": "[1] Kick", 
        "2": "[2] Minitaur", 
        "3/4": "[3/4] Drums", 
        "5": "[5] V. Bass", 
        "6": "[6] SH01A", 
        "7": "[7] TB3", 
        "8": "[8] Grandmother", 
        "9/10":"[9/10] Deepmind", 
        "11/12":"[11/12] Roland Go", 
        "13/14":"[13/14] Yamaha", 
        "15": "[15] GTR", 
        "16": "[16] MIC", 
        "17/18":"[17/18] MASTER", 
        "19/20":"[19/20] Space", 
        "21/22":"[21/22] Timefactor",
        "23/24":"[23/24] Deluge", 
        "25/26": "[25/26] Pitchfactor"
    }

    group_name_by_channel = { 
        "1": "KICK 1 [BUS]",
        "2": "BASS 2 [BUS]",
        "3/4": "DRUMS 3/4 [BUS]",
        "5/6": "HITS 5/6 [BUS]",
        "7/8": "MUSIC 7/8 [BUS]",
        "9/10": "VOX 9/10 [BUS]",
        "11/12": "ATMOSPHERE 11/12 [BUS]",
        "13/14": "FX 13/14 [BUS]",
        "15/16": "ALIENS 15/16 [BUS]",
        "MIDI_1": "UP MIDI_1 [BUS]"
    }

    def add(self, action_def, args):
        try:
            args = args.split()
            channel = args[0]
            self.canonical_parent.log_message('-----ADD-----')
            output_track = self.get_output_track_by_channel(channel)            
            dictionary = { 
                'track_name': self.track_name_by_channel[channel],
                'track_channel': channel,
                'output': output_track.name,
                'color_index': output_track.color_index + 1
            }
    
            actions = '''
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
            '''.format(**dictionary)

            self.canonical_parent.clyphx_pro_component.trigger_action_list(actions)


            
        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))



    """
    ASSIGN
        selected channel
        -> add external audio effect with audio to target mixer channel
        -> add "assigned" state on channel name 
        -> INSAUDIO o add track and set input from target mixer channel (return)
            name equals previous track name + resample
            monitor auto
            arm on
            bind fader_${target_channel} to sel/vol

    """
    def assign(self, action_def, args):
        try:
            self.canonical_parent.log_message('-----ASSIGN-----')
            track = action_def['track']
            track_idx = list(self.song().tracks).index(track) + 1
            args = args.split()
            channel = args[0]
            is_midi = args[0] == "midi"

            if is_midi: 
                fader_num = int(args[1])
                assigned_to = '[-> midi %s]' % fader_num
                tracks = self.get_tracks_if_name_contains(assigned_to)
                if len(tracks) > 0: 
                    self.canonical_parent.log_message('Channel Already Assigned to %s' % tracks[0].name)
                    return
                
                dictionary = { 
                    'track_idx': track_idx,
                    'track_name': ("%s %s" % (track.name.split(assigned_to)[0], assigned_to)),
                    'fader_num': fader_num,
                    'knob_1_index' : fader_num,
                    'knob_2_index' : fader_num + 4,
                    'knob_3_index' : fader_num + 8
                }
                actions = '''
                    SEL/NAME "{track_name}";
                    BIND FADER_MIDI_{fader_num} "{track_name}"/VOL;
                    BIND KNOB_{knob_1_index} "{track_name}"/PAN;
                    BIND KNOB_{knob_2_index} "{track_name}"/SEND B;
                    BIND KNOB_{knob_3_index} "{track_name}"/SEND A;
                '''.format(**dictionary)
                self.canonical_parent.log_message(actions)
                self.canonical_parent.clyphx_pro_component.trigger_action_list(actions)
            else: 
                assigned_to = '[-> %s]' % channel
                tracks = self.get_tracks_if_name_contains(assigned_to)
                if len(tracks) > 0: 
                    self.canonical_parent.log_message('Channel Already Assigned to %s' % tracks[0].name)
                    return

                dictionary = { 
                    'track_idx': track_idx,
                    'track_name': ("%s %s" % (track.name.split(assigned_to)[0], assigned_to)),
                    'channel': channel,
                    'dev_name': ("ToMixer%s.adv" % (channel.split('/')[0])), 
                    'channel_first': channel.split('/')[0],
                    'bus_channel': self.group_name_by_channel[channel],
                    # 'rec_channel': self.group_name_by_channel[channel],
                }       
                actions = '''
                    SEL/NAME "{track_name}";
                    SEL/MUTE;
                    LOADUSER "{dev_name}";
                    WAIT 3;           
                    INSAUDIO;
                    WAIT 3;  
                    SEL/INSUB "Post FX";         
                    BIND FADER_{channel_first} "From {track_name}"/VOL;
                    "{bus_channel}"/DEV("ToMixer") OFF;
                    "{bus_channel}"/DEV("ToMixer") MON IN;
                '''.format(**dictionary)
                self.canonical_parent.log_message(actions)
                self.canonical_parent.clyphx_pro_component.trigger_action_list(actions)
            
        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))




    def unassign(self, action_def, args):
        try:
            self.canonical_parent.log_message('-----UNNNNNNASSIGN-----')
            track = action_def['track']
            
            args = args.split()
            # channel = args[0]

            assigned_prefix = '[->'
            tracks = self.get_tracks_if_name_contains(assigned_prefix)
            for track in tracks:
                search = re.search(r'\[->(.*?)\]', track.name)
                channel = search.group(1) if search else None 
                channel_first = channel.split('/')[0]
                to_mixer_dev_name = 'ToMixer%s' % channel_first
                
                track_idx = list(self.song().tracks).index(track) + 1

                dictionary = { 
                    'track_idx': track_idx,
                    'track_name': track.name.split(assigned_prefix)[0],
                    'dev_name': to_mixer_dev_name,
                    'channel': channel,
                    'channel_first': channel_first,
                }

                actions = '''
                    {track_idx}/NAME "{track_name}";
                    {track_idx}/DEV("{dev_name}") DEL;
                    BIND FADER_{channel_first} NONE;
                    "KICK 1 [BUS]", "BASS 2 [BUS]", "DRUMS 3/4 [BUS]", "HITS 5/6 [BUS]", "MUSIC 7/8 [BUS]", "VOX 9/10 [BUS]", "ATMOSPHERE 11/12 [BUS]", "FX 13/14 [BUS]", "ALIENS 15/16 [BUS]"/DEV("ToMixer") ON;
                    "KICK 1 [BUS]", "BASS 2 [BUS]", "DRUMS 3/4 [BUS]", "HITS 5/6 [BUS]", "MUSIC 7/8 [BUS]", "VOX 9/10 [BUS]", "ATMOSPHERE 11/12 [BUS]", "FX 13/14 [BUS]", "ALIENS 15/16 [BUS]"/MON AUTO
                '''.format(**dictionary)


            self.canonical_parent.log_message(actions)

            self.canonical_parent.clyphx_pro_component.trigger_action_list(actions)
            
        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))

    def unbind_all(self, action_def, args):
        try:
            self.canonical_parent.log_message('-----UNBIND-----')
            track = action_def['track']
            track_idx = list(self.song().tracks).index(track) + 1
            dictionary = { 
                'track_idx': track_idx,
            }   
            actions = '''                  
                    BIND KNOB_1 "Bass [rec]"/PAN;
                    BIND KNOB_2 "Drums [rec]"/PAN;
                    BIND KNOB_3 "Hits [rec]"/PAN;
                    BIND KNOB_4 SEL/SEND A;
                    BIND KNOB_5 "Music [rec]"/PAN;
                    BIND KNOB_6 "Vox [rec]"/PAN;
                    BIND KNOB_7 "Atmosphere [rec]"/PAN;
                    BIND KNOB_8 SEL/SEND B;
                    BIND KNOB_9 "FX [rec]"/PAN;
                    BIND KNOB_10 "Aliens [rec]"/PAN;
                    BIND KNOB_11 "Up [rec]"/PAN;
                    BIND KNOB_12 SEL/PAN;

                    BIND FADER_1 "Kick [rec]"/VOL
                    BIND FADER_2 "Bass [rec]"/VOL
                    BIND FADER_3 "Drums [rec]"/VOL
                    BIND FADER_4 NONE
                    BIND FADER_5 "Hits [rec]"/VOL
                    BIND FADER_6 NONE
                    BIND FADER_7 "Music [rec]"/VOL
                    BIND FADER_8 NONE
                    BIND FADER_9 "Vox [rec]"/VOL
                    BIND FADER_10 NONE
                    BIND FADER_11 "Atmosphere [rec]"/VOL
                    BIND FADER_12 NONE
                    BIND FADER_13 "FX [rec]"/VOL
                    BIND FADER_14 NONE
                    BIND FADER_15 "Aliens [rec]"/VOL
                    BIND FADER_16 NONE

                    BIND FADER_MIDI_1 "Up [rec]"/VOL
                    BIND FADER_MIDI_2 "REFERENCE [rec]"/VOL
                    BIND FADER_MIDI_3 NONE
                    BIND FADER_MIDI_4 SEL/VOL
            '''.format(**dictionary)

            self.canonical_parent.log_message(actions)
            self.canonical_parent.clyphx_pro_component.trigger_action_list(actions)
            
        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))




    def monitor(self, action_def, args):
        try:
            self.canonical_parent.log_message('-----MONITOR-----')
            args = args.split()
            track_channel_id = args[0]
            monitor = args[1] == 'on'

            self.canonical_parent.log_message('track_channel_id: ' + track_channel_id)
            self.canonical_parent.log_message('monitor: %s' % monitor)

            tracks = self.get_tracks_if_name_contains('[%s]' % track_channel_id)
            not_armed_tracks = filter(lambda track: track.arm != 1, tracks)
            for track in not_armed_tracks:
                track_idx = list(self.song().tracks).index(track) + 1
                self.canonical_parent.log_message('track to apply mon: %s' % track.name)
                self.canonical_parent.log_message('track idx: %s' % track_idx)
                self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/mixer_assign %s' % (track_idx, 'master' if monitor else 'prev'))            
        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))


    def daw_monitor(self, action_def, args):
        try:
            self.canonical_parent.log_message('-----DAW MONITOR-----')
            args = args.split()
            track_channel_id = args[0].replace('"', "")
            monitor = args[1] == 'on'

            self.canonical_parent.log_message('track_channel_id: ' + track_channel_id)
            self.canonical_parent.log_message('monitor: %s' % monitor)

            tracks = self.get_tracks_if_name_contains('(%s)' % track_channel_id)
            for track in tracks:
                track_idx = list(self.song().tracks).index(track) + 1
                self.canonical_parent.log_message('track to apply mon: %s' % track.name)
                self.canonical_parent.log_message('track idx: %s' % track_idx)
                self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/DEV(1) P1 %s' % (track_idx, "127" if monitor else "0"))
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
        return self.get_tracks_if_name_contains("(%s)" % channel)[0]

    def on_track_list_changed(self):
        self.canonical_parent.log_message('Track list changed..')
        # track_list = list(self.song().tracks)
        # # result_tracks = []
        # for track in track_list:
        #     if track.is_grouped and "[BUS]" in track.group_track.name:
        #          self.canonical_parent.log_message(dumpobj(track))