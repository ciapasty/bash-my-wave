from django.utils import timezone
import logging

from .models import AudioFile

logger = logging.getLogger('debug.log')


def handle_uploaded_files(files):
    errorMessage = ''
    if (len(files) == 0):
        return 'No files selected for upload!'

    for f in files.keys():
        tempFile = files[f]
        existingFile = AudioFile.objects.filter(name=tempFile.name)
        if (len(existingFile) > 0):
            errorMessage += tempFile.name + ': file already exists.\n'
            break

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
    return errorMessage
