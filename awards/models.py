from django.db import models

from django.contrib.auth.models import User

class Award(models.Model):
    TIER_CHOICES = [('gold', 'gold'), ('silver', 'silver'), ('bronze', 'bronze')]
    tier = models.CharField(choices=TIER_CHOICES, max_length=6)
    purchased_by = models.ForeignKey(User, related_name='purchased_awards', null=True, blank=True, on_delete=models.SET_NULL)
    sent_to = models.ForeignKey(User, related_name='received_awards', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.sent_to:
            return '%s award sent to %s from %s' % (self.tier, self.sent_to, self.purchased_by)
        else:
            return 'Unsent %s award purchased by %s' % (self.tier, self.purchased_by)

    def buy(user, tier):
        Award(purchased_by=user, tier=tier).save()

    def count(user):
        gold = sum(award.tier == 'gold' for award in user.received_awards.all())
        silver = sum(award.tier == 'silver' for award in user.received_awards.all())
        bronze = sum(award.tier == 'bronze' for award in user.received_awards.all())
        return{'gold': gold, 'silver': silver, 'bronze': bronze}
