from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import UploadFileForm
from .models import AudioFile
from .Utility import handle_uploaded_file

import logging
logger = logging.getLogger('debug.log')


def index(request):
    errorMessage = ''
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        logger.info("form.isValid: " + str(form.is_valid()))
        # if form.is_valid():
        audioFile, errorMessage = handle_uploaded_file(request.FILES)
        if (audioFile is not None):
            return HttpResponseRedirect(reverse('bashMyWave:wave', args=(audioFile,)))

    return render(
        request,
        'bashMyWave/index.html',
        {
            'error_message': errorMessage,
            'last20_audiofiles': AudioFile.objects.order_by('-upload_date')[:20]
        }
    )


def wave(request, waveID):
    return render(request, 'bashMyWave/wave.html')
