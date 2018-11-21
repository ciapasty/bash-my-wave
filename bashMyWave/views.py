from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import FileResponse
# from django.core.files import File

# from .forms import UploadFileForm
from .models import AudioFile, Comment
from .Utility import handle_uploaded_file

import logging
logger = logging.getLogger('debug.log')


def index(request):
    errorMessage = ''
    if request.method == 'POST':
        # form = UploadFileForm(request.POST, request.FILES)
        # logger.info("form.isValid: " + str(form.is_valid()))
        # if form.is_valid():
        audioFileID, errorMessage = handle_uploaded_file(request.FILES)
        if (audioFileID is not None):
            return HttpResponseRedirect(reverse('bashMyWave:wave', args=(audioFileID,)))

    return render(
        request,
        'bashMyWave/index.html',
        {
            'error_message': errorMessage,
            'last20_audiofiles': AudioFile.objects.order_by('-upload_date')[:20]
        }
    )


def wave(request, waveID):
    audioFile = get_object_or_404(AudioFile, pk=waveID)
    return render(
        request,
        'bashMyWave/wave.html',
        {
            'audiofile': audioFile,
            'comments': Comment.objects.filter(audiofile=audioFile)
        }
    )


def mediaServe(request, waveID, filename):
    if (request.method == 'GET'):
        audioFile = get_object_or_404(AudioFile, pk=waveID)
        # f = File(audioFile.file)
        # if filename is None:
        #     raise ValueError("Found empty filename")
        response = FileResponse(audioFile.file, content_type="audio/x-wav")
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response
