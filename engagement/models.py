from django.db import models
from accounts.models import User

class Confession(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True) # For moderation if needed

    def __str__(self):
        return f"Confession {self.id}"

class Appreciation(models.Model):
    recipient_name = models.CharField(max_length=100) # Can be a string, since it's anonymous/open
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appreciation for {self.recipient_name}"

class Poll(models.Model):
    question = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text

class PollVote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('poll', 'user') # One vote per user per poll

    def __str__(self):
        return f"{self.user.email} voted for {self.option.text}"

class LeaderboardStat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')
    points = models.IntegerField(default=0)
    help_provided = models.IntegerField(default=0)
    resources_shared = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.email} Stats"
