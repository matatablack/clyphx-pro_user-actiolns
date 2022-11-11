from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase


class TrackActionFilter(UserActionsBase):
    """
    ShiftAction crea+
    """

    def create_actions(self):
        """ Create the action.  We define it as a global action since it's not specific
        to a track, device or clip. """
        self.add_track_action('<track>', self.filter_action_tracks)

  
    def filter_action_tracks(self, action_def, args):
        track = action_def['track']
        arg_split = []
        x_mode = 0
        for a in re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', args):
            if 'dev' in a:
                arg_split.append('dev(%s)' % a.replace('dev', ''))
            elif 'clip' in a:
                arg_split.append('clip(%s)' % a.replace('clip', ''))
            elif a == '>':
                pass
            elif a == 'x':
                x_mode = 1
            else:
                arg_split.append(a)
        arg_split[0] = arg_split[0].replace('>', '')
        if x_mode == 0:
            if arg_split[0] == 'grps':
                if action_def['track'].is_foldable == 1:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
            if arg_split[0] == 'armed':
                if action_def['track'].arm == 1:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
            if arg_split[0] == 'audio':
                if action_def['track'].has_audio_input == 1:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
            if arg_split[0] == 'midi':
                if action_def['track'].has_midi_input == 1:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
            if arg_split[0] == 'monin':
                if action_def['track'].current_monitoring_state == 0:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
            if arg_split[0] == 'monauto':
                if action_def['track'].current_monitoring_state == 1:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
            if arg_split[0] == 'monoff':
                if action_def['track'].current_monitoring_state == 2:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
            if '+' in arg_split[0] or '-' in arg_split[0]:
                track_index = list(self.song().tracks).index(action_def['track']) + int(arg_split[0]) + 1
                action = '%s/%s' % (track_index, ' '.join(arg_split[1:]))
            if "'" in arg_split[0]:
                arg_split[0] = arg_split[0].replace("'", "")
                if arg_split[0] in action_def['track'].name:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
            if '"' in arg_split[0]:
                arg_split[0] = arg_split[0].replace('"', '')
                if arg_split[0] == action_def['track'].name:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
        else:
            if arg_split[0] == 'grps':
                if action_def['track'].is_foldable != 1:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
            if arg_split[0] == 'armed':
                if action_def['track'].arm != 1:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
            if arg_split[0] == 'audio':
                if action_def['track'].has_audio_input != 1:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
            if arg_split[0] == 'midi':
                if action_def['track'].has_midi_input != 1:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
            if arg_split[0] == 'monin':
                if action_def['track'].current_monitoring_state != 0:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
            if arg_split[0] == 'monauto':
                if action_def['track'].current_monitoring_state != 1:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
            if arg_split[0] == 'monoff':
                if action_def['track'].current_monitoring_state != 2:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
            if "'" in arg_split[0]:
                arg_split[0] = arg_split[0].replace("'", "")
                if arg_split[0] not in action_def['track'].name:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
            if '"' in arg_split[0]:
                arg_split[0] = arg_split[0].replace('"', '')
                if arg_split[0] != action_def['track'].name:
                    action = '"%s"/%s' % (track.name, ' '.join(arg_split[1:]))
        self.canonical_parent.clyphx_pro_component.trigger_action_list(action)