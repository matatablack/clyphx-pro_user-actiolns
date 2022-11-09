drum_machine_names_mapping_array = ["Kick", "Snare", "CHH", "Perc"]

column_controls_1 = ["SEND A", "SEND B", "DEV(2) P1", "DEV(2) P2"]

colors_by_name = {
    "Kick": {
        "default": 63,
        "active": 100,
    },
    "Minitaur": {
        "default": 1,
        "active": 100,
    },
    "Drums": {
        "default": 67,
        "active": 100,
    },
    "Omni 4": {
        "default": 6,
        "active": 100,
    },
    "Omni 1": {
        "default": 23,
        "active": 100,
    },
    "V. Bass": {
        "default": 115,
        "active": 100,
        "brightness": 10
    },
    "SH01A": {
        "default": 70,
        "active": 100,
    },
    "TB3": {
        "default": 7,
        "active": 100,
    },
    "Grandmother": {
        "default": 110,
        "active": 100,
    },
    "Deepmind": {
        "default": 2,
        "active": 100,
    },
    "Omni 2": {
        "default": 16,
        "active": 100,
    },
    "GTR VOX": {
        "default": 30,
        "active": 100,
    },
    "BASS COMP": {
        "default": 40,
        "active": 100,
    },
    "Yamaha": {
        "default": 77,
        "active": 100,
    },
    "Omni 3": {
        "default": 18,
        "active": 100,
    },
    "GTR Acus": {
        "default": 71,
        "active": 100,
    },
    "A-Send A": {
        "default": 32,
        "active": 100,
    },
    "B-Send B": {
        "default": 115,
        "active": 100,
    },
    "C-Send C": {
        "default": 75,
        "active": 100,
    },
    "Master": {
        "default": 90,
        "active": 100,
    }
}


instrument_control_0 = """ 
    tpl change_bank 1;
    bind mf_b1_e1 "Kick"/SEND A;
    bind mf_b1_e5 "Kick"/DEV(2) P1;
    bind mf_b1_e9 "Kick"/DEV(2) P2;
    bind mf_b1_e13 "Kick"/DEV(2) P3;
    bind mf_b1_e2 "Minitaur"/SEND A;
    bind mf_b1_e6 "Minitaur"/DEV(2) P1;
    bind mf_b1_e10 "Minitaur"/DEV(2) P2;
    bind mf_b1_e14 "Minitaur"/DEV(2) P3;
    bind mf_b1_e3 "Drums"/SEND A;
    bind mf_b1_e7 "Drums"/DEV(2) P1;
    bind mf_b1_e11 "Drums"/DEV(2) P2;
    bind mf_b1_e15 "Drums"/DEV(2) P3;
    bind mf_b1_e4 "Omni 4"/SEND A;
    bind mf_b1_e8 "Omni 4"/DEV(2) P1;
    bind mf_b1_e12 "Omni 4"/DEV(2) P2;
    bind mf_b1_e16 "Omni 4"/DEV(2) P3;
 """

instrument_control_0_bank2 = """ 

    tpl change_bank 2;

    bind mf_b2_s5 "Kick"/SOLO;
    bind mf_b2_s9 "Kick"/MUTE;
    bind mf_b2_s13 "Kick"/ARM;

    bind mf_b2_s6 "Minitaur"/SOLO;
    bind mf_b2_s10 "Minitaur"/MUTE;
    bind mf_b2_s14 "Minitaur"/ARM;

    bind mf_b2_s7 "Drums"/SOLO;
    bind mf_b2_s11 "Drums"/MUTE;
    bind mf_b2_s15 "Drums"/ARM;

    bind mf_b2_s8 "Omni 4"/SOLO;
    bind mf_b2_s12 "Omni 4"/MUTE;
    bind mf_b2_s16 "Omni 4"/ARM;

    bind mf_b2_e1 "Kick"/VOL;
    bind mf_b2_e5 "Kick"/PAN;
    bind mf_b2_e9 "Kick"/SEND C;
    bind mf_b2_e13 "Kick"/SEND B;

    bind mf_b2_e2 "Minitaur"/VOL;
    bind mf_b2_e6 "Minitaur"/PAN;
    bind mf_b2_e10 "Minitaur"/SEND C;
    bind mf_b2_e14 "Minitaur"/SEND B;

    bind mf_b2_e3 "Drums"/VOL;
    bind mf_b2_e7 "Drums"/PAN;
    bind mf_b2_e11 "Drums"/SEND C;
    bind mf_b2_e15 "Drums"/SEND B;

    bind mf_b2_e4 "Omni 4"/VOL;
    bind mf_b2_e8 "Omni 4"/PAN;
    bind mf_b2_e12 "Omni 4"/SEND C;
    bind mf_b2_e16 "Omni 4"/SEND B;
 """

