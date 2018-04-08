from django.utils import timezone
import logging

from .models import AudioFile

logger = logging.getLogger('debug.log')


def handle_uploaded_file(file):
    if (len(file) == 0):
        return (None, 'No files selected for upload!')

    tempFile = file['file']
    existingFile = AudioFile.objects.filter(name=tempFile.name)
    if (len(existingFile) > 0):
        return (None, tempFile.name + ': file already exists.\n')

    logger.info('Processing: ' + tempFile.name)
    filePath = 'media/' + tempFile.name
    with open(filePath, 'wb') as destination:
        for chunk in tempFile.chunks():
            destination.write(chunk)

    audioFile = AudioFile(
        upload_date=timezone.now(),
        user='mattijah',
        name=tempFile.name,
        file_path=filePath,
        waveform_short=''  # TODO: make proper handling
    )
    
    audioFile.save()

    return (audioFile.name, '')
