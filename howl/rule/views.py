from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms

from models import Rule
from howlcore import core

from django.utils.encoding import force_text

import json

class RuleChoiceField(forms.ChoiceField):

    def valid_value(self, value):
        return True

    # def valid_value(self, value):
    #  "Check to see if the provided value is a valid choice"
    #     text_value = force_text(value)
    #     for k, v in self.choices:
    #         if isinstance(v, (list, tuple)):
    #             # This is an optgroup, so look inside the group for options
    #             for k2, v2 in v:
    #                 if value == k2 or text_value == force_text(k2):
    #                     return True
    #         else:
    #             if value == k or text_value == force_text(k):
    #                 return True
    #     return False

class NewRuleForm(forms.Form):
    name = forms.CharField()
    origin_name = RuleChoiceField()
    origin_attribute = RuleChoiceField()
    option = forms.ChoiceField(choices=Rule.OPTION)
    origin_value = forms.CharField(required=False)

    destination_name = RuleChoiceField()
    destination_method = RuleChoiceField()
    destination_value = forms.CharField(required=False)

    def clean_name(self):
        if len(Rule.objects.filter(name=self.cleaned_data["name"])) != 0:
            return False
        return True

    def clean(self):
        # check if origin_name exists, and if in device-list

        # and has the given origin_attribute

        # check if destination_name exists and in device-list

        # and has the given destination_attribute

        pass


def index(request):
    context = {}

    context["rule_list"] = Rule.objects.all();

    context["devicelist"] = []
    attributelist = {}

    for elem in core.get_devices():
        obj = {}
        obj["name"] = elem.__name__
        obj["children"] = elem.objects.all()
        attributelist[elem.__name__] = elem.attributes
        context["devicelist"].append(obj)

    context["attributelist"] = json.dumps(attributelist)

    try:
        if request.include_form:
            context["form"] = NewRuleForm(request.POST)
    except:
        pass

    return render(request, "rule/overview.html", context)


def display(request, rule_name):
    if rule_name == "new":
        return add(request)
    else:
        return HttpResponseRedirect('/rule/')


def add(request):

    if request.method == 'POST':
        form = NewRuleForm(request.POST)

        if form.is_valid():
            print form.cleaned_data["name"]
            print form.cleaned_data["origin_name"]
            print form.cleaned_data["origin_attribute"]
            print form.cleaned_data["option"]
            print form.cleaned_data["origin_value"]

            return HttpResponseRedirect('/rule/')
        else:
            # TODO: a bit hacky
            request.include_form = True
            return index(request)

    else:
        return HttpResponseRedirect('/rule/')


def test(request, rule_name):
    rule = Rule.objects.get(name=rule_name)
    context = core.generate_msg(core.MessageType.INFO, rule.test(), "")

    return render(request, 'misc/message.html', context)


def trigger(request, rule_name):
    rule = Rule.objects.get(name=rule_name)
    print rule.trigger()
    context = core.generate_msg(core.MessageType.INFO, "done", "trigger not implemented")

    return render(request, 'misc/message.html', context)


def request_device_attributes(request, device_name):
    pass