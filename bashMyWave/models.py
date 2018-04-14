from django.db import models


class AudioFile(models.Model):
    upload_date = models.DateTimeField('date uploaded')
    user = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    file_path = models.CharField(max_length=200)
    waveform_short = models.TextField()

    def __str__(self):
        return self.name


class Comment(models.Model):
    audiofile = models.ForeignKey(AudioFile, on_delete=models.CASCADE)
    time_posted = models.DateTimeField('date posted')
    user = models.CharField(max_length=200)
    audio_time = models.PositiveIntegerField()
    text = models.TextField()

    def __str__(self):
        return self.text
