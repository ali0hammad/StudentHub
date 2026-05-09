from django.db import models
from accounts.models import User

class SupportPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="Share your struggles, stress, or seek advice anonymously.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SupportComment(models.Model):
    post = models.ForeignKey(SupportPost, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.post.title}"

class MentorMatching(models.Model):
    ROLES = [
        ('mentor', 'Senior Mentor'),
        ('mentee', 'Junior Mentee'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES)
    department = models.CharField(max_length=100)
    expertise_needs = models.TextField(help_text="What can you teach? OR What do you need help with?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.get_role_display()}"

class SocialWallPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author.email}"
