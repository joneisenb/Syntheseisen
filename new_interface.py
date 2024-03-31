import customtkinter as ctk
import tkinter as tk
from basicsynth import seqManySinWavs

window = ctk.CTk()
window.title("Syntheseisen")
window.geometry("800x600")
window._fg_color='#272725'
ctk.set_appearance_mode('dark')

FONT = ("Aharoni",16)
FONT_COLOR = 'black'
BOX_COLOR = 'white'

Major = [2,2,1,2,2,2,1]
Natural_Minor = [2,1,2,2,1,2,2]
Harmonic_Minor = [2,1,2,2,1,3,1]
Dorian_Mode = [2,1,2,2,2,1,2]
Mixolydian_Mode = [2,2,1,2,2,1,2]
Ahava_Raba_Mode = [1,3,1,2,1,2,2]
Minor_Pentatonic = [3,2,2,3,2,1]

tempo = 120 # Default
frequency = [] # A4
note_type = 'Whole' #
note_interval = 1
calculated_note_duration = 1 # 1 second
note_count = 1
dotted_modifier = 1 # 1.5 if dotted
semitone_shift = 1 # One step
chord_offset = [] # root note of chord
chord = []
seventh = False
scale_name = "Major"
scale = Major #
times_played = 1

attack = 0
decay = 0
sustain = .5
release = 0



app = ctk.CTkFrame(window,fg_color='#272725')
app.pack(expand=True,fill='both',padx=5,pady=5)

## LEFT BOX

left_box = ctk.CTkFrame(app, fg_color='#EEE7D5',width=260,corner_radius=5)
left_box.pack(padx=5,pady=5,side='left',fill='y')

label_box = ctk.CTkFrame(left_box, fg_color='transparent',width=80)
label_box.pack(fill='y',side='left',expand=True,padx=10)

middle_box = ctk.CTkFrame(left_box, fg_color='transparent',width=100)
middle_box.pack(fill='y',side='left',expand=True)

unit_box = ctk.CTkFrame(left_box, fg_color='transparent',width=40)
unit_box.pack(fill='y',side='right',expand=True,padx=10)

## FUNCTIONS

def create_sound():
    calculate_all_variables()
    seqManySinWavs(frequency,calculated_note_duration,note_count,chord,attack,decay,sustain,release,times_played)

def calculate_all_variables():
    tempo_function(int(tempo_entry.get()))
    chord_function(chord_entry.get())
    frequency_function(int(frequency_entry.get()))
    include_seventh_function(include_seventh_checkbox.get())
    construct_chord()
    calculate_note_length_seconds()
    note_count_function(int(note_count_entry.get()))
    times_played_function(int(times_played_entry.get()))

    print("Tempo \t\t", tempo)
    print("Note Type\t", note_type)
    print("Dot_mod\t\t", dotted_modifier)
    print("Note Dur\t", calculated_note_duration)
    print("Frequency\t", frequency)
    print("Scale\t\t", scale_name)
    print("Chord Intervals\t", chord)
    print("Chord offset\t", chord_offset)
    print("Note Count\t", note_count)
    print(" ")

def calculate_note_length_seconds():
    global calculated_note_duration
    global note_type
    global tempo
    global dotted_modifier
    global note_interval

    calculated_note_duration = round((60 * note_interval * dotted_modifier * 4) / tempo, 5)

def sum_steps_in_scale(start,end):
    global scale
    global chord
    step = 0
    for i in range(start,end):
        step+= scale[i % len(scale)]
    return step

def construct_chord():
    global scale
    global chord
    global seventh
    global frequency
    chord = []

    chord_length = 3
    next_note = chord_offset[0]
    if seventh:
        chord_length = 0
    for i in range(0, chord_length):
        chord.append(sum_steps_in_scale(next_note, next_note + 2))
        next_note += 2


def tempo_function(tempo_val):
    global tempo
    tempo = tempo_val

def frequency_function(freq_val):
    global frequency
    frequency = []
    for offset in range(0, len(chord_offset)):
        frequency.append(freq_val * 2**(sum_steps_in_scale(0, chord_offset[offset])/12))
    print("Updated Frequency", frequency)


