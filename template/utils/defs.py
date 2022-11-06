drum_machine_names_mapping_array = ["Kick", "Snare", "CHH", "Perc"]

column_controls_1 = ["SEND A", "SEND B", "DEV(2) P1", "DEV(2) P2"]

instrument_control_0 = """ 
    bind mf_b1_e1 "Kick"/SEND A;
    bind mf_b1_e5 "Kick"/SEND B;
    bind mf_b1_e9 "Kick"/DEV(2) P1;
    bind mf_b1_e13 "Kick"/DEV(2) P2;
    bind mf_b1_e2 "Minitaur"/SEND A;
    bind mf_b1_e6 "Minitaur"/SEND B;
    bind mf_b1_e10 "Minitaur"/DEV(2) P1;
    bind mf_b1_e14 "Minitaur"/DEV(2) P2;
    bind mf_b1_e3 "Drums"/SEND A;
    bind mf_b1_e7 "Drums"/SEND B;
    bind mf_b1_e11 "Drums"/DEV(2) P1;
    bind mf_b1_e15 "Drums"/DEV(2) P2;
    bind mf_b1_e4 "Omni 4"/SEND A;
    bind mf_b1_e8 "Omni 4"/SEND B;
    bind mf_b1_e12 "Omni 4"/DEV(2) P1;
    bind mf_b1_e16 "Omni 4"/DEV(2) P2;


 """

instrument_control_1 = """ 
    bind mf_b1_e1 "Omni 1"/SEND A;
    bind mf_b1_e5 "Omni 1"/SEND B;
    bind mf_b1_e9 "Omni 1"/DEV(2) P1;
    bind mf_b1_e13 "Omni 1"/DEV(2) P2;
    bind mf_b1_e2 "V. Bass"/SEND A;
    bind mf_b1_e6 "V. Bass"/SEND B;
    bind mf_b1_e10 "V. Bass"/DEV(2) P1;
    bind mf_b1_e14 "V. Bass"/DEV(2) P2;
    bind mf_b1_e3 "SH01A"/SEND A;
    bind mf_b1_e7 "SH01A"/SEND B;
    bind mf_b1_e11 "SH01A"/DEV(2) P1;
    bind mf_b1_e15 "SH01A"/DEV(2) P2;
    bind mf_b1_e4 "TB3"/SEND A;
    bind mf_b1_e8 "TB3"/SEND B;
    bind mf_b1_e12 "TB3"/DEV(2) P1;
    bind mf_b1_e16 "TB3"/DEV(2) P2;


 """

instrument_control_2 = """ 
    bind mf_b1_e1 "Grandmother"/SEND A;
    bind mf_b1_e5 "Grandmother"/SEND B;
    bind mf_b1_e9 "Grandmother"/DEV(2) P1;
    bind mf_b1_e13 "Grandmother"/DEV(2) P2;
    bind mf_b1_e2 "Deepmind"/SEND A;
    bind mf_b1_e6 "Deepmind"/SEND B;
    bind mf_b1_e10 "Deepmind"/DEV(2) P1;
    bind mf_b1_e14 "Deepmind"/DEV(2) P2;
    bind mf_b1_e3 "Omni 2"/SEND A;
    bind mf_b1_e7 "Omni 2"/SEND B;
    bind mf_b1_e11 "Omni 2"/DEV(2) P1;
    bind mf_b1_e15 "Omni 2"/DEV(2) P2;
    bind mf_b1_e4 "GTR VOX"/SEND A;
    bind mf_b1_e8 "GTR VOX"/SEND B;
    bind mf_b1_e12 "GTR VOX"/DEV(2) P1;
    bind mf_b1_e16 "GTR VOX"/DEV(2) P2;


 """

instrument_control_3 = """ 
    bind mf_b1_e1 "BASS COMP"/SEND A;
    bind mf_b1_e5 "BASS COMP"/SEND B;
    bind mf_b1_e9 "BASS COMP"/DEV(2) P1;
    bind mf_b1_e13 "BASS COMP"/DEV(2) P2;
    bind mf_b1_e2 "Yamaha"/SEND A;
    bind mf_b1_e6 "Yamaha"/SEND B;
    bind mf_b1_e10 "Yamaha"/DEV(2) P1;
    bind mf_b1_e14 "Yamaha"/DEV(2) P2;
    bind mf_b1_e3 "Omni 3"/SEND A;
    bind mf_b1_e7 "Omni 3"/SEND B;
    bind mf_b1_e11 "Omni 3"/DEV(2) P1;
    bind mf_b1_e15 "Omni 3"/DEV(2) P2;
    bind mf_b1_e4 "GTR Acus"/SEND A;
    bind mf_b1_e8 "GTR Acus"/SEND B;
    bind mf_b1_e12"GTR Acus"/DEV(2) P1;
    bind mf_b1_e16 "GTR Acus"/DEV(2) P2;


 """
 


