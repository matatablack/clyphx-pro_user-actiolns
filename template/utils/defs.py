drum_machine_names_mapping_array = ["Kick", "Snare", "CHH", "Perc"]

default_binding = """ 
    bind mf_b1_e1 sel/send A;
    bind mf_b1_e2 sel/send B;
    bind mf_b1_e3 sel/send C;
    bind mf_b1_e4 NONE;
    bind mf_b1_e5 sel/vol;
    bind mf_b1_e6 sel/pan;
    bind mf_b1_e7 NONE;
    bind mf_b1_e8 NONE;
    bind mf_b1_e9 sel/dev(sel) p1;
    bind mf_b1_e10 sel/dev(sel) p2;
    bind mf_b1_e11 sel/dev(sel) p3;
    bind mf_b1_e12 sel/dev(sel) p4;
    bind mf_b1_e13 sel/dev(sel) p5;
    bind mf_b1_e14 sel/dev(sel) p6;
    bind mf_b1_e15 sel/dev(sel) p7;
    bind mf_b1_e16 sel/dev(sel) p8;
 """

drum_machine_paralel_mix = """
    bind mf_b1_e1 "DrumAut"/dev("Sends") p1;
    bind mf_b1_e5 "DrumAut"/dev("Sends") p5;
    bind mf_b1_e9 "DrumAut"/dev("Customs") p1;
    bind mf_b1_e13 "DrumAut"/dev("Customs") p5;
    bind mf_b1_e2 "DrumAut"/dev("Sends") p2;
    bind mf_b1_e6 "DrumAut"/dev("Sends") p6;
    bind mf_b1_e10 "DrumAut"/dev("Customs") p2;
    bind mf_b1_e14 "DrumAut"/dev("Customs") p6;
    bind mf_b1_e3 "DrumAut"/dev("Sends") p3;
    bind mf_b1_e7 "DrumAut"/dev("Sends") p7;
    bind mf_b1_e11 "DrumAut"/dev("Customs") p3;
    bind mf_b1_e15 "DrumAut"/dev("Customs") p7;
    bind mf_b1_e4 "DrumAut"/dev("Sends") p4;
    bind mf_b1_e8 "DrumAut"/dev("Sends") p8;
    bind mf_b1_e12 "DrumAut"/dev("Customs") p4;
    bind mf_b1_e16 "DrumAut"/dev("Customs") p8;
"""


mf_color_schemas = {
    "drum_machine_paralel_mix":[
        [1,10, 10, 20],
        [2,10, 10, 20],
        [3,10, 10, 20],
        [4,10, 10, 20],
        [5,24, 10, 20],
        [6,24, 10, 20],
        [7,24, 10, 20],
        [8,24, 10, 20],
        [9,87, 100, 100],
        [13,87, 100, 100],
        [10,29, 100, 100],
        [14,29, 100, 100],
        [11,63, 100, 100],
        [15,63, 100, 100],
        [12,110, 100, 100],
        [16,110, 100, 100]
    ],
    "default_binding":[
        [1,10, 100, 100],
        [2,24, 100, 100],
        [3,38, 100, 100],
        [4,52, 100, 100],
        [5,60, 100, 100],
        [6,60, 100, 100],
        [7,60, 100, 100],
        [8,60, 100, 100],
        [9,85, 100, 100],
        [10,86, 100, 100],
        [11,87, 100, 100],
        [12,88, 100, 100],
        [13,89, 100, 100],
        [14,90, 100, 100],
        [15,91, 100, 100],
        [16,92, 100, 100]
    ]
}

control_modes_defs = {
    "default_binding" :  {
        "binding": default_binding,
        "color_schema": mf_color_schemas["default_binding"]
    },
    "drum_machine_paralel_mix" : {
        "binding": drum_machine_paralel_mix,
        "color_schema": mf_color_schemas["drum_machine_paralel_mix"]
    }
}