def note_type_function(note_val):
    global note_interval
    global note_type
    if note_val == 'Whole':
        note_interval = 1
        note_type = 'Whole'
    if note_val == 'Half':
        note_interval = 1/2
        note_type = 'Half'
    if note_val == 'Quarter':
        note_interval = 1/4
        note_type = 'Quarter'
    if note_val == 'Eighth':
        note_interval = 1/8
        note_type = 'Eigth'
    if note_val == 'Sixteenth':
        note_interval = 1/16
        note_type = 'Sixteenth'

def dotted_function():
    global dotted_modifier
    dotted_modifier = note_length_checkbox.get()

def scale_function(value):
    global scale
    global scale_name
    if value == "Major":
        scale = Major
    if value == "Natural Minor":
        scale = Natural_Minor
    if value == "Harmonic Minor":
        scale = Harmonic_Minor
    if value == "Dorian Mode":
        scale = Dorian_Mode
    if value == "Mixolydian Mode":
        scale = Mixolydian_Mode
    if value == "Ahava Raba Mode":
        scale = Ahava_Raba_Mode
    if value == "Minor Pentatonic":
        scale = Minor_Pentatonic
    scale_name = value

def chord_function(chord_string):
    global chord_offset
    chord_offset = []
    for offset in range(0,len(chord_string)):
        chord_offset.append(int(chord_string[offset]) - 1)

def include_seventh_function(b):
    global seventh
    seventh = b

def note_count_function(note_count_string):
    global note_count
    note_count = note_count_string

def times_played_function(num):
    global times_played
    times_played = num


## UI

### TEMPO

tempo_label = ctk.CTkLabel(label_box,text="Tempo",text_color=FONT_COLOR,font=FONT)
bpm_label = ctk.CTkLabel(unit_box, text="BPM",text_color=FONT_COLOR,font=FONT)
tempo_entry = ctk.CTkEntry(
    middle_box,
    font=FONT,
    justify='center',
    corner_radius=0,
    height=5,
    placeholder_text="120",
    width=110,
    fg_color=BOX_COLOR,
    placeholder_text_color=FONT_COLOR,
    text_color=FONT_COLOR
    )
tempo_entry.insert(0,'120')

tempo_label.pack(expand=True)
bpm_label.pack(expand=True)
tempo_entry.pack(expand=True)

### FREQUENCY


frequency_label = ctk.CTkLabel(label_box,text="Frequency",text_color=FONT_COLOR,font=FONT)
hz_label = ctk.CTkLabel(unit_box, text="Hz",text_color=FONT_COLOR,font=FONT)
frequency_entry = ctk.CTkEntry(
    middle_box,
    font=FONT,
    justify='center',
    corner_radius=0,
    height=5,
    placeholder_text="220",
    width=110,
    fg_color=BOX_COLOR,
    placeholder_text_color=FONT_COLOR,
    text_color=FONT_COLOR,
    )
frequency_entry.insert(0,'220')

frequency_label.pack(expand=True)
hz_label.pack(expand=True)
frequency_entry.pack(expand=True)

### LENGTH OF NOTE

note_length_label = ctk.CTkLabel(label_box,text="Note Type",text_color=FONT_COLOR,font=FONT)
note_types = ["Whole","Half","Quarter","Eighth","Sixteenth"]
note_length_dropdown = ctk.CTkComboBox(
    middle_box,
    values=note_types,
    corner_radius=0,
    height=5,
    text_color=FONT_COLOR,
    bg_color=BOX_COLOR,
    state='normal',
    width=110,
    justify='center',
    fg_color='#F7F7F7',
    font=FONT,
    command=note_type_function
    )
note_length_dropdown.set("Whole")
note_length_checkbox = ctk.CTkCheckBox(
    unit_box,
    onvalue=1.5,
    offvalue=1,
    text='•',
    font=("CTkFont", 24),
    width=40,
    text_color=FONT_COLOR,
    command=dotted_function
    )

note_length_label.pack(expand=True)
note_length_dropdown.pack(expand=True)
note_length_checkbox.pack(expand=True,padx=10)

### SCALE

