#!/usr/bin/env python

import numpy as np
import re
import json
from scipy.io import wavfile
from matplotlib import pyplot as plt

from functools import lru_cache
import soundfile as sf

FS = 120000
F32 = np.float32    # useful alias

class SoundWave:

    s_r = 44100
    frequency = 110
    time = 1
    wavetable_length = 128
    gain = 0
    attack_length = 10000

    def set_sample_rate(self, val):
        self.s_r = val
        return

    def set_frequency(self, val):
        self.frequency = val

    def set_time(self, seconds):
        self.time = seconds
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


def iround(x):
    return int(round(x))

def t2s(t):
    return iround(FS * t)


@lru_cache(maxsize=None)
def getSinWav(freq, nsamp, amp=0.2):
    tx    = np.arange(nsamp)
    wav   = np.sin(2 * np.pi * freq / FS * tx) * amp
    return F32(wav)


def justSinWav():
    'just a simple sin wav (pure tone)'
    freq  = 800     # hz
    dur   = 1       # s
    nsamp = iround(FS * dur)
    wav   = getSinWav(freq, nsamp)
    wavfile.write('output.wav', FS, wav)


def seqManySinWavs(freq, dur, num_notes,scale,attack,decay,sustain,release,times_played):
    'multiple sin wavs of different freqs arranged sequentially'
    nsamp = iround(dur * FS * 4)

    sil   = np.zeros(FS//10, dtype=F32)
    wavs  = [ sil ]

    a, d, s, r =  (iround(attack * nsamp), iround(decay * nsamp),
                       iround(sustain * nsamp),    iround(release * nsamp))
    env = basicRampUpDownEnvelope(a, r)

    # plt.plot(env)
    # plt.show()
    for f in range(0, len(freq)):
        for repeat in range(times_played):
            frequency = freq[f]
            for wid in range(num_notes):
                ratio = 2**(scale[wid%(len(scale)-1)]/12)
                wav = getSinWav(frequency, len(env))
                wav *= env
                wavs.append(wav)
                # wavs.append(sil)
                frequency *= ratio
    wav = np.hstack(wavs)
    wavfile.write('output.wav', FS, wav)




def basicRampUpDownEnvelope(attack, release):
    env1 = np.linspace(0, 1, attack )  # up
    env2 = np.linspace(1, 0, release)  # down
    env  = np.hstack((env1, env2))
    return F32(env)


def adsrEnvelope(attack, decay, sustain, release, dur, sustainAmp=0.8):
    'ADSR env'
    env = [
        np.linspace(0, dur, attack),
        np.linspace(dur, sustainAmp, decay)
    ]
    env = np.hstack(env)
    return env


def adsrFadeEnvelope(attack, decay, sustain, release, sustainAmp=0.4, fade=4):
    '''
    similar to adsr, but with slow exponential decay during sustain.
    this captures behavior of a plucked string
    '''
    env = [
        np.linspace(0, 1, attack),
        np.linspace(1, sustainAmp, decay),
        np.exp(-np.linspace(0, fade, sustain)) * sustainAmp,
        np.linspace(np.exp(-fade) * sustainAmp, 0, release)
    ]
    env = np.hstack(env)
    return F32(env)


def seqManySinWavsWithEnv():
    'multiple sin wavs of different freqs arranged in seq (with env)'
    freq  = 400
    ratio = 6/5
    sil   = np.zeros(FS//10, dtype=F32)
    wavs  = [ sil ]
    envType = 3
    if envType == 1:        # 1 basic ramp env
        dur     = 1
        nsamp   = iround(dur * FS)
        attack  = iround(0.01 * FS)
        release = nsamp - attack
        env   = basicRampUpDownEnvelope(attack, release)
    elif envType == 2:      # 2 adsr env
        a, d, s, r =  (iround(0.01 * FS), iround(0.15 * FS),
                       iround(1 * FS),    iround(0.03 * FS))
        env = adsrEnvelope(a, d, s, r)
    elif envType == 3:      # 3 edsr env with fade during sustain
        a, d, s, r =  (iround(0.01 * FS), iround(0.15 * FS),
                       iround(1 * FS),    iround(0.03 * FS))
        env = adsrFadeEnvelope(a, d, s, r, sustainAmp=0.4, fade=4)
    plt.plot(env)
    plt.show()
    for wid in range(5):
        wav = getSinWav(freq, len(env))
        wav *= env
        wavs.append(wav)
        wavs.append(sil)
        freq *= ratio
    wav = np.hstack(wavs)
    wavfile.write('output.wav', FS, wav)


def additiveSynth(freq, dur, vol):
    '''
    returns a synthesized sound by adding several partials
    freq : frequency of fundamental (in Hz)
    dur  : duration in seconds (only controls sustain)
    vol  : volume (linear)
    '''
    harlim   = 40
    harjump  = 5

    attack   = iround(0.003 * FS)
    decay    = iround(0.03  * FS)
    sustain  = iround(dur   * FS)
    release  = iround(0.02  * FS)

    combined   = 0
    for har in range(1, harlim, harjump):
        fhar = freq * har         # frequency for the partial
        if fhar > FS * 0.4:      # respect nyquist
            break
        fade = 2.5 + 0.4 * har      # fade depends on the partial har
        amp  = (har+2) ** -2.5    # amplitude depends on partial har
        env  = adsrFadeEnvelope(attack, decay, sustain, release,
                                sustainAmp=0.8, fade=fade)
        partial = getSinWav(fhar, len(env), amp=amp) * env
        combined = combined + partial
    correction = (110 / freq) ** 0.4
    ret = combined / abs(combined).max() * 0.5 * vol * correction
    return ret


def seqManyMuliHarmonicWav():
    'multiple additiveSynth output'
    freq  = 220
    ratio = 6/5
    sil   = np.zeros(FS//10, dtype=F32)
    wavs  = [ sil ]
    for wid in range(10):
        #wav = additiveSynth(freq, 2, 1)
        wav = fmSynth(freq, 2, 1)
        wavs.append(wav)
        wavs.append(sil)
        freq *= ratio
    wav = np.hstack(wavs)
    wavfile.write('output.wav', FS, wav)


def keymapEqTemp():
    '''
    Returns a dict that maps (octave, keyname) to its freq in Hz
    (Tuning scheme: equal temperament)
    '''
    f0   = 55 # 55 is the usual default
    # keys = 'a a# b c c# d d# e f f# g g#'.split()
    # NOTE: we are starting with C now on
    keys = 'c c# d d# e f f# g g# a a# b'.split()
    fvec = []
    keymap = {}
    for oc in range(0, 8):
        for idx, key in enumerate(keys):
            # f[k] = α f[k-1] ; α = 2 ** (1/12)
            fkey = f0 * 2 ** (oc + idx/12)
            fvec.append(fkey)
            keymap[(oc, key)] = fkey
            #print(f'{oc:}\t{key:4}\t{fkey:.2f}')
    return keymap


def keyPatten():
    'returns regex to match <oc><key>[<dur>][+/-<vol>]'
    octave = '([0-5])'
    key    = '(a|a#|b|c|c#|d|d#|e|f|f#|g|g#)'
    dur    = '([1-9]+)?' #optional
    vol    = '([+-][0-9]+)?' #optional
    patt   = f'^{octave}{key}{dur}{vol}$'
    return re.compile(patt)


_keymap  = keymapEqTemp()
_keypatt = keyPatten()


def parseKey(key):
    '''
    parse a key of the form 3c#4+2
    return a 4-tuple of octave, key, duration, volume
    '''
    mt  = _keypatt.match(key.strip())
    oc  = int(mt.group(1))
    key = mt.group(2)
    dur = mt.group(3)
    dur = 1 if dur is None else int(dur)
    vol = mt.group(4)
    vol = 0 if vol is None else int(vol)
    return oc, key, dur, vol


def kt4fdv(kt4):
    '4tuple key params to freq, dur, vol'
    f = _keymap[(kt4[0], kt4[1])]
    d = kt4[2]
    v = 10 ** (kt4[3]/10)    # similar to dB
    return f, d, v


def getSampleEnv(dur):
    att  = int(0.0005 * FS)
    dur  = int(dur * FS)
    fall = int(0.2 * FS)
    env = np.hstack([ np.linspace(0, 1, att), np.ones(dur), np.linspace(1, 0, fall) ])
    return env


def applyEnv(audio, dur, vol):
    vol1 = 10 ** (vol / 10)
    audio = audio / abs(audio).max() * 0.5 * vol1
    env   = getSampleEnv(dur)
    if len(audio) < len(env):
        diff  = len(env) - len(audio)
        audio = np.hstack((audio, np.zeros(diff, dtype=np.float32)))
    if len(audio) > len(env):
        audio = audio[:len(env)]
    audio *= env
    audio = audio / abs(audio).max() * vol1
    #- plt.plot(audio); plt.show()
    return F32(audio)


# with open('piano-harmonics.json') as fi:
#     __pianohar = json.load(fi)


# def pianoAdditiveSynth(octave, key, dur, vol):
#     '''
#     returns a synthesized sound by adding several partials
#     freq : frequency of fundamental (in Hz)
#     dur  : duration in seconds (only controls sustain)
#     vol  : volume (linear)
#     '''

#     freq, dur, vol = kt4fdv((octave, key, dur, vol))

#     freq = freq / 4

#     attack   = iround(0.001 * FS)
#     decay    = iround(0.001 * FS)
#     sustain  = iround(dur   * FS)
#     release  = iround(0.2   * FS)

#     combined   = 0
#     for idx, har in enumerate(__pianohar['peaks']):
#         fhar = freq * har       # frequency for the partial
#         if fhar > FS * 0.3:    # respect nyquist
#             break
#         fade = 1.0 + (freq/220) ** 0.5
#         amp  = np.exp(__pianohar['vals'][idx])
#         env  = adsrFadeEnvelope(attack, decay, sustain, release,
#                                 sustainAmp=0.7, fade=fade)
#         partial = getSinWav(fhar, len(env), amp=amp) * env
#         combined = combined + partial
#     correction = (110 / freq) ** 0.2
#     ret = combined / abs(combined).max() * 0.5 * vol * correction
#     return F32(ret)


# def pianoSample(octave, key, dur, vol):
#     if pianoSample.type == 1:
#         return pianoAdditiveSynth(octave, key, dur, vol)
#     elif pianoSample.type == 2:
#         return fmSynth(octave, key, dur, vol)
#     key = key.upper()
#     fname = f'samples/piano/{octave}{key}.ogg'
#     audio, rate = sf.read(fname)
#     assert rate == FS
#     audio = applyEnv(audio, dur, vol)
#     return audio


# pianoSample.type = 0


# __dmap = { 'H' : 'samples/home/',
#            'K' : 'samples/drumkit/' }


# def loadByWavlist(key, dur, vol):
#     srcdir = __dmap[key[0]]
#     idx = int(key[1:]) # this is the line number
#     with open(f'{srcdir}/wavlist.txt') as fi:
#         lines = [ line.strip() for line in fi ]
#     fname = lines[idx-1]
#     audio, rate = sf.read(f'{srcdir}/{fname}')
#     assert rate == FS
#     dur   = 4
#     audio = applyEnv(audio, dur, vol)
#     return F32(audio)


# @lru_cache(maxsize=None)
# def sampleSynth(octave, key, dur, vol):
#     if key[0] == 'P':
#         ret = pianoSample(octave, key[1:], dur, vol)
#     elif key[0] in __dmap:
#         ret = loadByWavlist(key, dur, vol)
#     else:
#         ret = pianoSample(octave, key, dur, vol)
#     return ret


# def signAbsPow(sig, p=1):
#     sign = np.sign(sig)
#     return sign * abs(sig) ** p


# def fmodulate(fmods, amps, freq, dur):
#     attack  = t2s(0.1)
#     decay   = t2s(0.05)
#     release = t2s(0.3)
#     sustain = t2s(dur)
#     adsr2   = adsrFadeEnvelope(attack, decay, sustain, release, 0.9, 1)
#     adsr    = adsrFadeEnvelope(attack, decay, sustain, release, 0.9, 0.1)
#     ns      = len(adsr)
#     gain = 5
#     tx   = (2.0 * np.pi / FS) * np.arange(ns)
#     combined = 0
#     for idx, fm in enumerate(fmods):
#         comp = np.sin(fm * freq * tx)
#         comp = signAbsPow(comp, 0.8)
#         #comp = np.sign(comp)
#         combined += comp * amps[idx]
#     modsig  = 1 + gain * combined * adsr2
#     phase   = 2.0 * np.pi * freq * modsig / FS
#     phase   = phase.cumsum()
#     sig     = np.sin(phase)
#     sig     = signAbsPow(sig, 0.7)
#     sig     = sig * adsr
#     return np.float32(sig)


# def fmSynth(octave, key, dur, vol):

#     freq, dur, vol = kt4fdv((octave, key, dur, vol))

#     freq = freq / 8

#     AR    = np.array

#     fmods = AR([ 2, 5, 11 ])
#     amps  = AR([ 1, 1, 2 ])
#     amps  = amps / amps.sum()

#     ret = fmodulate(fmods, amps, freq, dur)

#     correction = (110 / freq) ** 0.1
#     ret = ret/ abs(ret).max() * vol * correction

#     return ret


# def testSampleSynth():
#     #data = sampleSynth(6, 'a', 2, 0)
#     #data = sampleSynth(6, 'H4', 2, 0)
#     data = fmSynth(220, 1, 1)
#     plt.plot(data); plt.show()
#     #print(rate, data.shape, data.dtype)


    #justSinWav()
    #seqManySinWavs()
    #seqManySinWavsWithEnv()
    #seqManyMuliHarmonicWav()
    #testSampleSynth()




# DISCLAIMER:
# -> Only very basic ideas are explored here
# -> I am not presenting anything new or original
# -> Consider this as a fairly good starting point
#    (rather than a `gold standard`)



