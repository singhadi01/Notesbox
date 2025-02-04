from django.db import models
from django.contrib.auth.models import User
import re
import random
import string

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensure each subject is unique
    code = models.CharField(max_length=6,blank=True,unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    def generate_unique_code(self):
        code = ''.join(random.choices(string.digits, k=6))
        while Subject.objects.filter(code=code).exists():
            code = ''.join(random.choices(string.digits, k=6))
        return code
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
            super(Subject, self).save(*args, **kwargs)
    def __str__(self):
        return self.name

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # Link each video to a subject
    title = models.CharField(max_length=255)
    link = models.URLField()
    embed_link = models.URLField(blank=True, null=True) 
            
    def convert_to_embed(self,link):
        match = re.search(r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|shorts/|live/))([\w-]+)", link)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"
        return "Invalid YouTube link"
    def save(self, *args, **kwargs):
        if not self.embed_link:
            self.embed_link = self.convert_to_embed(self.link)  # Auto-generate embed link if not present
        super(Video, self).save(*args, **kwargs)  
    def __str__(self):
        return self.title
