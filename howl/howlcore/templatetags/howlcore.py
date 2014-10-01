from django import template
from django.utils.safestring import mark_safe

from .. import core

register = template.Library()

@register.simple_tag
def statustype(format_string):

    print format_string

    BADGE = {core.StatusType.UNDEFINED      : "default",
             core.StatusType.OK             : "success",
             core.StatusType.NOT_RESPONDING : "danger",
             core.StatusType.ERROR          : "danger",
             }

    GLYPHICON = {core.StatusType.UNDEFINED      : "asterisk",
                 core.StatusType.OK             : "ok",
                 core.StatusType.NOT_RESPONDING : "remove",
                 core.StatusType.ERROR          : "remove",
                 }

    s = """ <span class="badge badge-{0}">
                <span rel="tooltip" title="{1}">
                    <span class="glyphicon glyphicon-{2}"></span>
                </span>
            </span>
        """

    if format_string == core.StatusType.UNDEFINED:
        s = s.format(BADGE[core.StatusType.UNDEFINED], core.Device.STATUS_TYPE[core.StatusType.UNDEFINED][1], GLYPHICON[core.StatusType.UNDEFINED])
    elif format_string == core.StatusType.OK:
        s = s.format(BADGE[core.StatusType.OK], core.Device.STATUS_TYPE[core.StatusType.OK][1], GLYPHICON[core.StatusType.OK])
    elif format_string == core.StatusType.NOT_RESPONDING:
        s = s.format(BADGE[core.StatusType.NOT_RESPONDING], core.Device.STATUS_TYPE[core.StatusType.NOT_RESPONDING][1], GLYPHICON[core.StatusType.NOT_RESPONDING])
    elif format_string == core.StatusType.ERROR:
        s = s.format(BADGE[core.StatusType.ERROR], core.Device.STATUS_TYPE[core.StatusType.ERROR][1], GLYPHICON[core.StatusType.ERROR])

    return s
