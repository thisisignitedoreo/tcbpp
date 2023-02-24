from argparse import ArgumentParser
from pydub import AudioSegment
import random
import json
import lib
import os

def print_progress_bar(value, max_value, pb_len):
    print(f"[{''.join(['#' if i / pb_len < value / max_value else ' ' for i in range(pb_len)])}], {round(value / max_value * 100)}%", end="\r")

def recognize_macro(path):
    if os.path.basename(path).endswith(".echo"): 
        return load_macro(path, 1)
    elif os.path.basename(path).endswith(".mcb.json"):
        return load_macro(path, 4)
    elif os.path.basename(path).endswith(".json"):
        file = json.loads(open(path).read())
        if file.get("actions") is None:
            return load_macro(path, 2)
        else:
            return load_macro(path, 5)
    elif os.path.basename(path).endswith(".replay"):
        return load_macro(path, 3)
    else:
        print("Can't determine macro type, selecting Plain Text. You can manually set type by --type argument.")
        return load_macro(path, 0)

def load_macro(path, macro_type):
    if macro_type == 0:
        print("Type: Plain Text (frames)")
        replay_list = open(path).readlines()
        nl = "\n" # sorry
        print(f"FPS: {float(replay_list[0].replace(nl, ''))}")

        print(f"Macro Length: {len(replay_list) - 1}")

        macro = {"fps": float(replay_list[0].replace("\n", "")), "actions": []}
        
        for k, i in list(enumerate(replay_list))[1:]:
            splited = i.split()
            # frame: splited[0]
            # pl_1: not not int(splitted[1])
            # pl_2: not not int(splitted[2])
            macro["actions"].append([int(splited[0]), not not int(splited[1]), not not int(splited[2])])
        return macro

    elif macro_type == 1:
        print("Type: EchoBot")
        json_data = json.load(open(path))
        print(f"FPS: {json_data['FPS']}")

        print(f"Macro Length: {len(json_data['Echo Replay']) - 1}")
        
        replay = convert([i["Hold"] for i in json_data["Echo Replay"]])
        macro = []
        
        for k, i in enumerate(replay):
            macro.append([i[0], i[1], None])
        
        return {"fps": json_data["FPS"], "actions": macro}
    elif macro_type == 2:
        print("Type: TasBot")
        json_data = json.load(open(path))
        print(f"FPS: {json_data['fps']}")
        
        replay = [[i["frame"], i["player_1"]["click"], i["player_2"]["click"]] for i in json_data["macro"]]
        
        print(f"Macro Length: {len(replay) - 1}")

        macro = []
        
        for k, i in enumerate(replay):
            macro.append([i[0], [None, False, True][i[1]], [None, False, True][i[2]]])
        
        return {"fps": json_data["fps"], "actions": macro}
    elif macro_type == 3:
        print("Type: ReplayBot")
        with open(path, "rb") as f:
            length = os.path.getsize(path)
            magic = f.read(4)
            if magic != b"RPLY":
                print("This macro is either too old or corrupted")
                exit(1)
        
            version = int.from_bytes(f.read(1), "big")
            frames = False
            if version == 2:
                frames = int.from_bytes(f.read(1), "big") == 1
            
            if frames:
                macro = []
                
                fps = struct.unpack("f", f.read(4))[0]
                print(f"FPS: {fps}")
                
                print(f"Macro Length: {(length - f.tell()) / 5}")
                
                for k, i in enumerate(range(0, (length - f.tell()), 5)):
                    frame = int.from_bytes(f.read(4), "little")
                    state = int.from_bytes(f.read(1), "little")
                    p1 = not not state & 0x1
                    p2 = not not state >> 1
                    macro.append([frame, p1, p2])
                return {"fps": fps, "actions": macro}
            else:
                print("This macro is not recorded with frames")
                exit(1)
        self.log_info("Successfully decoded \"ReplayBot\" replay!")
    elif macro_type == 4:
        print("Type: MacroBot")
        json_data = json.load(open(path))
        print(f"FPS: {json_data['fps']}")
        
        print(f"Macro Length: {len(json['actions']) - 1}")
        
        replay = [[i["frame"], i["press"], i["player2"]] for i in json_data["actions"]]
        
        return {"fps": json_data["fps"], "actions": replay}
    elif macro_type == 5:
        print("Type: DashReplay")
        json_data = json.load(open(path))
        print(f"FPS: {json_data['fps']}")
        
        replay = convert([i["down"] for i in json_data["actions"]])
        
        macro = []

        print(f"Macro Length: {len(replay) - 1}")
        
        for k, i in enumerate(replay):
            macro.append([i[0], i[1], None])

        return {"fps": json_data["fps"], "actions": macro}

def convert(array):
    old = array[0]
    res = [[0, old]]
    for k, i in enumerate(array):
        if i != old:
            res.append([k, i])
        old = i
    return res

def add_end(text, end):
    return text if text.endswith(end) else text + end

