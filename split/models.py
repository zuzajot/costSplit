from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()


class Group(models.Model):
    name = models.CharField(max_length=100)
    invite_url = models.CharField(max_length=200, unique=True)
    admin_id = models.ForeignKey("Profile", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class GroupUser(models.Model):
    group_id = models.ForeignKey("Group", on_delete=models.CASCADE)
    user_id = models.ForeignKey("Profile", on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.group_id} - {self.user_id} - {self.balance}"


class Cost(models.Model):
    title = models.CharField(max_length=100)
    amount = models.FloatField()
    payer_id = models.ForeignKey("Profile", on_delete=models.DO_NOTHING)
    group_id = models.ForeignKey("Group", on_delete=models.CASCADE)
    users = models.ManyToManyField("Profile", related_name="cost_users_many_to_many")

    def __str__(self):
        return f"{self.title} - {self.amount} - {self.payer_id} - {self.group_id}"


class CostUser(models.Model):
    cost_id = models.ForeignKey("Cost", on_delete=models.CASCADE)
    user_id = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id} - {self.cost_id}"


class Payment(models.Model):
    amount = models.FloatField()
    group_id = models.ForeignKey("Group", on_delete=models.CASCADE)
    user_id = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id} - {self.group_id} - {self.amount}"