master_fx_and_sends = """ 
    bind mf_b1_e1 "A-Send A"/DEV(1) P1;
    bind mf_b1_e5 "A-Send A"/DEV(1) P2;
    bind mf_b1_e9 "A-Send A"/DEV(1) P3;
    bind mf_b1_e13 "A-Send A"/DEV(1) P4;

    bind mf_b1_e2 "B-Send B"/DEV(1) P1;
    bind mf_b1_e6 "B-Send B"/DEV(1) P2;
    bind mf_b1_e10 "B-Send B"/DEV(1) P3;
    bind mf_b1_e14 "B-Send B"/DEV(1) P4;
    
    bind mf_b1_e3 "C-Send C"/DEV(1) P1;
    bind mf_b1_e7 "C-Send C"/DEV(1) P2;
    bind mf_b1_e11 "C-Send C"/DEV(1) P3;
    bind mf_b1_e15 "C-Send C"/DEV(1) P4;

    bind mf_b1_e4 "Master"/DEV("FX") P1;
    bind mf_b1_e8 "Master"/DEV("FX") P2;
    bind mf_b1_e12 "Master"/DEV("FX") P3;
    bind mf_b1_e16 "Master"/DEV("FX") P4;


 """

live_1 = """ 
    bind mf_b1_e1 "Drums"/DEV(1) P1;
    bind mf_b1_e5 "Drums"/DEV(1) P2;
    bind mf_b1_e9 "Drums"/DEV(1) P3;
    bind mf_b1_e13 "Drums"/DEV(1) P4;

    bind mf_b1_e2 "BASS COMP"/DEV(1); P1
    bind mf_b1_e6 "BASS COMP"/DEV(1) P2;
    bind mf_b1_e10 "BASS COMP"/DEV(1) P3;
    bind mf_b1_e14 "BASS COMP"/DEV(1) P4;
    
    bind mf_b1_e3 "Omni 1"/DEV(1) P1;
    bind mf_b1_e7 "Omni 1"/DEV(1) P2;
    bind mf_b1_e11 "Omni 1"/DEV(1) P3;
    bind mf_b1_e15 "Omni 1"/DEV(1) P4;

    bind mf_b1_e4 "GTR VOX"/DEV("FX") P1;
    bind mf_b1_e8 "GTR VOX"/DEV("FX") P2;
    bind mf_b1_e12 "GTR VOX"/DEV("FX") P3;
    bind mf_b1_e16 "GTR VOX"/DEV("FX") P4;


 """


mf_color_schemas = {
    "default_binding":[
        [1,10, 100, 100],
        [2,24, 100, 100],
        [3,38, 100, 100],
        [4,52, 100, 100],
        [5,60, 100, 100],
        [6,45, 100, 100],
        [7,75, 100, 100],
        [8,2, 100, 100],
        [9,126, 100, 100],
        [10,34, 100, 100],
        [11,87, 100, 100],
        [12,48, 100, 100],
        [13,89, 100, 100],
        [14,90, 100, 100],
        [15,91, 100, 100],
        [16,92, 100, 100]
    ],
    "instrument_control_2":[
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
    "instrument_control_3":[
        [1,10, 10, 20],
        [2,10, 10, 20],
        [3,30, 60, 30],
        [4,10, 40, 20],
        [5,24, 60, 20],
        [6,24, 10, 20],
        [7,24, 50, 20],
        [8,24, 20, 20],
        [9,87, 40, 100],
        [13,82, 30, 100],
        [10,29, 100, 100],
        [14,29, 100, 100],
        [11,61, 100, 100],
        [15,63, 100, 100],
        [12,13, 100, 100],
        [16,110, 100, 100]
    ],
}

control_modes_defs = {
    "instrument_control_0": {
        "binding": instrument_control_0,
        "color_schema": mf_color_schemas["default_binding"],
    },
    "instrument_control_1": {
        "binding": instrument_control_1,
        "color_schema": mf_color_schemas["default_binding"],
    },
    "instrument_control_2": {
        "binding": instrument_control_2,
        "color_schema": mf_color_schemas["instrument_control_2"],
    },
    "instrument_control_3": {
        "binding": instrument_control_3,
        "color_schema": mf_color_schemas["instrument_control_3"],
    },
    "master_fx_and_sends": {
        "binding": master_fx_and_sends,
        "color_schema": mf_color_schemas["instrument_control_3"],
    },
    "live_1": {
        "binding": live_1,
        "color_schema": mf_color_schemas["instrument_control_3"],
    }
}