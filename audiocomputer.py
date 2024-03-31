import numpy as np
import scipy.io.wavfile as wav

class AudioComputer():
    sample_rate = 44100
    frequency = 220
    time = 1
    waveform = np.sin
    wavetable_length = 128
    gain = 0
    attack_length = 10000

    def interpolate_linearly(wave_table, index):
        truncated_index = int(np.floor(index))
        next_index = (truncated_index + 1) % wave_table.shape[0]

        next_index_weight = index - truncated_index
        truncated_index_weight = 1 - next_index_weight

        return truncated_index_weight * wave_table[truncated_index] + next_index_weight * wave_table[next_index]

    def attack(signal, attack_length = 10000):
        fade_in = (1 - np.cos(np.linspace(0, np.pi, attack_length))) * 0.5

        signal[:attack_length] = np.multiply(fade_in, signal[:attack_length])

        return signal

    def sawtooth(x):
        return (x + np.pi) / np.pi %2 - 1

    def set_sample_rate(self, val):
        self.sample_rate = val
        return

    def set_frequency(self, val):
        self.frequency = val

    def set_time(self, seconds):
        self.time = seconds
        return

    def set_waveform(self, wave):
        if wave == "Sin":
            self.waveform = np.sin
        if wave == "Saw":
            self.waveform = (np.pi) / np.pi %2 - 1
        return

    def set_wavetable_length(self, val):
        self.wavetable_length = val
        return

    def set_gain(self, val):
        self.gain = val
        return

    def set_attack_length(self, val):
        self.attack_length = val
        return

    def create_wav_file(self, name):
        wave_table = np.zeros((self.wavetable_length,))
        for n in range(self.wavetable_length):
            wave_table[n] = self.waveform(2 * np.pi * n / self.wavetable_length)

        output = np.zeros((self.time * self.sample_rate,))

        index = 0
        index_increment = self.frequency * self.wavetable_length / self.sample_rate

        for n in range(output.shape[0]):
            # output[n] = wave_table[int(np.floor(index))]\
            output[n] = self.interpolate_linearly(wave_table, index)
            index += index_increment
            index %= self.wavetable_length

        amplitude = 10 ** (self.gain / 20)
        output *= amplitude

        output = self.attack(output, self.attack_length)

        wav.write(name + '.wav', self.sample_rate, output.astype(np.float32))



def main():
    return

if __name__ == '__main__':
    main()