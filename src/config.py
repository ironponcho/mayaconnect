maya_connection = dict(
    host='localhost',
    python_port=4442,
    mel_port=4443,
    buffer_length=65536,
    is_debug=False,  # commands will be transmitted individually and a debug report will be generated
    command_send_batch_size=320
    # 65536 Buffer + 320 batch size -> 8.11
    # 32768 Buffer + 160 batch size -> 11.39
    # default Buffer + 1 batch size -> 144.08

    # just used if is_debug is false, commands will be send to maya in batches to improve performance
)
input_file = dict(
    idle_time_export_file="resource/VTG_RE_April_May_Germany.xlsx",
    date_format='%d.%m.%Y %H:%M:%S',
    start_search_period='01.04.2022 00:00:00',
    end_search_period='31.05.2022 23:59:59',
    end_search_period_for_representation='15.05.2022 23:59:59',  # filters to the dates before this str
    search_for_n_most_relevant_locations=25,  # 0 to disable relevancy filtering
    search_locations=[],  # empty array to  disable specific location filtering
    use_real_gps_location=True
)
general_representation = dict(
    real_seconds_per_day=1.5,
)
visualization = dict(
    is_enabled=True,
    location_padding=7,  # just relevant if use_real_gps_location is false
    altitude_block_padding=0.15,
    frames_per_second=30,
    block_size=0.55,
    strech_map_factor=3.5,  # factor to create space between the different locations
    block_pop_out_in_percent=125,

    #gradient_start_color=(0, 0.5725, 0.6588),
    gradient_start_color=(0, 0, 1),

    #gradient_end_color=(0.8980, 0.1176, 0.2039),
    gradient_end_color=(1, 0, 0),
    gradient_fading_delay_in_seconds=1.5,  # how long should be waited before the fade starts
    gradient_fading_time_in_seconds=5  # how long should it take to fade between start and end color
)
audiolization = dict(
    is_enabled=False,
    disappearing_tracks_enabled=True,
    base_note=48,  # C4
    ticks_per_beat=480,
    bpm=120,
    # 1 Beat = 1 quarter note
    appearing_note_substain_in_quaters=0.064,  # 64th Note
    disappearing_note_substain_in_quaters=0.128,  # 32th Note
    scale="Major",
    midi_channel=10,
    note_velocity=100,
    appearing_midi_channel=0,
    disappearing_midi_channel=1
)
