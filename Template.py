from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
from template.TemplateBase import TemplateBase

""" The number of X-Controls to add shift functionality to. """
NUM_X_CONTROLS = 100


class Template(UserActionsBase):
    """
        # def on_selected_track_changed(self):
    #     # trigger = self.canonical_parent.clyphx_pro_component.trigger_action_list
    #     track = self.song().selected_track
    #     self.canonical_parent.show_message('new track name: %s' % track.name)
        def record_midi_to_audio(self, action_def, args):
        track = action_def['track']
        track.arm.value = True
        self.canonical_parent.show_message('track name is')

        MSG \"HOLA %s\"

    """

    tpl = TemplateBase()

    def __init__(self, cx_core, *a, **k):
        super(Template, self).__init__(cx_core, *a, **k)
        self.tpl.doInit(self)

    def create_actions(self):
        self.add_global_action('tpl', self.entryPointHandler)
        self.add_global_action('dumpall', self.dumpall_cmd)
        self.add_global_action('dumptree', self.dumptree_cmd)

    def entryPointHandler(self, _, args):
        self.tpl.dispatch(args)

    def on_selected_track_changed(self):
        # self.tpl.set_selected_track(self.song().view.selected_track)
        self.dumpall_cmd(self.song().view.selected_track)

    def dumpall_cmd(self, obj):
        txt = ''
        txt += '\n' + self._dumpobj(obj, False)
        self.canonical_parent.log_message(txt)

    def dumptree_cmd(self, _, args):
        """Dump basic song, song view, track, clip info"""
        t = '\n'
        song = self.song()
        t += 'Song: length:%.f cur:%.f playing:%s tempo:%.f\n' % (
        song.song_length, song.current_song_time, song.is_playing, song.tempo)
        sel_trk = song.view.selected_track
        sel_scene = song.view.selected_scene
        hilited_clip = '<empty slot>' if song.view.highlighted_clip_slot.clip is None else song.view.highlighted_clip_slot.clip.name
        t += 'Song view: selTrk:%s selScene:%s selClip:%s\n' % (sel_trk.name, sel_scene.name, hilited_clip)
        for track in song.tracks:
            t += '    track %s\n' % track.name
            for slot in track.clip_slots:
                tag = '' if slot.clip is None else slot.clip.name
                t += '        clipslot %s\n' % tag

        self.canonical_parent.log_message(t)


    #################### Supporting code
    def _make_member_desc(self, member_name, member):
        return '{} <{}>'.format(member_name, type(member).__name__)


    def _dumpobj(self, obj, show_callables=False):
        '''A debugging function that prints out the names and values of all the
        members of the given object.  Very useful for inspecting objects in
        interactive sessions'''
        txt = 'TYPE: %s\n' % type(obj).__name__

        members = {}
        for name in dir(obj):
            try:
                members[name] = getattr(obj, name)
            except Exception as e:
                members[name] = 'EXCEPTION getting value: %s - %s' % (type(e), str(e))

        members = {name: member for name, member in members.items()
                if name not in ('__builtins__', '__doc__')}
        members = {name: member for name, member in members.items()
                if not name.startswith('__') and not name.endswith('__')}
        if not show_callables:
            members = {name: member for name, member in members.items()
                    if not callable(member)}
        if len(members) == 0:
            txt += '  <EMPTY>\n'
            return txt
        max_desc_len = max([len(self._make_member_desc(k, v)) for k, v in members.items()])

        items = list(members.items())
        items.sort()
        for name, member in items:
            member_desc = self._make_member_desc(name, member)
            txt += '  {} = {}\n'.format(member_desc.ljust(max_desc_len), member)

        return txt
