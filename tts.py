import sys
from TTS.api import TTS

DEFAULT_TTS_INDEX = 0
AUDIO_PATH = "output/"
tts = None


class Settings:
    def save_list(name, list) -> None:
        with open(name + "_list.txt", "w") as f:
            for m in list:
                f.write(m + "\n")

    def save_models() -> None: Settings.save_list("models", tts.list_models())
    def save_speakers() -> None: Settings.save_list("speakers", tts.speakers)

    def default_settings() -> dict(str, str):
        return dict(speaker=tts.speakers[2],
                    language=tts.languages[0],
                    emotion="Happy",
                    speed=4)


def load_tts(index=DEFAULT_TTS_INDEX) -> None:
    global tts
    tts = TTS(load_model(index))


def load_model(index: int) -> str:
    models = ["tts_models/multilingual/multi-dataset/your_tts",
              "tts_models/en/ljspeech/vits",
              "tts_models/en/vctk/vits",
              "tts_models/en/jenny/jenny"]
    return models[int(index)]


class Request:
    words = [str]
    filenames = str
    settings = dict(str, str)
    is_with_vc = False
    vc_path = str

    def __init__(self, words, filename=[str(hash(words))], vc_path=None,
                 settings=Settings.default_settings()) -> None:
        self.words, self.filename, self.settings = words, filename, settings

        if vc_path:
            self.is_with_vc = True
            self.vc_path = vc_path


def process_request(request: Request) -> None:
    global tts
    if not tts:  # if not loaded, load default model
        load_tts()

    # todo: iterate words array with vc array

    request.settings["text"] = request.words[0]
    request.settings["file_path"] = "".join(
        (AUDIO_PATH, request.filenames[0], ".wav"))

    if request.is_with_vc:
        request.settings["speaker_wav"] = request.vc_path
        tts.tts_with_vc_to_file(**request.settings)
    else:
        tts.tts_to_file(**request.settings)


def main() -> None:
    print("TTS: load, say, q")
    command = ""
    while command != "q":
        command = input("--> ")
        execute(command)

    sys.exit()


def execute(command: str) -> None:
    command_split = command.split()
    match command_split[:1][0]:
        case "load": load_tts(command_split[1:][0])
        case "say": process_request(Request(" ".join(command_split[1:])))
        case "save speakers": Settings.save_speakers()
        case "save models": Settings.save_models()
        case _: print("")


main()