instrument_control_1 = """ 
    tpl change_bank 1;

    bind mf_b1_e1 "Omni 1"/SEND A;
    bind mf_b1_e5 "Omni 1"/DEV(2) P1;
    bind mf_b1_e9 "Omni 1"/DEV(2) P2;
    bind mf_b1_e13 "Omni 1"/DEV(2) P3;
    bind mf_b1_e2 "V. Bass"/SEND A;
    bind mf_b1_e6 "V. Bass"/DEV(2) P1;
    bind mf_b1_e10 "V. Bass"/DEV(2) P2;
    bind mf_b1_e14 "V. Bass"/DEV(2) P3;
    bind mf_b1_e3 "SH01A"/SEND A;
    bind mf_b1_e7 "SH01A"/DEV(2) P1;
    bind mf_b1_e11 "SH01A"/DEV(2) P2;
    bind mf_b1_e15 "SH01A"/DEV(2) P3;
    bind mf_b1_e4 "TB3"/SEND A;
    bind mf_b1_e8 "TB3"/DEV(2) P1;
    bind mf_b1_e12 "TB3"/DEV(2) P2;
    bind mf_b1_e16 "TB3"/DEV(2) P3;
 """

instrument_control_1_bank2 = """ 
    tpl change_bank 2;

    bind mf_b2_s5 "Omni 1"/SOLO;
    bind mf_b2_s9 "Omni 1"/MUTE;
    bind mf_b2_s13 "Omni 1"/ARM;

    bind mf_b2_s6 "V. Bass"/SOLO;
    bind mf_b2_s10 "V. Bass"/MUTE;
    bind mf_b2_s14 "V. Bass"/ARM;

    bind mf_b2_s7 "SH01A"/SOLO;
    bind mf_b2_s11 "SH01A"/MUTE;
    bind mf_b2_s15 "SH01A"/ARM;

    bind mf_b2_s8 "TB3"/SOLO;
    bind mf_b2_s12 "TB3"/MUTE;
    bind mf_b2_s16 "TB3"/ARM;

    bind mf_b2_e1 "Omni 1"/VOL;
    bind mf_b2_e5 "Omni 1"/PAN;
    bind mf_b2_e9 "Omni 1"/SEND C;
    bind mf_b2_e13 "Omni 1"/SEND B;

    bind mf_b2_e2 "V. Bass"/VOL;
    bind mf_b2_e6 "V. Bass"/PAN;
    bind mf_b2_e10 "V. Bass"/SEND C;
    bind mf_b2_e14 "V. Bass"/SEND B;

    bind mf_b2_e3 "SH01A"/VOL;
    bind mf_b2_e7 "SH01A"/PAN;
    bind mf_b2_e11 "SH01A"/SEND C;
    bind mf_b2_e15 "SH01A"/SEND B;

    bind mf_b2_e4 "TB3"/VOL;
    bind mf_b2_e8 "TB3"/PAN;
    bind mf_b2_e12 "TB3"/SEND C;
    bind mf_b2_e16 "TB3"/SEND B;
 """

