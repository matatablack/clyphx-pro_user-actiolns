drum_machine_names_mapping_array = ["Kick", "Snare", "CHH", "Perc"]

instrument_control_1 = """ 
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

instrument_control_2 = """ 
    bind mf_b1_e1 "GTR Acus"/SEND A;
    bind mf_b1_e5 "GTR Acus"/SEND B;
    bind mf_b1_e9 "GTR Acus"/DEV(2) P1;
    bind mf_b1_e13 "GTR Acus"/DEV(2) P2;
    bind mf_b1_e2 "BASS COMP"/SEND A;
    bind mf_b1_e6 "BASS COMP"/SEND B;
    bind mf_b1_e10 "BASS COMP"/DEV(2) P1;
    bind mf_b1_e14 "BASS COMP"/DEV(2) P2;
    bind mf_b1_e3 "Yamaha"/SEND A;
    bind mf_b1_e7 "Yamaha"/SEND B;
    bind mf_b1_e11 "Yamaha"/DEV(2) P1;
    bind mf_b1_e15 "Yamaha"/DEV(2) P2;
    bind mf_b1_e4 "Omni 3"/SEND A;
    bind mf_b1_e8 "Omni 3"/SEND B;
    bind mf_b1_e12 "Omni 3"/DEV(2) P1;
    bind mf_b1_e16 "Omni 3"/DEV(2) P2;
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
}

control_modes_defs = {
    "instrument_control_1": {
        "binding": instrument_control_1,
        "color_schema": mf_color_schemas["default_binding"]
    },
    "instrument_control_2": {
        "binding": instrument_control_2,
        "color_schema": mf_color_schemas["instrument_control_2"]
    }
}