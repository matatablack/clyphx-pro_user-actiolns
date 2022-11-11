from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase


class TrackNumbersToVariables(UserActionsBase):
    """
 As you can see here, this project contains 4 major groups which I call "FAM", short for "instrument families". These groups are defined as any group track which itself isn't grouped (aka non-nested group track). Moreover, each of these FAMs contain a certain number of instruments (any non-group track). By default, this action will create 5 variables for each FAM's instruments, whether or not they actually contain 5 instruments (as we'll see later on, you can change this setting). As you can see from the first variable, the first non-nested group track of this project is Track 1 (%FAM_0%). The track number of the 3 other non-nested group tracks are assigned right after. Next, we see that our first group (%FAM_0%) contains instruments on tracks 2, 3, 4 and 5, so a total of 4 non-group tracks. The reason why I want variables all the way to 5 even though there are less than 5 instruments is that in my set-up I need to fill those references even though they don't exist (don't worry if it's over your head). Now, turn your attention to the FAM_3 instruments. Here, you see that FAM 3 has its first instrument on Track 14, its 2nd on track 15 and its 3rd on track...17. This is because track 16 is a group track, aka a sub-group because it's nested inside FAM 3 group track, hence why it isn't declared as a FAM variable. You can also see that FAM 3 contains more than 5 instruments, since variable %FAM_3_LAST% is assigned to a track number higher than %FAM_3_INS_5%.

So now it's possible to create a set-up of controls which actions refer to tracks depending on their structure and organization, rather than by exact track number or name. Moreover, as we'll see later on, this action can be automatically triggered every time there is a track list change. Which means if you change track order or add a new track, your variables will automatically be updated!

Arguments:
ALL or "Fam Track Name" (required) : you can choose to assign variables for all tracks of your project or only for one specific family (non-nested group). In this way, you can change the way you want to assign variables for each family.
AUDIO, MIDI, ARM or ALL (required) : determine what kind of track gets defined as an instrument track. Only AUDIO tracks, only MIDI, all ARMable tracks (if tracks has no input then it well get ignored) or ALL non-group tracks (so even tracks with no input) can be selected.
SUB (optional) : if you have lots of sub-groups inside your family groups, you can optionally add SUB as a 3rd argument and only the first instrument of each sub-group will be assigned to variables, rather than all instruments.
+1 or -1 : (optional) : you can add this argument if you wish to offset the FAM indices positively or negatively.

You can also have a single argument named CLEAR in order to assign track -1 to all variables.

Examples:

[] TRACKVAR ALL ALL

Assign track numbers to variables for all tracks. Instruments are defined as any non-group track.

[] TRACKVAR "SYNTHS" MIDI

Assign track numbers to variables for non-nested group called "SYNTHS". Instruments are defined as any MIDI track.

[] TRACKVAR "STRINGS" ARM SUBS

Assign track numbers of first instruments of each sub-group inside the non-nested group called "STRINGS". Instruments are defined as any track that can be armed.

[] TRACKVAR ALL ALL SUBS -1

Assign track numbers of first instruments of each sub-group of all non-nested groups. Offset the non-nested groups numbers by -1.


Advanced:

There are additional settings which you can configure at the beginning of the code. These settings are mostly dependent on each one's setup and most likely won't change from project to project. You can change the max number of instrument variables to assign, log the variables to Live's log.txt file, among others.
If you wish to automatically update the variables on every track list change, simply create a macro called $default_trackvar$ and call the action with the arguments of your choice.
    """

    def create_actions(self):
        """ Create the action.  We define it as a global action since it's not specific
        to a track, device or clip. """
        self.add_track_action('trackvar', self.assign_track_numbers_to_variables)

  
    def assign_track_numbers_to_variables(self, action_def, args):
        max_ins_and_grps = 12            # max number of instruments and groups assigned
        fill_to_max = 0                 # create variables for missing instruments and groups until max_ins_and_grps number is reached
        create_last_track_fam = 1       # create a family variable assigned to the last track
        log_variable_assignments = 1    # print to log file
        track = self.song().tracks
        args = args.replace('"', '')
        args = args.split()
        if len(args) == 2:
            sub_mode = 0
            fam_count_offset = 0
        elif len(args) == 3:
            if args[2] == 'sub':
                sub_mode = 1
                fam_count_offset = 0
            else:
                sub_mode = 0
                fam_count_offset = int(args[2])
        elif len(args) == 4:
            sub_mode = 1
            fam_count_offset = int(args[3])
        else:   # 1 arg
            sub_mode = 0
            fam_count_offset = 0
            args.append('all')
        fam_idx_list = [len(self.song().tracks)]
        fam_count = 0
        sel_fam_count = -2
        for index in range(len(self.song().tracks)):
            if track[index].is_foldable == 1 and track[index].is_grouped == 0:
                if args[0] == 'all' or args[0] == 'clear':
                    track_number = (index + 1 if args[0] != 'clear' else -1)
                    action_string = '%%FAM_%i%% = %i' % (fam_count - fam_count_offset + 1, track_number)
                    self.canonical_parent.clyphx_pro_component.trigger_action_list(action_string)
                    if log_variable_assignments == 1: self.canonical_parent.log_message(action_string)
                    fam_idx_list.insert(fam_count, index)
                else:
                    if args[0] == track[index].name:
                        action_string = '%%FAM_%i%% = %i' % (fam_count - fam_count_offset + 1, index + 1)
                        self.canonical_parent.clyphx_pro_component.trigger_action_list(action_string)
                        if log_variable_assignments == 1: self.canonical_parent.log_message(action_string)
                        fam_idx_list.insert(0, index)
                        sel_fam_count = fam_count
                    if fam_count == sel_fam_count + 1:
                        fam_idx_list[1] = index
                fam_count += 1
        if create_last_track_fam == 1 and args[0] == 'all':
            track_number = (len(self.song().tracks) if args[0] != 'clear' else -1)
            action_string = '%%FAM_%i%% = %i' % (fam_count - fam_count_offset + 1, track_number)
            self.canonical_parent.clyphx_pro_component.trigger_action_list(action_string)
            if log_variable_assignments == 1: self.canonical_parent.log_message(action_string)
        for fam in range(len(fam_idx_list) - 1):
            grp_count = 0
            for index in range(fam_idx_list[fam], fam_idx_list[fam + 1]):
                if track[index].is_foldable == 1 and track[index].is_grouped == 1 and grp_count < max_ins_and_grps:
                    fam_count = (fam if args[0] == 'all' or args[0] == 'clear' else sel_fam_count)
                    track_number = (index + 1 if args[0] != 'clear' else -1)
                    action_string = '%%FAM_%i_GRP_%i%% = %i' % (fam_count - fam_count_offset + 1, grp_count + 1, track_number)
                    self.canonical_parent.clyphx_pro_component.trigger_action_list(action_string)
                    if log_variable_assignments == 1: self.canonical_parent.log_message(action_string)
                    grp_count += 1
            if grp_count > 0 and fill_to_max == 1:
                while grp_count < max_ins_and_grps:
                    track_number = (fam_idx_list[fam + 1] + 1 if args[0] != 'clear' else -1)
                    action_string = '%%FAM_%i_GRP_%i%% = %i' % (fam_count - fam_count_offset + 1, grp_count + 1, track_number)
                    self.canonical_parent.clyphx_pro_component.trigger_action_list(action_string)
                    if log_variable_assignments == 1: self.canonical_parent.log_message(action_string)
                    grp_count += 1
            sub_condition = (0 if sub_mode == 1 else 1)
            ins_count = 0
            for index in range(fam_idx_list[fam], fam_idx_list[fam + 1]):
                if args[1] == 'audio':
                    type_condition = (1 if track[index].has_audio_input == 1 and track[index].is_foldable == 0 else 0)
                elif args[1] == 'midi':
                    type_condition = track[index].has_midi_input
                elif args[1] == 'arm':
                    type_condition = track[index].can_be_armed
                elif args[1] == 'all':
                    type_condition = (1 if track[index].is_foldable == 0 else 0)
                if type_condition == 1 and sub_condition == 1:
                    fam_count = (fam if args[0] == 'all' or args[0] == 'clear' else sel_fam_count)
                    if ins_count < max_ins_and_grps:
                        track_number = (index + 1 if args[0] != 'clear' else -1)
                        action_string = '%%FAM_%i_INS_%i%% = %i' % (fam_count - fam_count_offset + 1, ins_count + 1, track_number)
                        self.canonical_parent.clyphx_pro_component.trigger_action_list(action_string)
                        if log_variable_assignments == 1: self.canonical_parent.log_message(action_string)
                        ins_count += 1
                if sub_mode == 1:
                    sub_condition = (1 if track[index].is_foldable == 1 and track[index].is_grouped == 1 else 0)
                else:
                    sub_condition = 1
            if ins_count > 0 and fill_to_max == 1:
                while ins_count < max_ins_and_grps:
                    track_number = (index + 1 if args[0] != 'clear' else -1)
                    action_string = '%%FAM_%i_INS_%i%% = %i' % (fam_count - fam_count_offset + 1, ins_count + 1, track_number)
                    self.canonical_parent.clyphx_pro_component.trigger_action_list(action_string)
                    if log_variable_assignments == 1: self.canonical_parent.log_message(action_string)
                    ins_count += 1
            track_number = (index + 1 if args[0] != 'clear' else -1)
            action_string = '%%FAM_%i_LAST%% = %i' % (fam_count - fam_count_offset + 1, track_number)
            self.canonical_parent.clyphx_pro_component.trigger_action_list(action_string)
            if log_variable_assignments == 1: self.canonical_parent.log_message(action_string)
        if log_variable_assignments == 1: self.canonical_parent.log_message('------------------------------------------')