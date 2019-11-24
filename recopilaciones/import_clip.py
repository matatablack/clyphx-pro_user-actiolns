#!/usr/bin/env python
"""
MIT License

Copyright (c) 2019 Piotr Styk <polfilm@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import live
import os
import yaml
import yamlordereddictloader

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class ImportClip(object):

    set = None
    track = None
    clip = None

    def __init__(self):

        self.connect()
        #self.debug_track_access_assume_first_is_midi()

    def connect(self):
        self.set = live.Set()
        self.set.scan(scan_clip_names = True, scan_devices = True)

    def set_tempo(self, in_tempo):
        self.set.tempo = in_tempo

    def ctl_insert_record_4bars_at_index(self, index):
        self.set.create_clip(0, index, 4)
        self.set.set_clip_name(0, index, "[4BARS] 3/RECFIX 4 {0} ; WAITS 4B ; SCENE >".format(index))
        device_list = self.set.get_device_list(1)
        device_parameters = self.set.get_device_parameters(1, 0)
        pass

    def debug_track_access_assume_first_is_midi(self):
        self.track = self.set.tracks[0]
        print("Track name %s" % self.track.name)

    def debug_clip_access(self):
        # only if clip exists
        self.clip = self.track.clips[0]
        print("Clip name %s, length %d beats" % (self.clip.name, self.clip.length))

    def play(self):
        self.clip.play()

    def add_clip(self):
        # track_index, clip_index, length
        self.set.create_clip(0, 0, 4)

        # since references by value not ref, we need to reload
        self.debug_set_access()
        self.debug_track_access_assume_first_is_midi()

        # verify
        self.debug_clip_access()

    def add_note(self):
        example_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ex001.4bars.yaml")
        data = None
        if os.path.isfile(example_file):
            data = yaml.load(open(example_file), Loader=yamlordereddictloader.Loader)


        print (data)
        # note position duration velocity
        self.clip.add_note(60, 0, 0.25, 60)
        self.clip.add_note(60, 1, 0.25, 10)
        self.clip.add_note(60, 2, 0.25, 120)
        self.clip.add_note(61, 3, 1, 120)

    def get_clip(self):
        #clips = self.set.get /live/name/clip
        #track3 = self.set.tracks[2]
        #tempo = self.set.get_tempo()
        #clip10 = self.set.get_clip_name(2, 1)
        #set_filename = self.set._get_last_opened_set_filename()
        #a = self.set.currently_open()

        from randomnames import random_namepair
        print ("random: {}".format(random_namepair()))
        from fourbars.als_parser import AlsParser

        als_filename = '../un/Piotrek173-ClyphxSessions.als.xml'
        alsparser = AlsParser(als_filename)

        for asset in alsparser.track.clipslots:
            print (asset.clip_name, asset.file_abs)
        pass
'''
        import xml.etree.ElementTree as ET
        root = ET.parse('../un/Piotrek173-ClyphxSessions.als.xml').getroot()
        for audiotrack in root.findall('LiveSet/Tracks/AudioTrack'):
            track_name = audiotrack.findall('Name/EffectiveName')[0].get('Value')
            pos = 0
            for clipslot in audiotrack.findall('DeviceChain/MainSequencer/ClipSlotList'):
                pos += 1
                clip_filename = clipslot.findall('ClipSlot/ClipSlot/Value/AudioClip/SampleRef/FileRef/Name')[0].get('Value')
                clip_name = clipslot.findall('ClipSlot/ClipSlot/Value/AudioClip/Name')[0].get('Value')
                clip_fullpath = ""
                for folder in clipslot.findall('ClipSlot/ClipSlot/Value/AudioClip/SampleRef/FileRef/SearchHint/PathHint/RelativePathElement'):
                    clip_fullpath = clip_fullpath + "/" + folder.get('Dir')
                clip_fullpath + "/" + clip_filename
                pass
'''
