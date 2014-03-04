from plone.app.content.interfaces import INameFromTitle
from zope.interface import implements, Interface
from zope.component import adapts


class ICustomTitle(Interface):
    pass


class CustomTitle(object):
    """ Uses the fields defined as title by seantis.people.supermodel to
    generate a title for a new object.

    """
    implements(INameFromTitle)
    adapts(ICustomTitle)

    def __init__(self, context):
        pass

    def __new__(cls, context):
        title = context.get_custom_title()
        instance = super(CustomTitle, cls).__new__(cls)

        instance.title = title
        context.setTitle(title)

        return instance


def on_object_modified(obj, event=None):
    obj.setTitle(obj.get_custom_title())