instrument_control_2 = """ 
    tpl change_bank 1

    bind mf_b1_e1 "Grandmother"/SEND A;
    bind mf_b1_e5 "Grandmother"/DEV(2) P1;
    bind mf_b1_e9 "Grandmother"/DEV(2) P2;
    bind mf_b1_e13 "Grandmother"/DEV(2) P3;
    bind mf_b1_e2 "Deepmind"/SEND A;
    bind mf_b1_e6 "Deepmind"/DEV(2) P1;
    bind mf_b1_e10 "Deepmind"/DEV(2) P2;
    bind mf_b1_e14 "Deepmind"/DEV(2) P3;
    bind mf_b1_e3 "Omni 2"/SEND A;
    bind mf_b1_e7 "Omni 2"/DEV(2) P1;
    bind mf_b1_e11 "Omni 2"/DEV(2) P2;
    bind mf_b1_e15 "Omni 2"/DEV(2) P3;
    bind mf_b1_e4 "GTR VOX"/SEND A;
    bind mf_b1_e8 "GTR VOX"/DEV(2) P1;
    bind mf_b1_e12 "GTR VOX"/DEV(2) P2;
    bind mf_b1_e16 "GTR VOX"/DEV(2) P3;
 """

instrument_control_2_bank2 = """ 
    tpl change_bank 2;
    
    bind mf_b2_s5 "Grandmother"/SOLO;
    bind mf_b2_s9 "Grandmother"/MUTE;
    bind mf_b2_s13 "Grandmother"/ARM;
    bind mf_b2_s6 "Deepmind"/SOLO;
    bind mf_b2_s10 "Deepmind"/MUTE;
    bind mf_b2_s14 "Deepmind"/ARM;
    bind mf_b2_s7 "Omni 2"/SOLO;
    bind mf_b2_s11 "Omni 2"/MUTE;
    bind mf_b2_s15 "Omni 2"/ARM;
    bind mf_b2_s8 "GTR VOX"/SOLO;
    bind mf_b2_s12 "GTR VOX"/MUTE;
    bind mf_b2_s16 "GTR VOX"/ARM;

    bind mf_b2_e1 "Grandmother"/VOL;
    bind mf_b2_e5 "Grandmother"/PAN;
    bind mf_b2_e9 "Grandmother"/SEND C;
    bind mf_b2_e13 "Grandmother"/SEND B;

    bind mf_b2_e2 "Deepmind"/VOL;
    bind mf_b2_e6 "Deepmind"/PAN;
    bind mf_b2_e10 "Deepmind"/SEND C;
    bind mf_b2_e14 "Deepmind"/SEND B;

    bind mf_b2_e3 "Omni 2"/VOL;
    bind mf_b2_e7 "Omni 2"/PAN;
    bind mf_b2_e11 "Omni 2"/SEND C;
    bind mf_b2_e15 "Omni 2"/SEND B;

    bind mf_b2_e4 "GTR VOX"/VOL;
    bind mf_b2_e8 "GTR VOX"/PAN;
    bind mf_b2_e12 "GTR VOX"/SEND C;
    bind mf_b2_e16 "GTR VOX"/SEND B;
 """

instrument_control_3 = """ 
    tpl change_bank 1;

    bind mf_b1_e1 "BASS COMP"/SEND A;
    bind mf_b1_e5 "BASS COMP"/DEV(2) P1;
    bind mf_b1_e9 "BASS COMP"/DEV(2) P2;
    bind mf_b1_e13 "BASS COMP"/DEV(2) P3;
    bind mf_b1_e2 "Yamaha"/SEND A;
    bind mf_b1_e6 "Yamaha"/DEV(2) P1;
    bind mf_b1_e10 "Yamaha"/DEV(2) P2;
    bind mf_b1_e14 "Yamaha"/DEV(2) P3;
    bind mf_b1_e3 "Omni 3"/SEND A;
    bind mf_b1_e7 "Omni 3"/DEV(2) P1;
    bind mf_b1_e11 "Omni 3"/DEV(2) P2;
    bind mf_b1_e15 "Omni 3"/DEV(2) P3;
    bind mf_b1_e4 "GTR Acus"/SEND A;
    bind mf_b1_e8 "GTR Acus"/DEV(2) P1;
    bind mf_b1_e12"GTR Acus"/DEV(2) P2;
    bind mf_b1_e16 "GTR Acus"/DEV(2) P2;
 """

