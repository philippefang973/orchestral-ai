import random
import os
import io
import sys
import subprocess as proc 
import time
import random

import soundfile as sf
from pydub import AudioSegment
from pysndfx import AudioEffectsChain

def convert(filestorage,user,logger) :
	b = io.BytesIO(filestorage.read())
	audio, sr = sf.read(b)
	audio = audio[:30*sr]
	fn= filestorage.filename.split(".")[0]
	proc.run(f"mkdir converter/input/{user}".split(" "))
	proc.run(f"mkdir converter/output/{user}".split(" "))
	sf.write(f"converter/input/{user}/{fn}.wav",audio,sr)

	now = time.time()
	proc.run(f"mkdir converter/output/{user}/stems".split(" "))
	proc.run(f"mkdir converter/output/{user}/midis".split(" "))
	proc.run(f"mkdir converter/output/{user}/synths".split(" "))

	now_spleeter = time.time()
	audio = f"converter/input/{user}/{fn}.wav"
	logger(audio)
	cmd = f"spleeter separate -p spleeter:4stems -o converter/output/{user}/stems "+audio
	proc.run(cmd.split(" "))
	logger(f"stems extracted")
	now_spleeter = time.time()-now_spleeter

	now_basicp = time.time()
	stems_dir = f"converter/output/{user}/stems/"+audio.split("/")[-1].split(".")[0]
	stems = [os.path.join(stems_dir,f) for f in os.listdir(stems_dir)]
	cmd = f"basic-pitch converter/output/{user}/midis "+" ".join(stems)
	proc.run(cmd.split(" "))

	logger("midis generation done")
	now_basicp = time.time() - now_basicp

	now_synth = time.time()
	soundfont_path = "converter/kaggle/sonanita-sf2"
	soundfont_files = os.listdir(soundfont_path)

	vocal_sf = [sf2 for sf2 in soundfont_files if "Violins Staccato" in sf2]
	bass_sf = [sf2 for sf2 in soundfont_files if "Brass" in sf2 or "Basses" in sf2]
	other_sf = [sf2 for sf2 in soundfont_files if "Concert Harp" in sf2]
	drums_sf = [sf2 for sf2 in soundfont_files if "Keys" in sf2]

	midi_files = [f for f in os.listdir(f"converter/output/{user}/midis")]

	synth_dir = f"converter/output/{user}/synths"
	for midi in midi_files :
		sfz = ""
		if "vocals" in midi : sfz = os.path.join(soundfont_path,random.choice(vocal_sf))
		if "drums" in midi : sfz = os.path.join(soundfont_path,random.choice(bass_sf))
		if "bass" in midi : sfz = os.path.join(soundfont_path,random.choice(other_sf))
		if "other" in midi : sfz = os.path.join(soundfont_path,random.choice(drums_sf))
		logger(sfz)
		midi_path = os.path.join(f"converter/output/{user}/midis",midi)
		synth_path = os.path.join(synth_dir,midi.split("_")[0]+"_synths.wav")
		proc.run(["midi2audio","-s",sfz,midi_path,synth_path])
	logger("synths generated")
	now_synth = time.time()-now_synth

	now_overlay = time.time()
	synth_files = [f for f in os.listdir(synth_dir)]
	overlay = None
	for s in synth_files :
		audio_segment = AudioSegment.from_file(os.path.join(synth_dir,s), format="wav")
		if overlay :
			overlay = overlay.overlay(audio_segment,position=0)
		else :
			overlay = audio_segment
			
	overlay.export(f"converter/output/{user}/result.wav", format="wav")
	fx = (
		AudioEffectsChain()
		.reverb()
	)
	fx(f"converter/output/{user}/result.wav", f"converter/output/{user}/result_reverb.wav")

	logger(f"spleeter ({now_spleeter} seconds)")
	logger(f"basic pitch ({now_basicp} seconds)")
	logger(f"synthesize ({now_synth} seconds)")
	logger(f"overlay ({time.time()-now_overlay} seconds)")
	logger(f"done converting ({time.time()-now} seconds)")

	converted, sr = sf.read(f"converter/output/{user}/result_reverb.wav")
	audio_bytes = None
	with io.BytesIO() as bytes_io:
		sf.write(bytes_io, converted, sr, format='wav')
		bytes_io.seek(0)
		audio_bytes = bytes_io.read()
	proc.run(f"rm -rf converter/input/{user}".split(" "))
	proc.run(f"rm -rf converter/output/{user}".split(" "))
	return audio_bytes