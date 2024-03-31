import customtkinter
from playsound import playsound
import os
from audiocomputer import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

octave = 0
frequency = 220
name_increment = 0

root = customtkinter.CTk()
root.geometry("500x800")

audio_computer = AudioComputer

def create_sound():
    global name_increment
    audio_computer.create_wav_file(audio_computer, "sound" + str(name_increment))
    playsound("sound" + str(name_increment) + ".wav")
    if os.path.exists("sound" + str(name_increment - 2) + ".wav"):
        os.remove("sound" + str(name_increment - 2) + ".wav")
    name_increment += 1

def set_time_label(value):
    audio_computer.set_time(audio_computer, int(value))
    time_label.configure(text=int(value))

def set_volume(db):
    audio_computer.set_gain(audio_computer, int(db))
    volume_label_percent.configure(text=str(int((volume_slider.get() / 75) * 100) + 100) + "%")

def set_wave(choice):
    if choice == "Saw":
        audio_computer.set_waveform(audio_computer, "Saw")
    if choice == "Sin":
        audio_computer.set_waveform(audio_computer, "Sin")
    if choice == "Square":
        print("Needs Implementation")

def set_note(choice):
    global frequency
    temp_freq=0
    if choice == "A":
        temp_freq = 220.00
    if choice == "A#":
        temp_freq = 233.08
    if choice =="B":
        temp_freq = 246.94
    if choice == "C":
        temp_freq = 261.63
    if choice == "C#":
        temp_freq = 277.18
    if choice =="D":
        temp_freq = 293.66
    if choice == "D#":
        temp_freq = 311.13
    if choice == "E":
        temp_freq = 329.63
    if choice == "F":
        temp_freq = 349.23
    if choice == "F#":
        temp_freq = 369.99
    if choice == "G":
        temp_freq = 392.00
    if choice == "G#":
        temp_freq = 415.30
    frequency = temp_freq
    audio_computer.set_frequency(audio_computer, calculate_frequency())

def calculate_frequency():
    audio_computer.frequency = frequency * (2**octave)
    return frequency * (2**octave)

def increase_octave():
    global octave
    octave +=1
    octave_label.configure(text=octave)
    calculate_frequency()

def decrease_octave():
    global octave
    octave -=1
    octave_label.configure(text=octave)
    calculate_frequency()

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=80, padx=80, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Synthesizer", font=("Roboto", 36))
label.pack(pady=12, padx=10)

# Time
time_slider = customtkinter.CTkSlider(frame,
    from_=1,
    to=10,
    command=set_time_label,
    number_of_steps=9
    )
time_slider.pack(pady=10)
time_slider.set(1)

time_label = customtkinter.CTkLabel(frame, text=int(time_slider.get()), font=("Roboto",12))
time_label.pack(pady=10)

# Volume
volume_label = customtkinter.CTkLabel(frame, text="Volume", font=("Roboto", 12))
volume_label.pack(pady=0)

volume_slider = customtkinter.CTkSlider(frame,
    from_=-75,
    to=0,
    command=set_volume
    )
volume_slider.pack(pady=10)
volume_slider.set(0)

volume_label_percent = customtkinter.CTkLabel(frame,text=str(int((volume_slider.get() / 75) * 100) + 100) + "%")
volume_label_percent.pack(pady=5)

# Waves
waves = ["Saw", "Sin", "Square"]
wave_select = customtkinter.CTkComboBox(frame,
                                        values=waves,
                                        command=set_wave)
wave_select.pack(pady=20)

#Note
notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
note_select = customtkinter.CTkComboBox(frame,
                                        values=notes,
                                        command=set_note)
note_select.pack(pady=20)

octave_box = customtkinter.CTkFrame(master=frame)
octave_box.pack(padx=40,pady=10)

octave_increment =  customtkinter.CTkButton(octave_box, text="+",width=20,height=20, font=("Roboto",24), command=increase_octave)
octave_increment.pack(side='right',padx=20)

octave_label = customtkinter.CTkLabel(octave_box, text=0, font=("Roboto",24))
octave_label.pack(side='right',padx=10)


octave_decrement =  customtkinter.CTkButton(octave_box, text="-",width=20,height=20, font=("Roboto",24), command=decrease_octave)
octave_decrement.pack(side='left',padx=20)

button = customtkinter.CTkButton(master=frame, text="Play Sound", command=create_sound)
button.pack(pady=12, padx=10)

root.mainloop()