from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import UploadFileForm
from .Utility import handle_uploaded_files

import logging
logger = logging.getLogger('debug.log')


def index(request):
    return render(request, 'bashMyWave/index.html')


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        logger.info("form.isValid: " + str(form.is_valid()))
        # if form.is_valid():
        handle_uploaded_files(request.FILES)
        # return HttpResponseRedirect('/bashMyWave')

    return HttpResponseRedirect('/bashMyWave')


def wave(request, waveName):
    return render(request, 'bashMyWave/wave.html')
