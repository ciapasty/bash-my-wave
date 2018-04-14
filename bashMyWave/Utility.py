from django.utils import timezone
from django.core.files.storage import FileSystemStorage

from .models import AudioFile

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

    fs = FileSystemStorage()
    filename = fs.save(tempFile.name, tempFile)
    uploaded_file_url = fs.url(filename)

    # filePath = 'media/' + tempFile.name
    # with open(filePath, 'wb') as destination:
    #     for chunk in tempFile.chunks():
    #         destination.write(chunk)

    audioFile = AudioFile(
        upload_date=timezone.now(),
        user='mattijah',
        name=tempFile.name,
        file_path=uploaded_file_url,
        waveform_short=''  # TODO: make proper handling
    )
    
    audioFile.save()

    return (audioFile.id, '')
