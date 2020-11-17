from . import models
from django.db.models import Q


def make_payment(group, payment):
    print("========PAYMENTS_RATES========")
    users_positive = _users_with_positive_balance(group)
    print(f"Payment: {payment}")
    for group_user in _distribution_rates(users_positive):
        print(f"User: {group_user[0].user_id}")
        print(f"Rate: {group_user[1]}")
        print(f"amount: {payment.amount}")
        print(f"Given: {payment.amount * group_user[1]}")
        models.PaymentUser(payment_id=payment, user_id=group_user[0].user_id, rate=group_user[1]).save()
        print("----------------------------")
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


# def _distribute_cost_among_users(users, amount, payer):
#     number_of_paying_users = len(users) - 1
#     group_users = list(set(users))
#     for group_user in group_users:
#         if group_user is payer:
#             if len(group_users) > number_of_paying_users:
#                 money = amount
#             else:
#                 money = amount - amount / number_of_paying_users
#             group_user.balance += money
#             group_user.save()
#         else:
#             money = amount / number_of_paying_users
#             group_user.balance -= money
#             group_user.save()


def delete_cost(cost):
    _update_users_group_balances(cost.group_id)
    _update_users_global_balances(cost.group_id)


# def _return_to_payer(payer, amount, number_of_payers=1, involved=False):
#     if payer is not involved:
#         money = amount
#     else:
#         money = amount - (amount / number_of_payers)
#     payer.balance -= money
#     payer.save()


def _update_users_global_balances(group):
    # print("=============================")
    # print("_update_users_global_balances")
    # print("=============================")
    for group_user in models.GroupUser.objects.filter(group_id=group):
        user_groups = models.GroupUser.objects.filter(user_id=group_user.user_id)
        global_user_balance = 0
        for user_group in user_groups:
            global_user_balance += user_group.balance
        group_user.user_id.balance = global_user_balance
        group_user.user_id.save()


def _update_users_group_balances(group):
    print("============================")
    print("_update_users_group_balances")
    print("============================")
    group_users = models.GroupUser.objects.filter(group_id=group)

    for group_user in group_users:
        print("========USER========")
        print(group_user.user_id)
        group_user_balance = 0

        print("========PAYMENT========")
        for payment in models.Payment.objects.filter(user_id=group_user.user_id, group_id=group):
            group_user_balance += payment.amount
            print(payment)

        print("========COST_USER========")
        for user_cost in models.CostUser.objects.filter(user_id=group_user.user_id):
            if not user_cost.cost_id.group_id == group:
                continue
            group_user_balance -= user_cost.cost_id.amount / _number_of_users_involved_in_cost(user_cost.cost_id)
            print(user_cost, _number_of_users_involved_in_cost(user_cost.cost_id))

        print("========COST========")
        for cost in models.Cost.objects.filter(payer_id=group_user.user_id, group_id=group):
            group_user_balance += cost.amount
            print(cost)

        for user_payment in models.PaymentUser.objects.filter(user_id=group_user.user_id):
            if not user_payment.payment_id.group_id == group:
                continue
            group_user_balance -= user_payment.payment_id.amount * user_payment.rate
            print("\n\n")
            print(f"Given to the user: {user_payment.payment_id.amount * user_payment.rate}")
            print("\n\n")

        print("========BALANCE========")
        print(group_user_balance)
        print("=======================")
        group_user.balance = group_user_balance
        group_user.save()


def _number_of_users_involved_in_cost(cost):
    return len(models.CostUser.objects.filter(cost_id=cost))
