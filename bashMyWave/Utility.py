from django.utils import timezone

from .models import AudioFile
from . import WaveReader

import logging
logger = logging.getLogger('debug.log')


def handle_uploaded_file(files):
    if (len(files) == 0):
        return (None, 'No files selected for upload!')

    tempFile = files['file']
    logger.info(files)
    existingFile = AudioFile.objects.filter(name=tempFile.name)
    if (len(existingFile) > 0):
        return (None, tempFile.name + ': file already exists.\n')

    #rawAudio = WaveReader.read(tempFile.temporary_file_path)

    audioFile = AudioFile(
        upload_date=timezone.now(),
        user='mattijah',
        name=tempFile.name,
        file=tempFile
        #waveform_short=WaveReader.generateWaveformSummary(rawAudio['riffHeader'], 1000, rawAudio['audioData'])
    )
    
    audioFile.save()

    return (audioFile.id, '')
