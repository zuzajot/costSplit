from . import models
from django.db.models import Q


def make_payment(group, payment):
    users_positive = _users_with_positive_balance(group)
    for group_user in _distribution_rates(users_positive):
        models.PaymentUser(payment_id=payment, user_id=group_user[0].user_id, rate=group_user[1]).save()
    _update_users_group_balances(group)
    _update_users_global_balances(group)


def _distribution_rates(users_positive):
    sum_of_money = _sum_of_money_owned(users_positive)
    rates = []
    for user in users_positive:
        rates.append((user, user.balance/sum_of_money))
    return rates


def _sum_of_money_owned(users_positive):
    sum_of_money = 0
    for group_user in users_positive:
        sum_of_money += group_user.balance
    return sum_of_money


def _users_with_positive_balance(group):
    return models.GroupUser.objects.filter(group_id=group, balance__gt=0)


def create_cost(cost, id_of_users_involved, group):
    for user_id in id_of_users_involved:
        user = models.Profile.objects.get(id=user_id)
        models.CostUser(user_id=user, cost_id=cost).save()
    _update_users_group_balances(group)
    _update_users_global_balances(group)


def delete_cost(cost):
    _update_users_group_balances(cost.group_id)
    _update_users_global_balances(cost.group_id)


def _update_users_global_balances(group):
    for group_user in models.GroupUser.objects.filter(group_id=group):
        user_groups = models.GroupUser.objects.filter(user_id=group_user.user_id)
        global_user_balance = 0
        for user_group in user_groups:
            global_user_balance += user_group.balance
        group_user.user_id.balance = global_user_balance
        group_user.user_id.save()


def _update_users_group_balances(group):

    group_users = models.GroupUser.objects.filter(group_id=group)

    for group_user in group_users:
        group_user_balance = 0

        for payment in models.Payment.objects.filter(user_id=group_user.user_id, group_id=group):
            group_user_balance += payment.amount
            print(payment)

        for user_cost in models.CostUser.objects.filter(user_id=group_user.user_id):
            if not user_cost.cost_id.group_id == group:
                continue
            group_user_balance -= user_cost.cost_id.amount / _number_of_users_involved_in_cost(user_cost.cost_id)

        for cost in models.Cost.objects.filter(payer_id=group_user.user_id, group_id=group):
            group_user_balance += cost.amount

        for user_payment in models.PaymentUser.objects.filter(user_id=group_user.user_id):
            if not user_payment.payment_id.group_id == group:
                continue
            group_user_balance -= user_payment.payment_id.amount * user_payment.rate

        print(group_user_balance)
        group_user.balance = group_user_balance
        group_user.save()


def _number_of_users_involved_in_cost(cost):
    return len(models.CostUser.objects.filter(cost_id=cost))
