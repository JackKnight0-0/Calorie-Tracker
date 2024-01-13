from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from PIL import Image


class UserProfile(models.Model):
    user = models.OneToOneField(to=get_user_model(), related_name='user_profile', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', default='avatars/default_avatar.jpg', null=True,
                               blank=True)
    slug = models.SlugField(unique=True, db_index=True, editable=False)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return

    class Meta:
        verbose_name = 'Userprofile'
        verbose_name_plural = 'Userprofile'

    def save(
            self, *args, **kwargs
    ):
        """
        Composes a slug with the username. Resizes the image to the specified size.
        """
        self.slug = slugify(self.user.username)
        print(self.avatar.path, self.avatar)
        super().save(*args, **kwargs)

        if self.avatar and self.avatar is not None:
            try:
                current_avatar = Image.open(self.avatar.path)
            except (ValueError, FileNotFoundError):
                self.avatar = 'avatars/default_avatar.jpg'
            else:
                if current_avatar.width > 300 or current_avatar.height > 300:
                    resize = (300, 300)
                    current_avatar.thumbnail(resize)
                    current_avatar.save(self.avatar.path)
                else:
                    self.avatar = 'avatars/default_avatar.jpg'
