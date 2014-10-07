from django.shortcuts import render

from models import Rule
from howlcore import core


def index(request):
    context = {}

    context["rule_list"] = Rule.objects.all();

    return render(request, "rule/overview.html", context)


def display(request):
    pass


def add(request):

    # check if origin is valid device instance
    for base in self.__class__.__bases__:
        print base.__name__


def test(request, rule_name):
    rule = Rule.objects.get(name=rule_name)
    context = core.generate_msg(core.MessageType.INFO, rule.test(), "")

    return render(request, 'misc/message.html', context)


def trigger(request, rule_name):
    rule = Rule.objects.get(name=rule_name)
    print rule.trigger()
    context = core.generate_msg(core.MessageType.INFO, "done", "trigger not implemented")

    return render(request, 'misc/message.html', context)