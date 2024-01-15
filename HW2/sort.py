from pathlib import Path
import re
import sys
import shutil
from abc import ABC, abstractmethod


class FileHandler(ABC):
    @abstractmethod
    def handle(self, file_name: Path, target_folder: Path):
        pass


class ImageHandler(FileHandler):
    def handle(self, file_name: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        file_name.replace(target_folder / self.normalize(file_name.name))


class AudioHandler(FileHandler):
    def handle(self, file_name: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        file_name.replace(target_folder / self.normalize(file_name.name))


class VideoHandler(FileHandler):
    def handle(self, file_name: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        file_name.replace(target_folder / self.normalize(file_name.name))


class DocumentHandler(FileHandler):
    def handle(self, file_name: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        file_name.replace(target_folder / self.normalize(file_name.name))


class ArchiveHandler(FileHandler):
    def handle(self, file_name: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        folder_for_file = target_folder / self.normalize(file_name.name.replace(file_name.suffix, ''))
        folder_for_file.mkdir(exist_ok=True, parents=True)
        try:
            shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
        except shutil.ReadError:
            folder_for_file.rmdir()
            return
        file_name.unlink()


class FileSorter:
    CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

    MAP = {}

    for cirilic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        MAP[ord(cirilic)] = latin
        MAP[ord(cirilic.upper())] = latin.upper()

    def __init__(self, source_folder):
        self.source_folder = source_folder
        self.handlers = {
            'JPEG': ImageHandler(),
            'JPG': ImageHandler(),
            'PNG': ImageHandler(),
            'SVG': ImageHandler(),
            'MP3': AudioHandler(),
            'OGG': AudioHandler(),
            'WAV': AudioHandler(),
            'AMR': AudioHandler(),
            'AVI': VideoHandler(),
            'MP4': VideoHandler(),
            'MOV': VideoHandler(),
            'MKV': VideoHandler(),
            'DOC': DocumentHandler(),
            'DOCX': DocumentHandler(),
            'TXT': DocumentHandler(),
            'PDF': DocumentHandler(),
            'XLSX': DocumentHandler(),
            'PPTX': DocumentHandler(),
            'ZIP': ArchiveHandler(),
            'GZ': ArchiveHandler(),
            'TAR': ArchiveHandler()
        }

    def get_extension(self, name):
        return Path(name).suffix[1:].upper()

    def scan(self, folder):
        pass  # Реалізуємо пізніше

    def normalize(self, name):
        string = name.translate(self.MAP)
        translated_name = re.sub(r'[^a-zA-Z.0-9_]', '_', string)
        return translated_name

    def core(self):
        pass  # Реалізуємо пізніше

    def start(self):
        if len(sys.argv) > 1:
            folder_process = Path(sys.argv[1])
            self.scan(folder_process)
            self.core()


if __name__ == "__main__":
    file_sorter = FileSorter(Path())
    file_sorter.start()