instrument_control_3_bank2 = """ 
    tpl change_bank 2;
    
    bind mf_b2_s5 "BASS COMP"/SOLO;
    bind mf_b2_s9 "BASS COMP"/MUTE;
    bind mf_b2_s13 "BASS COMP"/ARM;
    bind mf_b2_s6 "Yamaha"/SOLO;
    bind mf_b2_s10 "Yamaha"/MUTE;
    bind mf_b2_s14 "Yamaha"/ARM;
    bind mf_b2_s7 "Omni 3"/SOLO;
    bind mf_b2_s11 "Omni 3"/MUTE;
    bind mf_b2_s15 "Omni 3"/ARM;
    bind mf_b2_s8 "GTR VOX"/SOLO;
    bind mf_b2_s12 "GTR VOX"/MUTE;
    bind mf_b2_s16 "GTR VOX"/ARM;

    bind mf_b2_e1 "BASS COMP"/VOL;
    bind mf_b2_e5 "BASS COMP"/PAN;
    bind mf_b2_e9 "BASS COMP"/SEND C;
    bind mf_b2_e13 "BASS COMP"/SEND B;

    bind mf_b2_e2 "Yamaha"/VOL;
    bind mf_b2_e6 "Yamaha"/PAN;
    bind mf_b2_e10 "Yamaha"/SEND C;
    bind mf_b2_e14 "Yamaha"/SEND B;

    bind mf_b2_e3 "Omni 3"/VOL;
    bind mf_b2_e7 "Omni 3"/PAN;
    bind mf_b2_e11 "Omni 3"/SEND C;
    bind mf_b2_e15 "Omni 3"/SEND B;

    bind mf_b2_e4 "GTR VOX"/VOL;
    bind mf_b2_e8 "GTR VOX"/PAN;
    bind mf_b2_e12 "GTR VOX"/SEND C;
    bind mf_b2_e16 "GTR VOX"/SEND B;
 """


master_fx_and_sends = """ 
    bind mf_b1_e1 "A-Send A"/DEV(1) P1;
    bind mf_b1_e2 "A-Send A"/DEV(1) P2;
    bind mf_b1_e5 "A-Send A"/DEV(1) P3;
    bind mf_b1_e6 "A-Send A"/DEV(1) P4;

    bind mf_b1_e3 "B-Send B"/DEV(1) P1;
    bind mf_b1_e4 "B-Send B"/DEV(1) P2;
    bind mf_b1_e7 "B-Send B"/DEV(1) P3;
    bind mf_b1_e8 "B-Send B"/DEV(1) P4;
    
    bind mf_b1_e9 "C-Send C"/DEV(1) P1;
    bind mf_b1_e10 "C-Send C"/DEV(1) P2;
    bind mf_b1_e11 "C-Send C"/DEV(1) P3;
    bind mf_b1_e12 "C-Send C"/DEV(1) P4;

    bind mf_b1_e13 "Master"/DEV("FX") P1;
    bind mf_b1_e14 "Master"/DEV("FX") P2;
    bind mf_b1_e15 "Master"/DEV("FX") P3;
    bind mf_b1_e16 "Master"/DEV("FX") P4;
 """

live_1 = """ 
    tpl change_bank 1;
    bind mf_b1_e1 "Drums"/SEND A;
    bind mf_b1_e5 "Drums"/DEV(2) P1;
    bind mf_b1_e9 "Drums"/DEV(2) P2;
    bind mf_b1_e13 "Drums"/DEV(2) P3;
    bind mf_b1_e2 "Yamaha"/SEND A;
    bind mf_b1_e6 "Yamaha"/DEV(2) P1;
    bind mf_b1_e10 "Yamaha"/DEV(2) P2;
    bind mf_b1_e14 "Yamaha"/DEV(2) P3;
    bind mf_b1_e3 "Omni 1"/SEND A;
    bind mf_b1_e7 "Omni 1"/DEV(2) P1;
    bind mf_b1_e11 "Omni 1"/DEV(2) P2;
    bind mf_b1_e15 "Omni 1"/DEV(2) P3;
    bind mf_b1_e4 "GTR VOX"/SEND A;
    bind mf_b1_e8 "GTR VOX"/DEV(2) P1;
    bind mf_b1_e12 "GTR VOX"/DEV(2) P2;
    bind mf_b1_e16 "GTR VOX"/DEV(2) P3;
 """

