from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
from ClyphX_Pro.clyphx_pro.consts import DATA_HEADER
from template.TemplateBase import TemplateBase
import re

class Template(UserActionsBase):

    tpl = TemplateBase()

    def __init__(self, cx_core, *a, **k):
        super(Template, self).__init__(cx_core, *a, **k)
        self.tpl._do_init(self)

    def create_actions(self):
        self.add_global_action('tpl', self.dispatch)
        self.add_clip_action('get_clip', self.get_clip)
        self.add_track_action('get_track', self.get_track)
        self.add_global_action('recallsnap', self.recallsnap)
        """ FORUM USER ACTIONS """
        self.add_global_action('looplocs', self.loop_to_nearest_locs)
        self.add_global_action('loopstart', self.jump_loop_start)
        self.add_global_action('loopend', self.jump_loop_end)
        self.add_global_action('loc', self.jump_to_locator)
        self.add_global_action('hideall', self.hide_all_views)
        self.add_global_action('addmidi', self.add_midi_track)
        self.add_global_action('addaudio', self.add_audio_track)
        self.add_track_action('<track>', self.filter_action_tracks)
        self.add_track_action('HIDE', self.hide_or_reveal_grouped_tracks)

    def dispatch(self, _, args):
        trigger = self.canonical_parent.clyphx_pro_component.trigger_action_list
        self.tpl.dispatch(args, trigger)

    def get_clip(self, action_def, args):
        clip = action_def['clip']
        self.tpl.set_target_clip(clip)

    def get_track(self, action_def, args):
        track = action_def['track']
        self.tpl.set_target_track(track)
    
    def recallsnap(self, action_def, args):
        try:
            ident = args
            self.tpl.log('called recall snap with %s' % ident)
            if ident is not None:
                comp = self.canonical_parent.clyphx_pro_component
                data = self._song.get_data(DATA_HEADER % ident, None)
                if data:
                    comp.trigger_action_list('[%s] recall' % ident)
                    self.tpl.log('Recalling snap %s' % ident)
                else:
                    self.tpl.log('No data, cant recall snap %s' % ident)
        except BaseException as e:
            self.tpl.log('ERROR: ' + str(e))

    def on_selected_track_changed(self):
        self.tpl.on_selected_track_changed()
    
    def on_selected_scene_changed(self):
        self.tpl.on_selected_scene_changed()

    
    """
        Forum User Actions
    """

    """ HIDEALL """
    def hide_all_views(self, action_def, _):
        self.application().view.hide_view("Browser")
        self.application().view.hide_view("Detail")
        count = 0
        while count < 26:
            self.application().view.zoom_view(1, "", 1)
            count += 1

    """ ADDMIDI """
    def add_midi_track(self, action_def, args):
        if args == '':
            idx = None
        elif args == 'last':
            idx = -1
        else:
            idx = int(args) - 1
        self.song().create_midi_track(idx)

    """ ADDAUDIO """
    def add_audio_track(self, action_def, args):
        if args == '':
            idx = None
        elif args == 'last':
            idx = -1
        else:
            idx = int(args) - 1
        self.song().create_audio_track(idx)

    """ HIDE """
    def hide_or_reveal_grouped_tracks(self, action_def, args):
        track = action_def['track']
        track_idx = list(self.song().tracks).index(track)
        if self.song().tracks[track_idx].is_grouped == 1:
            grp_track = list(self.song().tracks).index(track.group_track) + 1
        else:
            grp_track = 0
        if args == '':
            action_string = '%s/FOLD' % (grp_track)
        if 'on' in args:
            action_string = '%s/FOLD ON' % (grp_track)
        if 'off' in args:
            action_string = '%s/FOLD OFF' % (grp_track)
        self.canonical_parent.clyphx_pro_component.trigger_action_list(action_string)


    """ LOOPLOCS """
    def loop_to_nearest_locs(self, action_def, _):
        cue_points = self.song().cue_points
        cue_points_num = len(cue_points)
        if cue_points_num > 0:
            current_time = self.song().current_song_time
            loop_start = current_time
            loop_end = self.song().last_event_time
            self.song().loop_length = 32.0
            for index in range(cue_points_num):
                cue_time = cue_points[index].time
                prev_cue_time = cue_points[index - 1].time
                last_cue_point = max(cue_time, prev_cue_time)
                if cue_time > current_time and cue_time <= loop_end:
                    loop_end = cue_time
            if current_time > last_cue_point:
                loop_start = last_cue_point
                loop_end = current_time
            loop_length = loop_end - loop_start
            self.song().loop_start = loop_start
            self.song().loop_length = loop_length

    """ LOOPSTART """
    def jump_loop_start(self, action_def, args):
        cue_points = self.song().cue_points
        cue_points_num = len(cue_points)
        current_loop_start = self.song().loop_start
        args = args.split()
        if args[0] == '>':
            self.song().loop_start += float(args[1])
            self.song().loop_length -= float(args[1])
        if args[0] == '<':
            self.song().loop_start -= float(args[1])
            self.song().loop_length += float(args[1])
        if args[0] == 'here':
            gap = self.song().loop_start - self.song().current_song_time
            self.song().loop_start = self.song().current_song_time
            self.song().loop_length += gap
        if args[0] == 'loc':
            if args[1] == '<':
                start_time = 0.0
                for index in range(cue_points_num):
                    cue_time = cue_points[index].time
                    if cue_time < current_loop_start and cue_time > start_time:
                        start_time = cue_time
                self.song().loop_start = start_time
                self.song().loop_length += current_loop_start - start_time
            if args[1] == '>':
                start_time = self.song().loop_start + self.song().loop_length
                for index in range(cue_points_num):
                    cue_time = cue_points[index].time
                    if cue_time > current_loop_start and cue_time < start_time:
                        start_time = cue_time
                self.song().loop_start = start_time
                self.song().loop_length -= start_time - current_loop_start

    """ LOOPEND """
    def jump_loop_end(self, action_def, args):
        cue_points = self.song().cue_points
        cue_points_num = len(cue_points)
        current_loop_end = self.song().loop_start + self.song().loop_length
        start_time = self.song().loop_start
        end_time = self.song().last_event_time
        args = args.split()
        if args[0] == '>':
            self.song().loop_length += float(args[1])
        if args[0] == '<':
            self.song().loop_length -= float(args[1])
        if args[0] == 'here':
            loop_end = self.song().loop_length + self.song().loop_start
            gap = self.song().current_song_time - loop_end
            self.song().loop_length += gap
        if args[0] == 'loc':
            if args[1] == '<':
                for index in range(cue_points_num):
                    cue_time = cue_points[index].time
                    if cue_time < current_loop_end and cue_time > start_time:
                        start_time = cue_time
                        self.song().loop_length = start_time - self.song().loop_start
            if args[1] == '>':
                for index in range(cue_points_num):
                    cue_time = cue_points[index].time
                    if cue_time > current_loop_end and cue_time <= end_time:
                        end_time = cue_time
                self.song().loop_length = end_time - self.song().loop_start

    """ LOC / Jump to locator """

    def jump_to_locator(self, action_def, args):
        cue_points = self.song().cue_points
        cue_points_num = len(cue_points)
        if args == '<<':
            if cue_points_num > 0:
                first_loc_time = 1000000.0
                for index in range(cue_points_num):
                    if cue_points[index].time < first_loc_time:
                        first_loc_time = cue_points[index].time
                        first_loc = index
                self.song().cue_points[first_loc].jump()
        if args == '<':
            self.song().jump_to_prev_cue()
        if args == '>':
            self.song().jump_to_next_cue()
        if args == '>>':
            if cue_points_num > 0:
                last_loc_time = 0.0
                for index in range(cue_points_num):
                    if cue_points[index].time > last_loc_time:
                        last_loc_time = cue_points[index].time
                        last_loc = index
                self.song().cue_points[last_loc].jump()
        if "'" in args:
            args = args.replace("'", '')
            for index in range(len(cue_points)):
                if args in self.song().cue_points[index].name:
                    cue_points[index].jump()
        if '"' in args:
            args = args.replace('"', '')
            for index in range(len(cue_points)):
                if args == self.song().cue_points[index].name:
                    cue_points[index].jump()

    """ TRACK FILTER ACTION """
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

