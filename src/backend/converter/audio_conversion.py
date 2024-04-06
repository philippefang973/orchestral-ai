import io
import random
import os
import soundfile as sf
import subprocess as proc
import time

# configure kaggle
homedir = os.path.expanduser("~")
proc.run(f"pwd")
cmd = f"cp converter/kaggle/credentials/kaggle.json {homedir}/.kaggle/."
proc.run(cmd.split(" "))
cmd = f"chmod 600 {homedir}/.kaggle/kaggle.json"
proc.run(cmd.split(" ")) 
import kaggle

def kaggle_run(user=".soy") :

    # upload to kaggle dataset
    print("upload dataset")
    cmd = f"kaggle datasets metadata philippefang/orchestralai-input -p converter/input/{user}"
    proc.run(cmd.split(" "))
    proc.run(["kaggle","datasets","version","-p",f"converter/input/{user}","-m",f"\"client {user} file\""])

    # run kaggle notebook
    print("run notebook")
    cmd = "kaggle kernels pull -p converter/kaggle/kernels -m philippefang/orchestralai"
    proc.run(cmd.split(" "))
    cmd = "kaggle kernels push -p converter/kaggle/kernels"
    proc.run(cmd.split(" "))
    
    status = 'running'
    now = time.time()
    while(status!='complete') :
        status = kaggle.api.kernels_status("philippefang/orchestralai")['status']
        print("{:.2f} {}".format(time.time()-now,status),end='\r')
    print("notebook finished")

    cmd = f"kaggle kernels output philippefang/orchestralai -p converter/output/{user}"
    proc.run(cmd.split(" "))
    print("output retrieved")


def convert(filestorage,user) :
    b = io.BytesIO(filestorage.read())
    audio, sr = sf.read(b)
    audio = audio[:30*sr]
    fn= filestorage.filename.split(".")[0]
    proc.run(f"mkdir converter/input/{user}".split(" "))
    proc.run(f"mkdir converter/output/{user}".split(" "))
    sf.write(f"converter/input/{user}/{fn}.wav",audio,sr)
    kaggle_run(user)
    converted, sr = sf.read(f"converter/output/{user}/result_reverb.wav")
    audio_bytes = None
    with io.BytesIO() as bytes_io:
        sf.write(bytes_io, converted, sr, format='wav')
        bytes_io.seek(0)
        audio_bytes = bytes_io.read()
    proc.run(f"rm -rf converter/input/{user}".split(" "))
    proc.run(f"rm -rf converter/output/{user}".split(" "))
    return audio_bytes