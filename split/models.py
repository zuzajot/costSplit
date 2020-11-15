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
    group_currency = models.CharField(max_length=3, choices=[('AON','AON'), ('ARS', 'ARS'), ('AUD', 'AUD'), ('AWG', 'AWG'), ('AZM', 'AZM'), ('BAM','BAM'), ('BBD', 'BBD'), ('BDT', 'BDT'), ('BGN', 'BGN'), ('BHD', 'BHD'), ('BIF', 'BIF'), ('BND', 'BND'), ('BOB', 'BOB'), ('BRL', 'BRL'), ('BSD', 'BSD'), ('BTN', 'BTN'), ('BWP', 'BWP'), ('BYN', 'BYN'), ('BZD', 'BZD'), ('CAD', 'CAD'), ('CDF','CDF'), ('CHF', 'CHF'), ('CLP', 'CLP'), ('CNY', 'CNY'), ('COP', 'COP'), ('CRC', 'CRC'), ('CUP', 'CUP'), ('CVE', 'CVE'), ('CZK', 'CZK'), ('DJF', 'DJF'), ('DKK', 'DKK'), ('DOP', 'DOP'), ('DZD', 'DZD'), ('EEK', 'EEK'), ('EGP', 'EGP'), ('ERN', 'ERN'), ('ETB', 'ETB'), ('EUR', 'EUR'), ('FJD', 'FJD'), ('GBP', 'GBP'), ('GEL', 'GEL'), ('GHC', 'GHC'), ('GIP', 'GIP'), ('GMD', 'GMD'), ('GNF', 'GNF'), ('GTQ', 'GTQ'), ('GYD', 'GYD'), ('HKD', 'HKD'), ('HNL', 'HNL'), ('HRK', 'HRK'), ('HTG', 'HTG'), ('HUF', 'HUF'), ('IDR', 'IDR'), ('ILS', 'ILS'), ('INR', 'INR'), ('IQD', 'IQD'), ('IRR', 'IRR'), ('ISK', 'ISK'), ('JMD', 'JMD'), ('JOD', 'JOD'), ('JPY', 'JPY'), ('KES', 'KES'), ('KGS', 'KGS'), ('KHR', 'KHR'), ('KMF', 'KMF'), ('KRW', 'KRW'), ('KWD', 'KWD'), ('KZT', 'KZT'), ('LAK', 'LAK'), ('LBP', 'LBP'), ('LKR', 'LKR'), ('LRD', 'LRD'), ('LSL', 'LSL'), ('LTL', 'LTL'), ('LVL', 'LVL'), ('LYD', 'LYD'), ('MAD', 'MAD'), ('MDL', 'MDL'), ('MGA', 'MGA'), ('MKD', 'MKD'), ('MMK', 'MMK'), ('MNT', 'MNT'), ('MOP', 'MOP'), ('MRO', 'MRO'), ('MUR', 'MUR'), ('MVR', 'MVR'), ('MWK', 'MWK'), ('MXN', 'MXN'), ('MYR', 'MYR'), ('MZM', 'MZM'), ('NAD', 'NAD'), ('NGN', 'NGN'), ('NIO', 'NIO'), ('NOK', 'NOK'), ('NPR', 'NPR'), ('NZD', 'NZD'), ('OMR', 'OMR'), ('PAB', 'PAB'), ('PEN', 'PEN'), ('PGK', 'PGK'), ('PHP', 'PHP'), ('PKR', 'PKR'), ('PLN', 'PLN'), ('PYG', 'PYG'), ('QAR', 'QAR'), ('RON', 'RON'), ('RSD', 'RSD'), ('RUB', 'RUB'), ('RWF', 'RWF'), ('SAR', 'SAR'), ('SBD', 'SBD'), ('SCP', 'SCP'), ('SCR', 'SCR'), ('SDD', 'SDD'), ('SEK', 'SEK'), ('SGD', 'SGD'), ('SLL','SLL'), ('SOS', 'SOS'), ('SRG', 'SRG'), ('STD', 'STD'), ('SVC', 'SVC'), ('SYP', 'SYP'), ('SZL', 'SZL'), ('THB', 'THB'), ('TJS', 'TJS'), ('TMM', 'TMM'), ('TND', 'TND'), ('TOP', 'TOP'), ('TRY', 'TRY'), ('TTD', 'TTD'), ('TWD', 'TWD'), ('TZS', 'TZS'), ('UAH', 'UAH'), ('UGX', 'UGX'), ('USD', 'USD'), ('UYU', 'UYU'), ('UZS', 'UZS'), ('VEB', 'VEB'), ('VND', 'VND'), ('VUV', 'VUV'), ('WN', 'WN'), ('WST', 'WST'), ('XAF', 'XAF'), ('XCD', 'XCD'), ('XOF', 'XOF'), ('XPF', 'XPF'), ('YER', 'YER'), ('ZAR', 'ZAR'), ('ZMK', 'ZMK'), ('ZWD', 'ZWD')])

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
    date = models.DateField(default=timezone.now)
    currency = models.CharField(max_length=3, choices=[('AON','AON'), ('ARS', 'ARS'), ('AUD', 'AUD'), ('AWG', 'AWG'), ('AZM', 'AZM'), ('BAM','BAM'), ('BBD', 'BBD'), ('BDT', 'BDT'), ('BGN', 'BGN'), ('BHD', 'BHD'), ('BIF', 'BIF'), ('BND', 'BND'), ('BOB', 'BOB'), ('BRL', 'BRL'), ('BSD', 'BSD'), ('BTN', 'BTN'), ('BWP', 'BWP'), ('BYN', 'BYN'), ('BZD', 'BZD'), ('CAD', 'CAD'), ('CDF','CDF'), ('CHF', 'CHF'), ('CLP', 'CLP'), ('CNY', 'CNY'), ('COP', 'COP'), ('CRC', 'CRC'), ('CUP', 'CUP'), ('CVE', 'CVE'), ('CZK', 'CZK'), ('DJF', 'DJF'), ('DKK', 'DKK'), ('DOP', 'DOP'), ('DZD', 'DZD'), ('EEK', 'EEK'), ('EGP', 'EGP'), ('ERN', 'ERN'), ('ETB', 'ETB'), ('EUR', 'EUR'), ('FJD', 'FJD'), ('GBP', 'GBP'), ('GEL', 'GEL'), ('GHC', 'GHC'), ('GIP', 'GIP'), ('GMD', 'GMD'), ('GNF', 'GNF'), ('GTQ', 'GTQ'), ('GYD', 'GYD'), ('HKD', 'HKD'), ('HNL', 'HNL'), ('HRK', 'HRK'), ('HTG', 'HTG'), ('HUF', 'HUF'), ('IDR', 'IDR'), ('ILS', 'ILS'), ('INR', 'INR'), ('IQD', 'IQD'), ('IRR', 'IRR'), ('ISK', 'ISK'), ('JMD', 'JMD'), ('JOD', 'JOD'), ('JPY', 'JPY'), ('KES', 'KES'), ('KGS', 'KGS'), ('KHR', 'KHR'), ('KMF', 'KMF'), ('KRW', 'KRW'), ('KWD', 'KWD'), ('KZT', 'KZT'), ('LAK', 'LAK'), ('LBP', 'LBP'), ('LKR', 'LKR'), ('LRD', 'LRD'), ('LSL', 'LSL'), ('LTL', 'LTL'), ('LVL', 'LVL'), ('LYD', 'LYD'), ('MAD', 'MAD'), ('MDL', 'MDL'), ('MGA', 'MGA'), ('MKD', 'MKD'), ('MMK', 'MMK'), ('MNT', 'MNT'), ('MOP', 'MOP'), ('MRO', 'MRO'), ('MUR', 'MUR'), ('MVR', 'MVR'), ('MWK', 'MWK'), ('MXN', 'MXN'), ('MYR', 'MYR'), ('MZM', 'MZM'), ('NAD', 'NAD'), ('NGN', 'NGN'), ('NIO', 'NIO'), ('NOK', 'NOK'), ('NPR', 'NPR'), ('NZD', 'NZD'), ('OMR', 'OMR'), ('PAB', 'PAB'), ('PEN', 'PEN'), ('PGK', 'PGK'), ('PHP', 'PHP'), ('PKR', 'PKR'), ('PLN', 'PLN'), ('PYG', 'PYG'), ('QAR', 'QAR'), ('RON', 'RON'), ('RSD', 'RSD'), ('RUB', 'RUB'), ('RWF', 'RWF'), ('SAR', 'SAR'), ('SBD', 'SBD'), ('SCP', 'SCP'), ('SCR', 'SCR'), ('SDD', 'SDD'), ('SEK', 'SEK'), ('SGD', 'SGD'), ('SLL','SLL'), ('SOS', 'SOS'), ('SRG', 'SRG'), ('STD', 'STD'), ('SVC', 'SVC'), ('SYP', 'SYP'), ('SZL', 'SZL'), ('THB', 'THB'), ('TJS', 'TJS'), ('TMM', 'TMM'), ('TND', 'TND'), ('TOP', 'TOP'), ('TRY', 'TRY'), ('TTD', 'TTD'), ('TWD', 'TWD'), ('TZS', 'TZS'), ('UAH', 'UAH'), ('UGX', 'UGX'), ('USD', 'USD'), ('UYU', 'UYU'), ('UZS', 'UZS'), ('VEB', 'VEB'), ('VND', 'VND'), ('VUV', 'VUV'), ('WN', 'WN'), ('WST', 'WST'), ('XAF', 'XAF'), ('XCD', 'XCD'), ('XOF', 'XOF'), ('XPF', 'XPF'), ('YER', 'YER'), ('ZAR', 'ZAR'), ('ZMK', 'ZMK'), ('ZWD', 'ZWD')])

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
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user_id} - {self.group_id} - {self.amount}"