live_1_bank2 = """ 
    tpl change_bank 2;
    
    bind mf_b2_s5 "Drums"/SOLO;
    bind mf_b2_s9 "Drums"/MUTE;
    bind mf_b2_s13 "Drums"/ARM;
    bind mf_b2_s6 "Yamaha"/SOLO;
    bind mf_b2_s10 "Yamaha"/MUTE;
    bind mf_b2_s14 "Yamaha"/ARM;
    bind mf_b2_s7 "Omni 1"/SOLO;
    bind mf_b2_s11 "Omni 1"/MUTE;
    bind mf_b2_s15 "Omni 1"/ARM;
    bind mf_b2_s8 "GTR VOX"/SOLO;
    bind mf_b2_s12 "GTR VOX"/MUTE;
    bind mf_b2_s16 "GTR VOX"/ARM;

    bind mf_b2_e1 "Drums"/VOL;
    bind mf_b2_e5 "Drums"/PAN;
    bind mf_b2_e9 "Drums"/SEND C;
    bind mf_b2_e13 "Drums"/SEND B;

    bind mf_b2_e2 "Yamaha"/VOL;
    bind mf_b2_e6 "Yamaha"/PAN;
    bind mf_b2_e10 "Yamaha"/SEND C;
    bind mf_b2_e14 "Yamaha"/SEND B;

    bind mf_b2_e3 "Omni 1"/VOL;
    bind mf_b2_e7 "Omni 1"/PAN;
    bind mf_b2_e11 "Omni 1"/SEND C;
    bind mf_b2_e15 "Omni 1"/SEND B;

    bind mf_b2_e4 "GTR VOX"/VOL;
    bind mf_b2_e8 "GTR VOX"/PAN;
    bind mf_b2_e12 "GTR VOX"/SEND C;
    bind mf_b2_e16 "GTR VOX"/SEND B;
 """


