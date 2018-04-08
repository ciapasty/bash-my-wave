from django.utils import timezone
import logging

from .models import AudioFile

logger = logging.getLogger('debug.log')


def handle_uploaded_files(files):
    for f in files.keys():
        tempFile = files[f]
        logger.error(tempFile)
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
