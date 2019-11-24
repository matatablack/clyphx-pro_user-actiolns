from functools import partial

from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import subject_slot

from ClyphX_Pro.clyphx_pro.MiscUtils import live_object_is_valid
from ClyphX_Pro.clyphx_pro.macrobat.ParameterRackBase import \
    parameter_value_to_macro_value
from ClyphX_Pro.clyphx_pro.osc.OSCElements import OSCElement


class BindingObserver(ControlSurfaceComponent):
    """
    BindingObserver handles observing the name and value of the parameter bound
    to a control and sending out OSC.

    For the parameter name, the address is of the form: /control_name/name
    For the parameter value, the address is of the form: /control_name/value
    For the parameter value as an int, the address is of the form: /control_name/int
    """

    def __init__(self, server, path, control, *a, **k):
        super(BindingObserver, self).__init__(*a, **k)
        self.is_private = True
        self._server = server
        self._path = path
        self._control = control
        self._on_parameter_changed.subject = control
        self._on_parameter_changed(control.parameter)

    def disconnect(self):
        super(BindingObserver, self).disconnect()
        self._server = None
        self._path = None
        self._control = None

    @subject_slot('parameter')
    def _on_parameter_changed(self, param):
        subject = self._control if live_object_is_valid(param) else None
        self._on_parameter_name_changed.subject = subject
        self._on_parameter_value_changed.subject = subject
        # using tasks here to thin out updates on parameter changes
        self._tasks.add(
            partial(self._on_parameter_name_changed, self._control.parameter_name))
        self._tasks.add(
            partial(self._on_parameter_value_changed, self._control.parameter_value))

    @subject_slot('parameter_name')
    def _on_parameter_name_changed(self, name, _=None):
        if not live_object_is_valid(self._control.parameter):
            name = '-'
        self._server.sendOSC('%s/name' % self._path, str(name))

    @subject_slot('parameter_value')
    def _on_parameter_value_changed(self, value, _=None):
        value_as_str = '-'
        value_as_int = 0
        if live_object_is_valid(self._control.parameter):
            # this is needed as some parameter values include special characters that
            # can't be converted to strings.  May want to add this to BindableElementMixin
            # in the next bindings update.
            value_as_str = ''.join(char for char in value if ord(char) < 128)
            # might be good to add this to bindings too.
            value_as_int = parameter_value_to_macro_value(self._control.parameter)
        self._server.sendOSC('%s/value' % self._path, str(value_as_str))
        self._server.sendOSC('%s/int' % self._path, int(value_as_int))


class OSCBindingViewerComponent(CompoundComponent):
    """
    OSCBindingViewerComponent creates BindingObservers for all of the bound controls
    of the first BindingComponent (the one owned by CXP). It also includes observers
    and OSC elements for sending out the name of the selected track and device.

    For track name, the address is /track/name
    For device name, the address is /device/name
    """

    def __init__(self, cx_core, *a, **k):
        self.create_actions = lambda: None
        super(OSCBindingViewerComponent, self).__init__(cx_core, *a, **k)
        self.is_private = True
        self._track_name_element = None
        self._device_name_element = None
        self.canonical_parent.schedule_message(2, self._do_init, cx_core)

    def disconnect(self):
        super(OSCBindingViewerComponent, self).disconnect()
        self._track_name_element = None
        self._device_name_element = None

    def _do_init(self, cx_core):
        # need to use scheduling here as user actions are created before the OSC server
        # and binding components.
        server = cx_core.osc_server
        bc = cx_core.get_binding_component(0)
        if server and bc:
            for i in xrange(bc.num_encoders):
                enc = bc.get_encoder(i)
                self.register_component(BindingObserver(server, '/%s' % enc.name, enc))
            for i in xrange(bc.num_buttons):
                btn = bc.get_button(i)
                self.register_component(BindingObserver(server, '/%s' % btn.name, btn))
            self._track_name_element = OSCElement(server, '/track/name')
            self._device_name_element = OSCElement(server, '/device/name')
            self.on_selected_track_changed()

    def on_selected_track_changed(self):
        if self._track_name_element and self._device_name_element:
            self._on_track_name_changed.subject = self._song.view.selected_track
            self._on_selected_device_changed.subject =\
                self._song.view.selected_track.view
            self._on_track_name_changed()
            self._on_device_name_changed()

    @subject_slot('name')
    def _on_track_name_changed(self):
        self._track_name_element.send_value(str(self._song.view.selected_track.name))

    @subject_slot('selected_device')
    def _on_selected_device_changed(self):
        dev = self._song.view.selected_track.view.selected_device
        self._on_device_name_changed.subject = dev if dev else None
        self._on_device_name_changed()

    @subject_slot('name')
    def _on_device_name_changed(self):
        dev = self._song.view.selected_track.view.selected_device
        name = dev.name if dev else '-'
        self._device_name_element.send_value(str(name))
