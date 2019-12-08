
def _make_member_desc(member_name, member):
    return '{} <{}>'.format(member_name, type(member).__name__)


def dumpobj(obj, show_callables=False):
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
    max_desc_len = max([len(_make_member_desc(k, v)) for k, v in members.items()])

    items = list(members.items())
    items.sort()
    for name, member in items:
        member_desc = _make_member_desc(name, member)
        txt += '  {} = {}\n'.format(member_desc.ljust(max_desc_len), member)

    return txt

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")