scale_values = ["Major", "Natural Minor", "Harmonic Minor", "Dorian Mode", "Mixolydian Mode", "Ahava Raba Mode", "Minor Pentatonic"]
scale_label = ctk.CTkLabel(label_box,font=FONT,text="Scale",text_color=FONT_COLOR)
scale_unit_label = ctk.CTkLabel(unit_box, text="",text_color=FONT_COLOR,font=FONT)
scale_dropdown = ctk.CTkComboBox(
    middle_box,
    values=scale_values,
    corner_radius=0,
    height=5,
    text_color=FONT_COLOR,
    bg_color=BOX_COLOR,
    state='normal',
    width=110,
    justify='center',
    fg_color='#F7F7F7',
    font=FONT,
    command=scale_function
    )
scale_dropdown.set('Major')


scale_label.pack(expand=True)
scale_unit_label.pack(expand=True)
scale_dropdown.pack(expand=True)

### CHORDS

chord_label = ctk.CTkLabel(label_box,text="Root Note(s)",text_color=FONT_COLOR,font=FONT)
chord_entry = ctk.CTkEntry(
    middle_box,
    font=FONT,
    justify='center',
    corner_radius=0,
    height=5,
    placeholder_text="1",
    width=110,
    fg_color=BOX_COLOR,
    placeholder_text_color=FONT_COLOR,
    text_color=FONT_COLOR
    )
chord_entry.insert(0,'1')

include_seventh_checkbox = ctk.CTkCheckBox(
    unit_box,
    onvalue=True,
    offvalue=False,
    text='7th',
    font=("CTkFont", 16),
    width=40,
    text_color=FONT_COLOR,
    command=include_seventh_function
    )

chord_label.pack(expand=True)
chord_entry.pack(expand=True)
include_seventh_checkbox.pack(expand=True,padx=10)

### NOTE REPEATING

note_count_label = ctk.CTkLabel(label_box,font=FONT,text="Note Count",text_color=FONT_COLOR)
note_unit_label = ctk.CTkLabel(unit_box, text="",text_color=FONT_COLOR,font=FONT)
note_count_entry = ctk.CTkEntry(
    middle_box,
    font=FONT,
    justify='center',
    corner_radius=0,
    height=5,
    placeholder_text="1",
    width=110,
    fg_color=BOX_COLOR,
    placeholder_text_color=FONT_COLOR,
    text_color=FONT_COLOR
    )
note_count_entry.insert(0,'1')


note_count_label.pack(expand=True)
note_unit_label.pack(expand=True)
note_count_entry.pack(expand=True)

### REPEAT BOX

times_played_label = ctk.CTkLabel(label_box,font=FONT,text="Times played",text_color=FONT_COLOR)
times_played_unit_label = ctk.CTkLabel(unit_box, text="",text_color=FONT_COLOR,font=FONT)
times_played_entry = ctk.CTkEntry(
    middle_box,
    font=FONT,
    justify='center',
    corner_radius=0,
    height=5,
    placeholder_text="1",
    width=110,
    fg_color=BOX_COLOR,
    placeholder_text_color=FONT_COLOR,
    text_color=FONT_COLOR
    )
times_played_entry.insert(0,'1')


times_played_label.pack(expand=True)
times_played_unit_label.pack(expand=True)
times_played_entry.pack(expand=True)

# BOTTOM BOX

## FUNCTIONS

def attack_function(slider_val):
    global attack
    attack = attack_slider.get()
    attack_value.configure(text=str(round(slider_val,3)) +"s")
    # update_graph()

def decay_function(slider_val):
    global decay
    decay = decay_slider.get()
    decay_value.configure(text=str(round(slider_val,3)) + "s")
    # update_graph()

def sustain_function(slider_val):
    global sustain
    sustain = sustain_slider.get()
    sustain_value.configure(text=str(round(slider_val * 100,1)) + "%")
    # update_graph()

def release_function(slider_val):
    global release
    release = release_slider.get()
    release_value.configure(text=str(round(slider_val,3)) + "s")
    # update_graph()

## UI

