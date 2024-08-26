from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='pics',default='default.png')
    bio = models.TextField(default=None,blank=True)
    role = (('participent', 'Participent'), ('admin', 'Admin'))
    acc_type = models.CharField(max_length=100, choices=role, default='participent')

    def __str__(self):
        return self.user.username

class ConsentDocument(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = RichTextField(blank=True,null=True)
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ConsentStatus(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('signed', 'Signed'),
        ('declined', 'Declined'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(ConsentDocument, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    signed_at = models.DateTimeField(null=True, blank=True)
    declined_at = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(blank=True)

class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('document_upload', 'Document Upload'),
        ('consent_signed', 'Consent Signed'),
        # Add more choices as needed
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField()