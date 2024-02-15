import torch
import torch.nn as nn
import pretty_midi
import os
import re

class LSTMNetwork(nn.Module):
   def __init__(self, n_vocab, seq_size, embedding_size, lstm_size):
       super(LSTMNetwork, self).__init__()
       self.seq_size = seq_size
       self.lstm_size = lstm_size
       self.embedding = nn.Embedding(n_vocab, embedding_size)
       self.lstm = nn.LSTM(embedding_size,
                           lstm_size,
                           batch_first=True)
       self.dense = nn.Linear(lstm_size, n_vocab)

   def forward(self, x, prev_state):
       embed = self.embedding(x)
       output, state = self.lstm(embed, prev_state)
       logits = self.dense(output)

       return logits, state

   def zero_state(self, batch_size):
       return (torch.zeros(1, batch_size, self.lstm_size),
               torch.zeros(1, batch_size, self.lstm_size))


def run_check() :
    print("Run check torch...")
    x = torch.rand(5, 3)
    print(x)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Device:', device)

def convert_to_midi_dict(f) :
    res = dict()
    midi_data = pretty_midi.PrettyMIDI(f)
    res["tempo"]=midi_data.estimate_tempo()
    res["beats"]=midi_data.get_beats()
    res["instruments"]=[]
    for inst in midi_data.instruments :
        notes_list = []
        for nt in inst.notes :
            dict_note = dict()
            dict_note["pitch"] = nt.pitch
            dict_note["velocity"] = nt.velocity
            dict_note["start"] = nt.start
            dict_note["end"] = nt.end
            notes_list+=[dict_note]
        res["instruments"]+=[notes_list]
    return res

def get_all_midi(path,pattern) :
    res = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if re.match(pattern,name) :
                res+=[os.path.join(root, name)]
    return res

path = '../../datasets/'  
run_check()
midi_files = get_all_midi(path,".*midi?$")
print("Number of MIDI files",len(midi_files))
for f in midi_files : convert_to_midi_dict(f)

