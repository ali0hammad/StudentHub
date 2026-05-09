from django.contrib import admin
from .models import Confession, Appreciation, Poll, PollOption, PollVote, LeaderboardStat

admin.site.register(Confession)
admin.site.register(Appreciation)
admin.site.register(Poll)
admin.site.register(PollOption)
admin.site.register(PollVote)
admin.site.register(LeaderboardStat)
