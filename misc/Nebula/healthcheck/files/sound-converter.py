import argparse
import numpy as np
import scipy.io.wavfile as wav
import os
from pydub.utils import make_chunks
from pydub import AudioSegment


# Sampling frequency
sample_rate = 44100

# Note length in seconds
note_length = 0.1

# Pause length in seconds
pause_length = 0.1

# Frequencies and names of notes within one scale
notes = [
    {'name': 'C4', 'freq': 261.63},
    {'name': 'D4', 'freq': 293.66},
    {'name': 'E4', 'freq': 329.63},
    {'name': 'F4', 'freq': 349.23},
    {'name': 'G4', 'freq': 392.00},
    {'name': 'A4', 'freq': 440.00},
    {'name': 'B4', 'freq': 493.88},
    {'name': 'C5', 'freq': 523.25}
]


def encode(data):
    freqs = []
    for digit in data:
        
        #print(digit)
        
        if digit == " ":
            pause = np.zeros(int(sample_rate * pause_length))
            freqs.append(pause)
        else:
            try:
                value = int(digit, 8)
            except ValueError:
                print(f"Invalid digit {digit} in input data.")
                return
            if value >= len(notes):
                print(f"Digit {digit} out of range of available notes.")
                return
            freqs.append(notes[value]['freq'])

    # Generating sound signal
    signal = np.array([])
    for freq in freqs:
        
        print(freq)
        
        if isinstance(freq, np.ndarray):
            # Adding pause
            signal = np.concatenate((signal, freq))
        else:
            t = np.linspace(0, note_length, int(note_length * sample_rate), False)
            wave = np.sin(2 * np.pi * freq * t)
            if len(signal) > 0:
                pause = np.zeros(int(sample_rate * pause_length))
                signal = np.concatenate((signal, pause))
            signal = np.concatenate((signal, wave))

    # Normalizing signal and converting to 16-bit integer
    scaled = np.int16(signal / np.max(np.abs(signal)) * 32767)

    # Writing WAV file
    wav.write('melody.wav', sample_rate, scaled)


def decode(file_path):
    # Load the audio file and split it into chunks of the specified length
    sound = AudioSegment.from_file(file_path, format=file_path.split(".")[-1])
    chunks = make_chunks(sound, int(note_length * 1000))

    with open("output.txt", "w") as output_file:
        last_freq = None
        for i, chunk in enumerate(chunks):
            # Only process chunks of the specified length
            if len(chunk) == int(note_length * 1000):
                # Convert the chunk to a NumPy array and apply the FFT
                samples = np.array(chunk.get_array_of_samples())
                fft = np.fft.fft(samples)

                # Compute the corresponding frequencies for each FFT value
                freqs = np.fft.fftfreq(len(samples), 1 / sample_rate)

                # Find the indices of the FFT values closest to each frequency in the range 260-520 Hz
                freq_indices = [np.abs(freqs - freq).argmin() for freq in range(260, 521, 30)]

                # Check if there are FFT values that are significantly different from zero for each frequency in the range
                freqs_in_chunk = []
                for freq_index in freq_indices:
                    if np.abs(fft[freq_index]) > np.max(np.abs(fft)) * 0.1:
                        freqs_in_chunk.append(freqs[freq_index])

                # Choose the frequency closest to the previous one, or 290 Hz if it's the first one
                if len(freqs_in_chunk) > 0:
                    freqs_in_chunk = sorted(freqs_in_chunk, key=lambda x: np.abs(x - last_freq) if last_freq is not None else np.abs(x - 290))
                    max_freq = freqs_in_chunk[0]
                    last_freq = max_freq
                else:
                    max_freq = None
                    last_freq = None

                time = i * note_length

                # Write the result to the output file
                if max_freq is not None:
                    output_file.write("[{:02d}:{:02d}.{:03d}] - {:.0f} Hz\n".format(int(time//60), int(time%60), int((time%1)*1000), max_freq))
                else:
                    output_file.write("[{:02d}:{:02d}.{:03d}] - P\n".format(int(time//60), int(time%60), int((time%1)*1000)))
            

# Parsing arguments
parser = argparse.ArgumentParser(description='Convert octal data to WAV sound file and decode sound file back to octal data.')
parser.add_argument('file', metavar='FILE', type=str, help='input file to encode or decode')
args = parser.parse_args()

# Encoding or decoding data
if args.file.endswith('.txt'):
    with open(args.file, 'r') as f:
        data = f.read()
    encode(data)
elif args.file.endswith('.wav') or args.file.endswith('.mp3'):
    decode(args.file)
else:
    print(f"Unsupported file format: {os.path.splitext(args.file)[1]}")
