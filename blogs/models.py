from django.db import models

class Post(models.Model):
    headline = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    publication = models.BooleanField(default=False)
    views = models.IntegerField(default=0)  # Изменено с Views на views

    def __str__(self):
        return self.headline

    class Meta:
        app_label = 'blogs'
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']