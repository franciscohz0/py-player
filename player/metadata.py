from pathlib import Path

from mutagen._file import File
from mutagen.id3 import ID3

def getMetadata(filePath):

    audio = File(filePath, easy=True)

    if audio is None:
        return {
            'title': Path(filePath).stem,
            'artist': 'Artista Desconocido'
        }

    return {
        'title': audio.get(
            'title',
            [Path(filePath).stem]
        )[0],

        'artist': audio.get(
            'artist',
            ['Artista Desconocido']
        )[0]
    }

def getCover(filePath):

    try:
        audio = File(filePath)

        if audio is not None:

            # FLAC
            if hasattr(audio, "pictures"):
                if audio.pictures:
                    return audio.pictures[0].data

            # M4A
            if "covr" in audio:
                return bytes(audio["covr"][0])

            # MP3
            tags = ID3(filePath)

            for tag in tags.values():

                if tag.FrameID == "APIC":
                    return tag.data

    except Exception as error:
        print(f'Error loading cover: {error}')

    return None