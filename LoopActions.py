from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase 
from utils.log_utils import dumpobj

class LoopActions(UserActionsBase):
    """
    Loopactions
    """

    def create_actions(self):
        """ Create the action.  We define it as a global action since it's not specific
        to a track, device or clip. """
        self.add_global_action('looplocs', self.loop_to_nearest_locs)
        self.add_global_action('loopstart', self.jump_loop_start)
        self.add_global_action('loopend', self.jump_loop_end)


    """ LOC / Jump to locator """

    dumpobj = dumpobj

    """ LOOPLOCS """
    def loop_to_nearest_locs(self, action_def, _):
        try:
            cue_points = self.song().cue_points
            cue_points_num = len(cue_points)
            # self.canonical_parent.log_message(dumpobj(self.song().view.selected_track))
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
        except BaseException as e:
            self.canonical_parent.log_message('ERROR: ' + str(e))


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