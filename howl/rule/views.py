from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.core.exceptions import ValidationError

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

    def _check_for_existence(self, device_class_name, instance_name):

        origin_instance = None

        device_list = core.get_devices()
        success = False
        for elem in device_list:
            if device_class_name.lower() == elem.__name__.lower():
                for inst in elem.objects.all():
                    if instance_name == inst.name:
                        success = True
                        origin_instance = inst
                        break

                if not success:
                    raise ValidationError(
                        'Invalid value: %(value)s',
                        code='invalid',
                        params={'value': instance_name},
                    )

        if not success:
            raise ValidationError(
                'Invalid value: %(value)s',
                code='invalid',
                params={'value': device_class_name},
            )

        return origin_instance

    def clean(self):
        # check if origin_name exists, and if in device-list

        data_origin_name = self.cleaned_data["origin_name"]
        device_class_name = data_origin_name[0:data_origin_name.find('.')]
        instance_name = data_origin_name[data_origin_name.find('.')+1:]

        origin_instance = self._check_for_existence(device_class_name, instance_name)
        
        # and has the given origin_attribute

        if not hasattr(origin_instance, self.cleaned_data["origin_attribute"]):
            raise ValidationError(
                'Invalid value: %(value)s',
                code='invalid',
                params={'value': self.cleaned_data["origin_attribute"]},
            )

        # check if destination_name exists and in device-list

        data_destination_name = self.cleaned_data["destination_name"]
        device_class_name = data_destination_name[0:data_destination_name.find('.')]
        instance_name = data_destination_name[data_destination_name.find('.')+1:]

        destination_instance = self._check_for_existence(device_class_name, instance_name)

        # and has the given destination_method

        # TODO: check if callable

        if not hasattr(destination_instance, self.cleaned_data["destination_method"]):
            raise ValidationError(
                'Invalid value: %(value)s',
                code='invalid',
                params={'value': self.cleaned_data["destination_method"]},
            )


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
            # print form.cleaned_data["name"]
            # print form.cleaned_data["origin_name"]
            # print form.cleaned_data["origin_attribute"]
            # print form.cleaned_data["option"]
            # print form.cleaned_data["origin_value"]

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