def render_audio(macro, clickpack, end_delay, out_path, mp3_export, soft_delay, hard_delay, soft, hard):
    fps = macro["fps"]
    ms_duration = (macro["actions"][-1][0] / fps * 1000)
    output = AudioSegment.silent(duration=ms_duration + end_delay)

    p1_overrides_p2 = False

    holds_p1 = os.listdir(add_end(clickpack, "/") + "p1/holds")
    releases_p1 = os.listdir(add_end(clickpack, "/") + "p1/releases")
    try:
        holds_p2 = os.listdir(add_end(clickpack, "/") + "p2/holds")
        releases_p2 = os.listdir(add_end(clickpack, "/") + "p2/releases")
    except FileNotFoundError:
        print("No player 2 found in clickpack! Defaulting to player 1 clicks.")
        p1_overrides_p2 = True
        holds_p2 = os.listdir(add_end(clickpack, "/") + "p1/holds")
        releases_p2 = os.listdir(add_end(clickpack, "/") + "p1/releases")
    try:
        softclicks = os.listdir(add_end(clickpack, "/") + "softclicks")
    except FileNotFoundError:
        print("No softclicks found in clickpack! Turning it off.")
        soft = False
    try:
        hardclicks = os.listdir(add_end(clickpack, "/") + "hardclicks")
    except FileNotFoundError:
        print("No hardclicks found in clickpack! Turning it off.")
        hard = False
    for k, i in enumerate(macro["actions"]):
        if k == 0:
            delay = -1
        else:
            delay = (i[0] / fps * 1000) - (macro["actions"][k - 1][0] / fps * 1000)
        if delay <= soft_delay and soft:
            if i[1]:
                output = output.overlay(AudioSegment.from_wav(add_end(clickpack, "/") + "softclicks/" + random.choice(softclicks)),
                                        position=i[0] / fps * 1000)
            elif not i[1]:
                output = output.overlay(AudioSegment.from_wav(add_end(clickpack, "/") + "p1/releases/" + random.choice(releases_p1)),
                                        position=i[0] / fps * 1000)
            if i[2] is True:
                output = output.overlay(AudioSegment.from_wav(add_end(clickpack, "/") + "softclicks/" + random.choice(softclicks)),
                                        position=i[0] / fps * 1000)
            elif not i[2] is True:
                output = output.overlay(AudioSegment.from_wav(add_end(clickpack, "/") + f"p{'1' if p1_overrides_p2 else '2'}/releases/" + random.choice(releases_p2)),
                                        position=i[0] / fps * 1000)
        elif delay >= hard_delay and hard:
            if i[1]:
                output = output.overlay(AudioSegment.from_wav(add_end(clickpack, "/") + "hardclicks/" + random.choice(hardclicks)),
                                        position=i[0] / fps * 1000)
            elif not i[1]:
                output = output.overlay(AudioSegment.from_wav(add_end(clickpack, "/") + "p1/releases/" + random.choice(releases_p1)),
                                        position=i[0] / fps * 1000)
            if i[2] is True:
                output = output.overlay(AudioSegment.from_wav(add_end(clickpack, "/") + "hardclicks/" + random.choice(hardclicks)),
                                        position=i[0] / fps * 1000)
            elif not i[2] is True:
                output = output.overlay(AudioSegment.from_wav(add_end(clickpack, "/") + f"p{'1' if p1_overrides_p2 else '2'}/releases/" + random.choice(releases_p2)),
                                        position=i[0] / fps * 1000)
        else:
            if i[1]:
                output = output.overlay(AudioSegment.from_wav(add_end(clickpack, "/") + "p1/holds/" + random.choice(holds_p1)),
                                        position=i[0] / fps * 1000)
            elif not i[1]:
                output = output.overlay(AudioSegment.from_wav(add_end(clickpack, "/") + "p1/releases/" + random.choice(releases_p1)),
                                        position=i[0] / fps * 1000)
            if i[2] is True:
                output = output.overlay(AudioSegment.from_wav(add_end(clickpack, "/") + f"p{'1' if p1_overrides_p2 else '2'}/holds/" + random.choice(holds_p2)),
                                        position=i[0] / fps * 1000)
            elif not i[2] is True:
                output = output.overlay(AudioSegment.from_wav(add_end(clickpack, "/") + f"p{'1' if p1_overrides_p2 else '2'}/releases/" + random.choice(releases_p2)),
                                        position=i[0] / fps * 1000)
        print_progress_bar(k, len(macro["actions"]), os.get_terminal_size()[0] - 10)
    print()
    
    if mp3_export:
        output.export(out_path, format="mp3", bitrate="320k")
    else:
        output.export(out_path, format="wav", bitrate="320k")

print(f"tcb++ version {lib.ver}")

parser = ArgumentParser(prog="tcb++ console", description="console version of tcb++")
parser.add_argument("-i", "--input", dest="input_path", required=True, help="input file")
parser.add_argument("-o", "--output", dest="output_path", required=True, help="output file")
parser.add_argument("--clickpack", dest="clickpack", required=True, help="clickpack folder")
parser.add_argument("--end-delay", dest="end_delay", required=False, default=3, type=int, help="end delay (int)")
parser.add_argument("--mp3-export", dest="mp3_export", required=False, default=False, action="store_true", help="export as mp3?")
parser.add_argument("--softclicks", dest="softclicks", required=False, action="store_true", help="use softclicks?")
parser.add_argument("--hardclicks", dest="hardclicks", required=False, action="store_true", help="use hardclicks?")
parser.add_argument("--softclick-delay", dest="softclick_delay", required=False, default=200, type=int, help="softclick delay (ms)")
parser.add_argument("--hardclick-delay", dest="hardclick_delay", required=False, default=500, type=int, help="hardclick delay (ms)")
parser.add_argument("--type", dest="type", required=False, choices=["plain-text", "macrobot", "replaybot", "echobot", "tasbot", "dashreplay"], help="overwrite standart type recognition")

args = parser.parse_args()

types = {
    "plain-text": 0,
    "echobot": 1,
    "tasbot": 2,
    "replaybot": 3,
    "macrobot": 4,
    "dashreplay": 5,
}

if args.type is not None:
    render_audio(load_macro(args.input_path, types[args.type]), args.clickpack, args.end_delay, args.output_path, args.mp3_export, args.softclick_delay, args.hardclick_delay, args.softclicks, args.hardclicks)
else:
    render_audio(recognize_macro(args.input_path), args.clickpack, args.end_delay, args.output_path, args.mp3_export, args.softclick_delay, args.hardclick_delay, args.softclicks, args.hardclicks)
