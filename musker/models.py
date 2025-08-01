from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone

# Create Meep model
from django.db import models
from django.contrib.auth.models import User

# Community model with ManyToMany for members
class Community(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_communities")
    members = models.ManyToManyField(User, related_name="joined_communities", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Meep model for posts
class Meep(models.Model):
    user = models.ForeignKey(User, related_name="meeps", on_delete=models.CASCADE)  # Link meep to user
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="meep_likes", blank=True)
    file = models.FileField(upload_to='meeps_files/', null=True, blank=True)  # Optional file upload
    community = models.ForeignKey(Community, related_name="meeps", on_delete=models.CASCADE, null=True)  # Temporarily nullable

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user.username} ({self.created_at:%Y-%m-%d %H:%M}): {self.body}"

class Comment(models.Model):
    meep = models.ForeignKey(Meep, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.meep.body[:30]}"

# Create A User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", 
        related_name="followed_by",
        symmetrical=False,
        blank=True)    
    date_modified = models.DateTimeField(auto_now=True)  # Fixed auto_now=True
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    
    profile_bio = models.CharField(null=True, blank=True, max_length=500)
    homepage_link = models.CharField(null=True, blank=True, max_length=100)
    facebook_link = models.CharField(null=True, blank=True, max_length=100)
    instagram_link = models.CharField(null=True, blank=True, max_length=100) 
    linkedin_link = models.CharField(null=True, blank=True, max_length=100)
    
    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    if created:
        # Create the profile for the user
        user_profile = Profile(user=instance)
        user_profile.save()
        # Have the user follow themselves
        user_profile.follows.set([instance])  # Set the user to follow themselves
        user_profile.save()

# Connect the signal to the User model
post_save.connect(create_profile, sender=User)

class Notification(models.Model):
    NOTIFY_LIKE = 'like'
    NOTIFY_COMMENT = 'comment'
    NOTIFY_FOLLOW = 'follow'

    NOTIFICATION_TYPES = [
        (NOTIFY_LIKE, 'Like'),
        (NOTIFY_COMMENT, 'Comment'),
        (NOTIFY_FOLLOW, 'Follow'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    meep = models.ForeignKey(Meep, on_delete=models.CASCADE, null=True, blank=True)  # Optional, only for post-related notifications
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Add this field to track read status

    def __str__(self):
        return f"Notification for {self.user.username} - {self.notification_type}"

    class Meta:
        ordering = ['-created_at']

