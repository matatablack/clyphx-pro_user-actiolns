from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
from utils.getters import selected_track 
from utils.log_utils import dumpobj
import re

class MixerActions(UserActionsBase):

    def create_actions(self):
        self.add_global_action('mixer_add', self.add)
        self.add_global_action('mixer_monitor', self.monitor)
        self.add_track_action('mixer_assign', self.assign)


    dumpobj = dumpobj

    track_name_by_channel = { 
        "1/2": "[1/2] Drums", 
        "3": "[3] Kick", 
        "4": "[4] Minitaur", 
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
        "25/26": "[25/26] something"
    }

    def add(self, action_def, args):
        try:
            args = args.split()
            channel = args[0]
            self.canonical_parent.log_message('-----ADD-----')
            # self.canonical_parent.trigger_action_list('[%s] recall' % ident)
            # self.canonical_parent.log_message(dumpobj(self.song().view.selected_track))
            tracks = self.get_tracks_if_name_contains(channel)
            self.canonical_parent.log_message(channel)
            self.canonical_parent.clyphx_pro_component.trigger_action_list('msg "testing!!!! %s"' % tracks[0].name)

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
                SEL/OUT "{output}";
                SEL/ARM;
                SEL/MON OFF;
                SEL/COLOR {color_index}
            '''.format(**dictionary)

            self.canonical_parent.clyphx_pro_component.trigger_action_list(actions)

            # selected_track = self.song().view.selected_track
            #put into arrange group?

            
        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))

    """
        to do -> if not mixer group and 
    """
    def assign(self, action_def, args):
        try:
            self.canonical_parent.log_message('-----ASSIGN-----')
            track = action_def['track']
            track_idx = list(self.song().tracks).index(track) + 1
            args = args.split()
            channel = args[0]
            output_track = None
            if channel == 'origin':
                origin_channel = self.get_track_channel(track)
                # self.canonical_parent.log_message("origin channel -> %s" % origin_channel)
                output_track = self.get_output_track_by_channel(origin_channel).name if origin_channel else None

            if channel == 'prev':
                prev_out = self.get_track_prev_channel(track)
                # self.canonical_parent.log_message("prev out -> %s" % prev_out)
                output_track = prev_out if prev_out else None

            if channel == 'master':
                output_track = "Master"


            current_out = track.output_routing_type.display_name.encode('utf8')
            prev_out = current_out

            self.canonical_parent.log_message("current out -> %s" % current_out)
            self.canonical_parent.log_message("prev out -> %s" % prev_out)
            
            dictionary = { 
                'track_idx': track_idx,
                'output_track': output_track if output_track != None else self.get_output_track_by_channel(channel).name,
                'track_name': ("%s --%s--" % (track.name.split(' --')[0], prev_out))
            }

            actions = '''
                {track_idx}/OUT "{output_track}";
                {track_idx}/NAME "{track_name}";
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
            for track in tracks:
                track_idx = list(self.song().tracks).index(track) + 1
                self.canonical_parent.log_message('track to apply mon: %s' % track.name)
                self.canonical_parent.log_message('track idx: %s' % track_idx)
                self.canonical_parent.clyphx_pro_component.trigger_action_list('%s/mixer_assign %s' % (track_idx, 'master' if monitor else 'prev'))            
        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))


    def on_track_list_changed(self):
        self.canonical_parent.log_message('Track list changed..')


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
     

"""     def apply_if_clip_name_contains(self, action_def, args):
     
        arg_split = args.split()
        track_list = list(self.song().tracks)
        for track in track_list:
            if arg_split[0] in track.name:
                action = '%s/%s' % (track_list.index(track) + 1, ' '.join(arg_split[1:]))
                self.canonical_parent.clyphx_pro_component.trigger_action_list(action)
 """


    