from django.db import models

from django.contrib.auth.models import User

class Award(models.Model):
    TIER_CHOICES = [('gold', 'gold'), ('silver', 'silver'), ('bronze', 'bronze')]
    tier = models.CharField(choices=TIER_CHOICES, max_length=6)
    purchased_by = models.ForeignKey(User, related_name='purchased_awards', null=True, blank=True, on_delete=models.SET_NULL)
    purchased_by_username = models.CharField(max_length=20)
    sent_to = models.ForeignKey(User, related_name='received_awards', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.purchased_by_username = User.objects.get(id=self.purchased_by.id).username
        super(Award, self).save(*args, **kwargs)

    def __str__(self):
        if self.sent_to:
            return '%s award sent to %s from %s with id %s' % (self.tier, self.sent_to, self.purchased_by, self.pk)
        else:
            return 'Unsent %s award purchased by %s with id %s' % (self.tier, self.purchased_by, self.pk)

    def received_awards_count(user):
        awards = user.received_awards.all()
        total = len(awards)
        gold = sum(award.tier == 'gold' for award in awards)
        silver = sum(award.tier == 'silver' for award in awards)
        bronze = sum(award.tier == 'bronze' for award in awards)
        return{'total': total, 'gold': gold, 'silver': silver, 'bronze': bronze}

    def sent_awards_count(user):
        awards = user.purchased_awards.all()
        total = sum(award.sent_to != None for award in awards)
        gold = sum(award.tier == 'gold' and award.sent_to != None for award in awards)
        silver = sum(award.tier == 'silver' and award.sent_to != None for award in awards)
        bronze = sum(award.tier == 'bronze' and award.sent_to != None for award in awards)
        return{'total': total, 'gold': gold, 'silver': silver, 'bronze': bronze}

    def unsent_awards_count(user):
        awards = user.purchased_awards.all()
        total = sum(award.sent_to == None for award in awards)
        gold = sum(award.tier == 'gold' and award.sent_to == None for award in awards)
        silver = sum(award.tier == 'silver' and award.sent_to == None for award in awards)
        bronze = sum(award.tier == 'bronze' and award.sent_to == None for award in awards)
        return{'total': total, 'gold': gold, 'silver': silver, 'bronze': bronze}

    def send_form_choices(user):
        unsent_awards = Award.unsent_awards_count(user)
        tier_choices = []
        if unsent_awards['gold']:
            tier_choices.append(('gold', 'Gold'))
        if unsent_awards['silver']:
            tier_choices.append(('silver', 'Silver'))
        if unsent_awards['bronze']:
            tier_choices.append(('bronze', 'Bronze'))
        return tier_choices