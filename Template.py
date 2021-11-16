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
        self.add_global_action('hideall', self.hide_all_views)
        self.add_global_action('addmidi', self.add_midi_track)
        self.add_global_action('addaudio', self.add_audio_track)
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




 

