from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase



class LocActions(UserActionsBase):
    """
    Shift
    """

    def create_actions(self):
        """ Create the action.  We define it as a global action since it's not specific
        to a track, device or clip. """
        self.add_global_action('loc', self.jump_to_locator)

  
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

