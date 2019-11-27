from Exchange.models import DomainOrder


def get_domain_obj(domain_name):
    """
    根据域名字段获取域名表中的对象
    :param domain_name:
    :return:
    """
    domain_objs = DomainOrder.objects.filter(domain_name=domain_name)
    if domain_objs:
        return domain_objs[0]