mf_color_schemas = {
    "instrument_control_0": [
        [1, colors_by_name["Kick"]["default"], 100, 100],
        [5, colors_by_name["Kick"]["default"], 100, 100],
        [9, colors_by_name["Kick"]["default"], 100, 100],
        [13, colors_by_name["Kick"]["default"], 100, 100],

        [2, colors_by_name["Minitaur"]["default"], 100, 100],
        [6, colors_by_name["Minitaur"]["default"], 100, 100],
        [10, colors_by_name["Minitaur"]["default"], 100, 100],
        [14, colors_by_name["Minitaur"]["default"], 100, 100],

        [3,  colors_by_name["Drums"]["default"], 100, 100],
        [7,  colors_by_name["Drums"]["default"], 100, 100],
        [11, colors_by_name["Drums"]["default"] , 100, 100],
        [15,  colors_by_name["Drums"]["default"], 100, 100],

        [4, colors_by_name["Omni 4"]["default"], 100, 100],
        [8, colors_by_name["Omni 4"]["default"], 100, 100],
        [12, colors_by_name["Omni 4"]["default"], 100, 100],
        [16, colors_by_name["Omni 4"]["default"], 100, 100]
    ],

    "instrument_control_1": [
        [1, colors_by_name["Omni 1"]["default"], 100, 100],
        [5, colors_by_name["Omni 1"]["default"], 100, 100],
        [9, colors_by_name["Omni 1"]["default"], 100, 100],
        [13, colors_by_name["Omni 1"]["default"], 100, 100],

        [2, colors_by_name["V. Bass"]["default"], 100, 100],
        [6, colors_by_name["V. Bass"]["default"], 100, 100],
        [10, colors_by_name["V. Bass"]["default"], 100, 100],
        [14, colors_by_name["V. Bass"]["default"], 100, 100],

        [3, colors_by_name["SH01A"]["default"], 100, 100],
        [7, colors_by_name["SH01A"]["default"], 100, 100],
        [11, colors_by_name["SH01A"]["default"], 100, 100],
        [15, colors_by_name["SH01A"]["default"], 100, 100],

        [4, colors_by_name["TB3"]["default"], 100, 100],
        [8, colors_by_name["TB3"]["default"], 100, 100],
        [12, colors_by_name["TB3"]["default"], 100, 100],
        [16, colors_by_name["TB3"]["default"], 100, 100]
    ],
    "instrument_control_1_bank2": [
        [17, colors_by_name["Omni 1"]["default"], 100, 100],
        [21, colors_by_name["Omni 1"]["default"], 100, 100],
        [25, colors_by_name["Omni 1"]["default"], 100, 100],
        [29, colors_by_name["Omni 1"]["default"], 100, 100],

        [18, colors_by_name["V. Bass"]["default"], 100, 100],
        [22, colors_by_name["V. Bass"]["default"], 100, 100],
        [26, colors_by_name["V. Bass"]["default"], 100, 100],
        [30, colors_by_name["V. Bass"]["default"], 100, 100],

        [19, colors_by_name["SH01A"]["default"], 100, 100],
        [23, colors_by_name["SH01A"]["default"], 100, 100],
        [27, colors_by_name["SH01A"]["default"], 100, 100],
        [31, colors_by_name["SH01A"]["default"], 100, 100],

        [20, colors_by_name["TB3"]["default"], 100, 100],
        [24, colors_by_name["TB3"]["default"], 100, 100],
        [28, colors_by_name["TB3"]["default"], 100, 100],
        [32, colors_by_name["TB3"]["default"], 100, 100]
    ],
    "instrument_control_2": [
        [1, colors_by_name["Grandmother"]["default"], 100, 100],
        [5, colors_by_name["Grandmother"]["default"], 100, 100],
        [9, colors_by_name["Grandmother"]["default"], 100, 100],
        [13, colors_by_name["Grandmother"]["default"], 100, 100],

        [2, colors_by_name["Deepmind"]["default"], 100, 100],
        [6, colors_by_name["Deepmind"]["default"], 100, 100],
        [10, colors_by_name["Deepmind"]["default"], 100, 100],
        [14, colors_by_name["Deepmind"]["default"], 100, 100],

        [3, colors_by_name["Omni 2"]["default"], 100, 100],
        [7, colors_by_name["Omni 2"]["default"], 100, 100],
        [11, colors_by_name["Omni 2"]["default"], 100, 100],
        [15, colors_by_name["Omni 2"]["default"], 100, 100],

        [4, colors_by_name["GTR VOX"]["default"], 100, 100],
        [8, colors_by_name["GTR VOX"]["default"], 100, 100],
        [12, colors_by_name["GTR VOX"]["default"], 100, 100],
        [16, colors_by_name["GTR VOX"]["default"], 100, 100]
    ],
    "instrument_control_2_bank2": [
        [17, colors_by_name["Grandmother"]["default"], 100, 100],
        [21, colors_by_name["Grandmother"]["default"], 100, 100],
        [25, colors_by_name["Grandmother"]["default"], 100, 100],
        [29, colors_by_name["Grandmother"]["default"], 100, 100],

        [18, colors_by_name["Deepmind"]["default"], 100, 100],
        [22, colors_by_name["Deepmind"]["default"], 100, 100],
        [26, colors_by_name["Deepmind"]["default"], 100, 100],
        [30, colors_by_name["Deepmind"]["default"], 100, 100],

        [19, colors_by_name["Omni 2"]["default"], 100, 100],
        [23, colors_by_name["Omni 2"]["default"], 100, 100],
        [27, colors_by_name["Omni 2"]["default"], 100, 100],
        [31, colors_by_name["Omni 2"]["default"], 100, 100],

        [20, colors_by_name["GTR VOX"]["default"], 100, 100],
        [24, colors_by_name["GTR VOX"]["default"], 100, 100],
        [28, colors_by_name["GTR VOX"]["default"], 100, 100],
        [32, colors_by_name["GTR VOX"]["default"], 100, 100]
    ],
    "instrument_control_3": [
        [1, colors_by_name["BASS COMP"]["default"], 100, 100],
        [5, colors_by_name["BASS COMP"]["default"], 100, 100],
        [9, colors_by_name["BASS COMP"]["default"], 100, 100],
        [13, colors_by_name["BASS COMP"]["default"], 100, 100],

        [2, colors_by_name["Yamaha"]["default"], 100, 100],
        [6, colors_by_name["Yamaha"]["default"], 100, 100],
        [10, colors_by_name["Yamaha"]["default"], 100, 100],
        [14, colors_by_name["Yamaha"]["default"], 100, 100],

        [3, colors_by_name["Omni 3"]["default"], 100, 100],
        [7, colors_by_name["Omni 3"]["default"], 100, 100],
        [11, colors_by_name["Omni 3"]["default"], 100, 100],
        [15, colors_by_name["Omni 3"]["default"], 100, 100],

        [4, colors_by_name["GTR Acus"]["default"], 100, 100],
        [8, colors_by_name["GTR Acus"]["default"], 100, 100],
        [12, colors_by_name["GTR Acus"]["default"], 100, 100],
        [16, colors_by_name["GTR Acus"]["default"], 100, 100]
    ],
    "master_fx_and_sends": [
        [1, colors_by_name["A-Send A"]["default"], 100, 100],
        [2, colors_by_name["A-Send A"]["default"], 100, 100],
        [5, colors_by_name["A-Send A"]["default"], 100, 100],
        [6, colors_by_name["A-Send A"]["default"], 100, 100],

        [9, colors_by_name["C-Send C"]["default"], 100, 100],
        [10, colors_by_name["C-Send C"]["default"], 100, 100],
        [11, colors_by_name["C-Send C"]["default"], 100, 100],
        [12, colors_by_name["C-Send C"]["default"], 100, 100],

        [13, colors_by_name["Master"]["default"], 100, 100],
        [14, colors_by_name["Master"]["default"], 100, 100],
        [15, colors_by_name["Master"]["default"], 100, 100],
        [16, colors_by_name["Master"]["default"], 100, 100],

        [3, colors_by_name["B-Send B"]["default"], 100, 100],
        [4, colors_by_name["B-Send B"]["default"], 100, 100],
        [7, colors_by_name["B-Send B"]["default"], 100, 100],
        [8, colors_by_name["B-Send B"]["default"], 100, 100],
    ],
    "live_1": [
        [1, colors_by_name["Drums"]["default"], 100, 100],
        [5, colors_by_name["Drums"]["default"], 100, 100],
        [9, colors_by_name["Drums"]["default"], 100, 100],
        [13, colors_by_name["Drums"]["default"], 100, 100],

        [2, colors_by_name["BASS COMP"]["default"], 100, 100],
        [6, colors_by_name["BASS COMP"]["default"], 100, 100],
        [10, colors_by_name["BASS COMP"]["default"], 100, 100],
        [14, colors_by_name["BASS COMP"]["default"], 100, 100],

        [3, colors_by_name["GTR VOX"]["default"], 100, 100],
        [7, colors_by_name["GTR VOX"]["default"], 100, 100],
        [11, colors_by_name["GTR VOX"]["default"], 100, 100],
        [15, colors_by_name["GTR VOX"]["default"], 100, 100],

        [4, colors_by_name["Yamaha"]["default"], 100, 100],
        [8, colors_by_name["Yamaha"]["default"], 100, 100],
        [12, colors_by_name["Yamaha"]["default"], 100, 100],
        [16, colors_by_name["Yamaha"]["default"], 100, 100]
    ],
}

