from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from datetime import date
from django.db import models
from mutagen import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from pydub import AudioSegment
import os
import cv2
import wave

# Create your models here.


#client model
#take client details

    

class Order(models.Model):

    status_options = [('completed', 'Completed'), ('in_progress', 'In Progress')]

    file = models.FileField(upload_to='transcriptions/')
    duration = models.CharField(max_length=4)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rush = models.BooleanField(default=False)
    verbatim = models.BooleanField(default=False)
    turnaround = models.IntegerField()
    status = models.CharField(max_length=50, choices=status_options, default='in_progress')
    created_at = models.DateField(auto_now=True)
    


    def __str__(self):
        return f"{self.user} {self.name}"



    def save(self, *args, **kwargs):
        # Save the instance first to ensure the file is available
        super().save(*args, **kwargs)

        file_path = self.file.path

        if self.file:
            video_types = ['mp4', '.mkv', '.mov', '.avi', '.webm', '.flv', '.wmv', '.avchd', 'mpeg-4']
            audio_types = ['wav', 'mp3', 'flac', 'ogg', 'aac', 'wma', 'm4a', 'aiff', 'aifc', 'opus']

            if any(file_path.endswith(ext) for ext in video_types):
                #create video capture object
                cap = cv2.VideoCapture(file_path)

                #count the number of frames
                fps = cap.get(cv2.CAP_PROP_FPS)
                total_no_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

                # calculate duration
                if fps > 0:
                    duration_in_seconds = total_no_frames / fps
                else:
                    duration_in_seconds = 0

                minutes = int(duration_in_seconds / 60)
                seconds = int(duration_in_seconds % 60)
                self.duration = f'{minutes}:{seconds}'

                # Release the video capture object
                cap.release()

                # Save again to update the duration field
                super().save(*args, **kwargs)
            
            elif any(file_path.endswith(ext) for ext in audio_types):
                audio_file = AudioSegment.from_file(file_path)
                length = audio_file.duration_seconds

                minutes = int(length/60)
                seconds = int(length % 60)

                self.duration = f'{minutes}:{seconds}'

                super().save(*args, **kwargs)