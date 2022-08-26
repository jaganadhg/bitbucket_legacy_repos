#!/usr/bin/env python

import wave

from numpy.oldnumeric.functions import fromstring
import pylab as plt

__author__ = "jaganadhg"
__date__ = "$Dec 23, 2009 4:48:39 PM$"
__license__ = "GPL"


class SpeechTools:
    """
    Python script for simple speech corpora processing such as visualizing
    the wave form and spectrogram.
    """

    def __init__(self):
        """
        Just initialization of the calss.
        """


    def show_wave_form(self, wavefile):
        """
        Function to plot wave form. Takes a .wav file as input.
        """
        wavfop = wavefile
        sinf, params = self.__get_info(wavfop)
        plt.plot(sinf)
        plt.show()
        

    def show_specgram(self, wav_file):
        """
        Function to plot spectrogram from a given .wav file.
        """
        wavf = wav_file
        sinf, params = self.__get_info(wavf)
        plt.specgram(sinf, Fs=params[2], scale_by_freq=True, \
        sides='default')
        plt.xlabel("Time(s)")
        plt.show()


    def show_wav_n_spec(self, wav_file):
        """
        Show wave form and spectrogrm from a given .wav file.
        """
        wavf = wav_file
        sinfo, params = self.__get_info(wavf)
        plt.subplot(211)
        plt.plot(sinfo)
        plt.title('Wave from and spectrogram of %s' % wavf)
        plt.xlabel("Time(s)")

        plt.subplot(212)
        plt.specgram(sinfo, Fs=params[2], scale_by_freq=True, \
        sides='default')
        plt.xlabel("Time(s)")
        plt.show()


    def timit_wav(self, timitdata, pltof='w'):
        """
        Function to plot the wave form from timit data in NLTK.
        Usage:
            >>> from speech import *
            >>> ob = SpeechTools()
            >>> from nltk.corpus import timit
            >>> adt = timit.audiodata('dr8-mbcg0/sa1')
            >>> ob.timit_wav(adt,pltof='b') # To plot wave and specgram
            >>> ob.timit_wav(adt,pltof='w') # To plot only wav
            >>> ob.timit_wav(adt,pltof='s') # to plot spec gram
            >>> ob.timit_wav(adt) # Default plot wave form only
        """
        adfplot = fromstring(timitdata, 'Int16')

        if pltof == 's':
            plt.specgram(adfplot, scale_by_freq=True, \
            sides='default')
            plt.xlabel("Time(s)")
            plt.show()
        elif pltof == 'b':
            plt.subplot(211)
            plt.plot(adfplot)
            plt.xlabel("Time(s)")

            plt.subplot(212)
            plt.specgram(adfplot, scale_by_freq=True, \
            sides='default')
            plt.xlabel("Time(s)")
            plt.show()
        else:
            plt.plot(adfplot)
            plt.xlabel("Time(s)")
            plt.show()


        

    def __get_info(self, wav_file):
        """
        Function to get required info for plotting the wav form.
        """
        wavf = wave.open(wav_file, 'r')
        sound_info = wavf.readframes(-1)
        sound_info_norm = fromstring(sound_info, 'Int16')
        wav_params = wavf.getparams()

        return sound_info_norm, wav_params



if __name__ == "__main__":
    ob = SpeechTools()
    wa = '/home/jaganadhg/Desktop/sa1/sa1.wav'
    ob.show_wav_n_spec(wa)