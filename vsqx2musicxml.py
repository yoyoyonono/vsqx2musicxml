from typing import Iterable, OrderedDict
import xmltodict
from pymusicxml import *
import os

def select_from_iterable(thing: Iterable) -> int:
    print(*(f'{x}: {y}' for (x, y) in enumerate(thing)), sep='\n')
    return int(input('?'))

def select_name_v3(voiceList: OrderedDict) -> int:
    print(*(f'{x["vVoiceName"]}: {y}' for (x, y) in voiceList.items()), sep='\n')
    return int(input('?'))

def select_name_v4(voiceList: OrderedDict) -> int:
    print(*(f'{x}: {y["name"]}' for x,y in enumerate(voiceList)), sep='\n')
    return int(input('?'))
    

os.chdir(os.getcwd())
fileList = sorted(os.listdir('./input/'), key=str.casefold)
print('Which score?')
fileName = fileList[select_from_iterable(fileList)]
obj: OrderedDict = xmltodict.parse(open(f'input/{fileName}', encoding='utf-8').read())
version: int = int(list(obj.keys())[0][3])
obj = next(iter(obj.values()))
score = Score(title=input("Title:"), composer=input("Composer:"))

partName: str
vpc: int
if version == 3:
    if type(obj['vVoiceTable']['vVoice']) == list:
        print('Which voice?')
        partName = obj['vVoiceTable']['vVoice'][select_name_v3(obj['vVoiceTable']['vVoice'])]['name']
    else:
        partName = obj['vVoiceTable']['vVoice']['vVoiceName']
        vpc = obj['vVoiceTable']['vVoice']['']
elif version == 4:
    if type(obj['vVoiceTable']['vVoice']) == list:
        print('Which voice?')
        partName = obj['vVoiceTable']['vVoice'][select_name_v4(obj['vVoiceTable']['vVoice'])]['name']
    else:
        partName = obj['vVoiceTable']['vVoice']['name']
part = Part(part_name=partName)
score.append(part)
measures = []
measureCount = 1
timeSigs = {}
if version == 3:
    if type(obj['masterTrack']['timeSig']) == list:
        for x in obj['masterTrack']['timeSig']:
            timeSigs[x['posMes']] = (x['nume'], x['denomi'])
    else:
        timeSigs = {0:(obj['masterTrack']['timeSig']['nume'], obj['masterTrack']['timeSig']['denomi'])}
elif version == 4:
    if type(obj['masterTrack']['timeSig']) == list:
        for x in obj['masterTrack']['timeSig']:
            timeSigs[x['m']] = (x['nu'], x['de'])
    else:
        timeSigs = {0:(obj['masterTrack']['timeSig']['nu'], obj['masterTrack']['timeSig']['de'])}

tempos = {}
if version == 3:
    if type(obj['masterTrack']['tempo']) == list:
        for x in obj['masterTrack']['tempo']:
            tempos[x['posTick']] = x['bpm']
    else:
        tempos = {0: obj['masterTrack']['tempo']['bpm']}
elif version == 4:
    if type(obj['masterTrack']['tempo']) == list:
        for x in obj['masterTrack']['tempo']:
            tempos[x['t']] = x['v']
    else:
        tempos = {0: obj['masterTrack']['tempo']['v']}
score.export_to_file(f'output/{"".join(fileName.split(".")[:-1])}.musicxml')

measures = []
musicPart: OrderedDict
notes: list
if version == 3:
    if type(obj['vsTrack']) == list:
        for x in obj['vsTrack']:
            if x['trackName'] == partName:
                musicPart = x['musicalPart']
    else:
        musicPart = obj['vsTrack']['musicalPart']
    notes = musicPart['note']
elif version == 4:
    if type(obj['vsTrack']) == list:
        for x in obj['vsTrack']:
            if x['name'] == partName:
                musicPart = x['vsPart']
    else:
        musicPart = obj['vsTrack']['vsPart']
    notes = musicPart['note']
print(notes)