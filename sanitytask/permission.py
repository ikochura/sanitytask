from datetime import datetime, timedelta, date

from .models import Shift, Check, CheckGroup, Client


def get_user_permission_object(user):
    # handler = {'all_companies': AnyCompanyPermission,
    #            'current_companies': MyCompanyPermission
    #            }
    # tmp = {}
    # perm_dict = {u'all_companies': 2,
    #              u'current_companies': 1
    #              }
    # for perm in Permission.objects.filter(user=user).values_list():
    #     tmp[perm[1]] = perm_dict[perm[1]]
    # v = list(tmp.values())
    # k = list(tmp.keys())
    # if tmp:
    #     return handler[k[v.index(max(v))]]
    # else:
    #     return MyCompanyPermission
    handler = {'Admin': AnyCompanyPermission,
               'Staff': AnyCompanyPermission,
               'Users': MyCompanyPermission}
    groups = user.groups.all()
    if groups:
        return handler[groups[0].name]
    return handler['Users']


class Perm:

    def __init__(self):
        pass

    @staticmethod
    def _select_shift():
        return Shift.objects.all()

    @staticmethod
    def get_empty_shift():
        return None

    @staticmethod
    def get_done_check(comp):
        return {}

    @staticmethod
    def get_alarm_check(year, month, day, user):
        if Check.objects.filter(user=user,
                                date=date(int(year), int(month), int(day))) and Check.objects.filter(
            result=False):
            return True
        else:
            return False


class AnyCompanyPermission(Perm):
    @staticmethod
    def has_perm():
        return True

    @staticmethod
    def get_check(user, date=datetime.today()):
        return Check.objects.filter(date=date, result=0).order_by('check_task__check_group__client',
                                                                  'check_task__check_group')

    @staticmethod
    def get_shift_checkgroup(user, client):
        return CheckGroup.objects.filter(checktask__check__date=datetime.today())

    @staticmethod
    def get_shift(user):
        return Perm._select_shift()

    @staticmethod
    def get_shift_comp(user, client):
        return Shift.objects.filter(checkgroup__client=client)

    @staticmethod
    def get_task_count(user):
        return Check.objects.filter(date=datetime.today(),
                                    result=0).count()

    @staticmethod
    def get_empty_shift():
        comp_dict = {}
        for comp in Client.objects.all():
            cg_dict = {}
            for cg in CheckGroup.objects.filter(client__name=comp.name):
                shift_list = [False, False, False, False, False, False, False]
                for sh in Shift.objects.filter(checkgroup__name=cg.name):
                    for idx, el in enumerate([sh.mon, sh.tue, sh.wed, sh.thu, sh.fri, sh.sat, sh.sun], 0):
                        if el:
                            shift_list[idx] = sh.user.username
                cg_dict[cg.name] = shift_list
            comp_dict[comp.name] = cg_dict
        return comp_dict

    @staticmethod
    def get_done_check(comp):
        check_dict = {}
        if comp == 'all':
            for cp in Client.objects.all():
                check_dict[cp.name] = Check.objects.filter(check_task__check_group__client=cp.name)
        else:
            check_dict[comp] = Check.objects.filter(check_task__check_group__client=comp)
        return check_dict

    @staticmethod
    def get_alarm(user):
        if Check.objects.filter(date=date.today() - timedelta(1)).count() or Check.objects.filter(
                date=date.today(), result=False, hidden_result=True).count():
            return True

    @staticmethod
    def get_alarm_check(year, month, day, user):
        if Check.objects.filter(date=date(int(year), int(month), int(day)),
                                result=False) or Check.objects.filter(
            date=date(int(year), int(month), int(day)), hidden_result=False):
            return True
        else:
            return False

    @staticmethod
    def get_date_check(user, year, month, day):
        return Check.objects.filter(date=datetime(int(year), int(month), int(day)))


class MyCompanyPermission(Perm):
    @staticmethod
    def has_perm():
        return False

    @staticmethod
    def get_check(user, date=datetime.today()):
        return Check.objects.filter(user=user, date=datetime.today(), result=0).order_by(
            'check_task__check_group__client',
            'check_task__check_group')

    @staticmethod
    def get_shift_checkgroup(user):
        return CheckGroup.objects.filter(checktask__check__date=datetime.today(),
                                         checktask__check__user=user)

    @staticmethod
    def get_shift_comp(user, client):
        return Shift.objects.filter(user=user, checkgroup__client=client)

    @staticmethod
    def get_shift(user):
        return Perm._select_shift().filter(user=user)

    @staticmethod
    def get_task_count(user):
        return Check.objects.filter(user=user,
                                    result=0,
                                    date=datetime.today()).count()

    @staticmethod
    def get_alarm_check(year, month, day, user):
        if Check.objects.filter(user=user,
                                date=date(year, month, day)) and Check.objects.filter(result=False):
            return True
        else:
            return False

    @staticmethod
    def get_alarm(user):
        if Check.objects.filter(user=user,
                                date=date.today() - timedelta(1)).count():
            return True

    @staticmethod
    def get_date_check(user, year, month, day):
        return Check.objects.filter(user=user,
                                    date=date(int(year), int(month), int(day)))
