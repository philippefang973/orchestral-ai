import random
import os
import io
import sys
import subprocess as proc 
import time
import random
import mimetypes

import soundfile as sf
from pydub import AudioSegment, effects
from pysndfx import AudioEffectsChain

def convert(filestorage,user,directory,logger=print) :
	logger("Audio uploaded, generating stems... (20%)")
	b = io.BytesIO(filestorage.read())
	audio, sr = sf.read(b)
	audio = audio[:30*sr]
	fn = filestorage.filename.split(".")[0]
	proc.run(f"mkdir {directory}/input/{user}".split(" "))
	proc.run(f"mkdir {directory}/output/{user}".split(" "))
	sf.write(f"{directory}/input/{user}/{fn}.wav",audio,sr)

	now = time.time()
	proc.run(f"mkdir {directory}/output/{user}/stems".split(" "))
	proc.run(f"mkdir {directory}/output/{user}/midis".split(" "))
	proc.run(f"mkdir {directory}/output/{user}/synths".split(" "))

	now_spleeter = time.time()
	audio = f"{directory}/input/{user}/{fn}.wav"
	logger(audio)
	cmd = f"spleeter separate -p spleeter:4stems -o {directory}/output/{user}/stems {audio} --verbose"
	proc.run(cmd.split(" "))
	logger(f"stems extracted")
	now_spleeter = time.time()-now_spleeter
	logger("Stems generated, generating MIDIs... (40%)")

	proc.run("ls -R".split(" "))
	now_basicp = time.time()
	stems_dir = f"{directory}/output/{user}/stems/"+audio.split("/")[-1].split(".")[0]
	stems = [os.path.join(stems_dir,f) for f in os.listdir(stems_dir) if "vocal" not in f]
	stem_vocal = [os.path.join(stems_dir,f) for f in os.listdir(stems_dir) if "vocal" in f][0]
	cmd = f"basic-pitch {directory}/output/{user}/midis "+" ".join(stems)
	proc.run(cmd.split(" "))
	cmd = f"cp {stem_vocal} {directory}/output/{user}/synths/."
	proc.run(cmd.split(" "))

	logger("midis generation done")
	now_basicp = time.time() - now_basicp
	logger("MIDIs generated, synthesizing with soundfonts... (60%)")
	now_synth = time.time()
	soundfont_path = "{directory}/kaggle/sonanita-sf2"
	soundfont_files = os.listdir(soundfont_path)

	brass_sf = [sf2 for sf2 in soundfont_files if "Brass" in sf2 and "Bass" not in sf2]
	brass_bass_sf = [sf2 for sf2 in soundfont_files if "Brass" in sf2 and "Bass" in sf2]
	keys_sf = [sf2 for sf2 in soundfont_files if "Keys" in sf2]
	percussions_sf = [sf2 for sf2 in soundfont_files if "Percussion" in sf2]
	string_sf = [sf2 for sf2 in soundfont_files if "Strings" in sf2 and "Bass" not in sf2]
	string_bass_sf = [sf2 for sf2 in soundfont_files if "Strings" in sf2 and "Bass" in sf2]
	woodwind_sf = [sf2 for sf2 in soundfont_files if "Woodwinds" in sf2 and "Bass" not in sf2]
	woodwind_bass_sf = [sf2 for sf2 in soundfont_files if "Woodwinds" in sf2 and "Bass" in sf2]

	midi_files = [f for f in os.listdir(f"{directory}/output/{user}/midis")]

	synth_dir = f"{directory}/output/{user}/synths"
	for midi in midi_files :
		midi_path = os.path.join(f"{directory}/output/{user}/midis",midi)
		if "other" in midi : 
			sfz1 = os.path.join(soundfont_path,random.choice(string_sf))
			sfz2 = os.path.join(soundfont_path,random.choice(brass_sf))
			sfz3 = os.path.join(soundfont_path,random.choice(woodwind_sf))
			sfz4 = os.path.join(soundfont_path,random.choice(keys_sf))
			logger(sfz1)
			synth_path = os.path.join(synth_dir,midi.split("_")[0]+"_synth1.wav")
			proc.run(["midi2audio","-r","44100","-s",sfz1,midi_path,synth_path])			
			logger(sfz2)
			synth_path = os.path.join(synth_dir,midi.split("_")[0]+"_synth2.wav")
			proc.run(["midi2audio","-r","44100","-s",sfz2,midi_path,synth_path])
			logger(sfz3)
			synth_path = os.path.join(synth_dir,midi.split("_")[0]+"_synth3.wav")
			proc.run(["midi2audio","-r","44100","-s",sfz3,midi_path,synth_path])	
			logger(sfz4)
			synth_path = os.path.join(synth_dir,midi.split("_")[0]+"_synth4.wav")
			proc.run(["midi2audio","-r","44100","-s",sfz4,midi_path,synth_path])	
		elif "bass" in midi : 
			sfz1 = os.path.join(soundfont_path,random.choice(string_bass_sf))
			sfz2 = os.path.join(soundfont_path,random.choice(brass_bass_sf))
			sfz3 = os.path.join(soundfont_path,random.choice(woodwind_bass_sf))
			logger(sfz1)
			synth_path = os.path.join(synth_dir,midi.split("_")[0]+"_synth1.wav")
			proc.run(["midi2audio","-r","44100","-s",sfz1,midi_path,synth_path])			
			logger(sfz2)
			synth_path = os.path.join(synth_dir,midi.split("_")[0]+"_synth2.wav")
			proc.run(["midi2audio","-r","44100","-s",sfz2,midi_path,synth_path])
			logger(sfz3)
			synth_path = os.path.join(synth_dir,midi.split("_")[0]+"_synth3.wav")
			proc.run(["midi2audio","-r","44100","-s",sfz3,midi_path,synth_path])
		else :
			sfz = ""
			if "drums" in midi : 
				sfz = os.path.join(soundfont_path,random.choice(percussions_sf))
			logger(sfz)
			synth_path = os.path.join(synth_dir,midi.split("_")[0]+"_synth.wav")
			proc.run(["midi2audio","-r","44100","-s",sfz,midi_path,synth_path])
	logger("synths generated")
	now_synth = time.time()-now_synth
	logger("MIDI synthesized, overlaying sounds... (80%)")
	now_overlay = time.time()
	synth_files = [f for f in os.listdir(synth_dir)]
	overlay = None
	for s in synth_files :
		audio_segment = AudioSegment.from_file(os.path.join(synth_dir,s), format="wav")
		audio_segment = audio_segment+3 if "vocal" not in s else audio_segment-12 #effects.normalize(audio_segment)  
		if overlay :
			overlay = overlay.overlay(audio_segment,position=0)
		else :
			overlay = audio_segment
			
	overlay.export(f"{directory}/output/{user}/result.wav", format="wav")
	fx = (
		AudioEffectsChain()
		.reverb(reverberance=70,
               hf_damping=70,
               room_scale=90,
               stereo_depth=100,
               pre_delay=10,
               wet_gain=0,
               wet_only=False)
	)
	output = f"{fn}_converted.wav"
	fx(f"{directory}/output/{user}/result.wav", f"{directory}/output/{user}/{output}")

	logger(f"spleeter ({now_spleeter} seconds)")
	logger(f"basic pitch ({now_basicp} seconds)")
	logger(f"synthesize ({now_synth} seconds)")
	logger(f"overlay ({time.time()-now_overlay} seconds)")
	logger(f"done converting ({time.time()-now} seconds)")
	logger("Overlaying finished, updating database... (99%)")

	converted, sr = sf.read(f"{directory}/output/{user}/{output}")
	audio_bytes = None
	with io.BytesIO() as bytes_io:
		sf.write(bytes_io, converted, sr, format='wav')
		bytes_io.seek(0)
		audio_bytes = bytes_io.read()
	proc.run(f"rm -rf {directory}/input/{user}".split(" "))
	proc.run(f"rm -rf {directory}/output/{user}".split(" "))
	return audio_bytes, output, mimetypes.guess_type(f"{directory}/output/{user}/{output}")[0]