control_modes_defs = {
    "instrument_control_0": {
        "binding": instrument_control_0,
        "color_schema": mf_color_schemas["instrument_control_0"],
    },
    "instrument_control_1": {
        "binding": instrument_control_1,
        "color_schema": mf_color_schemas["instrument_control_1"],
    },
    "instrument_control_1_bank2": {
        "binding": instrument_control_1_bank2,
        "color_schema": mf_color_schemas["instrument_control_1_bank2"],
    },
    "instrument_control_2": {
        "binding": instrument_control_2,
        "color_schema": mf_color_schemas["instrument_control_2"],
    },
    "instrument_control_2_bank2": {
        "binding": instrument_control_2_bank2,
        "color_schema": mf_color_schemas["instrument_control_2_bank2"],
    },
    "instrument_control_1": {
        "binding": instrument_control_1,
        "color_schema": mf_color_schemas["instrument_control_1"],
    },
    "instrument_control_3": {
        "binding": instrument_control_3,
        "color_schema": mf_color_schemas["instrument_control_3"],
    },
    "master_fx_and_sends": {
        "binding": master_fx_and_sends,
        "color_schema": mf_color_schemas["master_fx_and_sends"],
    },
    "live_1": {
        "binding": live_1,
        "color_schema": mf_color_schemas["live_1"],
    }
}
