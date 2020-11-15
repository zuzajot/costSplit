from . import models


def make_payment(group, amount, paying_user_group):
    for group_user in _distribution_rates(group):
        group_user[0].balance = group_user[0].balance - (amount * group_user[1])
        group_user[0].save()
    paying_user_group.balance += amount
    paying_user_group.save()
    _update_users_global_balances(group)


def _distribution_rates(group):
    users = _users_with_positive_balance(group)
    sum_of_money = _sum_of_money_owned(group)
    rates = []
    for user in users:
        rates.append((user, (-user.balance) / sum_of_money))
    return rates


def _sum_of_money_owned(group):
    sum_of_money = 0
    for group_user in _users_with_positive_balance(group):
        sum_of_money += (-group_user.balance)
    return sum_of_money


def _users_with_positive_balance(group):
    return models.GroupUser.objects.filter(group_id=group, balance__gt=0)


def create_cost(cost, id_of_users_involved, group):
    users_involved = [models.GroupUser.objects.get(user_id=cost.payer_id, group_id=group)]
    for user_id in id_of_users_involved:
        user = models.Profile.objects.get(id=user_id)
        models.CostUser(user_id=user, cost_id=cost).save()
        users_involved.append(models.GroupUser.objects.get(user_id=user, group_id=group))
    _distribute_cost_among_users(users_involved, cost.amount, users_involved[0])
    _update_users_global_balances(group)


def _distribute_cost_among_users(users, amount, payer):
    number_of_paying_users = len(users) - 1
    group_users = list(set(users))
    for group_user in group_users:
        if group_user is payer:
            if len(group_users) > number_of_paying_users:
                money = amount
            else:
                money = amount - amount / number_of_paying_users
            group_user.balance += money
            group_user.save()
        else:
            money = amount / number_of_paying_users
            group_user.balance -= money
            group_user.save()


def delete_cost(cost_users):
    pass


def _update_users_global_balances(group):
    for group_user in models.GroupUser.objects.filter(group_id=group):
        user_groups = models.GroupUser.objects.filter(user_id=group_user.user_id)
        global_user_balance = 0
        for user_group in user_groups:
            global_user_balance += user_group.balance
        group_user.user_id.balance = global_user_balance
        # print(f"group_user: {group_user}")
        # print(f"Profil: {group_user.user_id}, Bilans: {group_user.user_id.balance}")
        group_user.save()