bottom_box = ctk.CTkFrame(app,fg_color='#272725',height=260,corner_radius=5)
bottom_box.pack(pady=5,padx=5,side='bottom')

bottom_left_box = ctk.CTkFrame(bottom_box,width=240,fg_color='#EEE7D5',corner_radius=5)
bottom_left_box.pack(fill='y',side='left',expand=True)

bottom_right_box = ctk.CTkFrame(bottom_box,width=120,corner_radius=5)
bottom_right_box.pack(fill='y',side='right',expand=True)

top_label_box = ctk.CTkFrame(bottom_left_box, fg_color='transparent',height=30,corner_radius=5)
top_label_box.pack(fill='x',side='top',expand=True,pady=10)

middle_slider_box = ctk.CTkFrame(bottom_left_box, fg_color='transparent',height=160,corner_radius=5)
middle_slider_box.pack(fill='x',side='top',expand=True)

bottom_value_box = ctk.CTkFrame(bottom_left_box, fg_color='transparent',height=30,corner_radius=5)
bottom_value_box.pack(fill='x',side='bottom',expand=True,pady=10)

### ADSR Labels

attack_label = ctk.CTkLabel(top_label_box,text="Attack",text_color=FONT_COLOR,font=FONT,width=50)
decay_label = ctk.CTkLabel(top_label_box,text="Decay",text_color=FONT_COLOR,font=FONT,width=50)
sustain_label = ctk.CTkLabel(top_label_box,text="Sustain",text_color=FONT_COLOR,font=FONT,width=50)
release_label = ctk.CTkLabel(top_label_box,text="Release",text_color=FONT_COLOR,font=FONT,width=50)

attack_label.pack(padx=10,side='left',expand=True)
decay_label.pack(padx=10,side='left',expand=True)
sustain_label.pack(padx=10,side='left',expand=True)
release_label.pack(padx=10,side='left',expand=True)

### ADSR Sliders

attack_slider = ctk.CTkSlider(middle_slider_box,
    from_=0,
    to=1.5,
    command=attack_function,
    orientation='vertical',
    height=140
    )
attack_slider.set(0)
decay_slider = ctk.CTkSlider(middle_slider_box,
    from_=0,
    to=1.5,
    command=decay_function,
    orientation='vertical',
    height=140
    )
decay_slider.set(0)
sustain_slider = ctk.CTkSlider(middle_slider_box,
    from_=0,
    to=1,
    command=sustain_function,
    orientation='vertical',
    height=140
    )
sustain_slider.set(0.5)
release_slider = ctk.CTkSlider(middle_slider_box,
    from_=0,
    to=1.5,
    command=release_function,
    orientation='vertical',
    height=140
    )
release_slider.set(0)

attack_slider.pack(padx=10,side='left',expand=True)
decay_slider.pack(padx=10,side='left',expand=True)
sustain_slider.pack(padx=10,side='left',expand=True)
release_slider.pack(padx=10,side='left',expand=True)

### ADSR VALUES

attack_value = ctk.CTkLabel(bottom_value_box,text="0s",text_color=FONT_COLOR,font=FONT,width=80)
decay_value = ctk.CTkLabel(bottom_value_box,text="0s",text_color=FONT_COLOR,font=FONT,width=80)
sustain_value = ctk.CTkLabel(bottom_value_box,text="50%",text_color=FONT_COLOR,font=FONT,width=80)
release_value = ctk.CTkLabel(bottom_value_box,text="0s",text_color=FONT_COLOR,font=FONT,width=80)

attack_value.pack(padx=10,side='left',expand=True)
decay_value.pack(padx=10,side='left',expand=True)
sustain_value.pack(padx=10,side='left',expand=True)
release_value.pack(padx=10,side='left',expand=True)

### CREATE SOUND BUTTON

create_button = ctk.CTkButton(bottom_right_box, font=FONT, text_color=FONT_COLOR,fg_color='#007074',text="✓",command=create_sound)
create_button.pack(fill='both',expand=True)

# MIDDLE BOX

middle_box = ctk.CTkFrame(app, fg_color='#E1926A',corner_radius=5)
middle_box.pack(padx=5,pady=5,fill='both',expand=True)

window.mainloop()