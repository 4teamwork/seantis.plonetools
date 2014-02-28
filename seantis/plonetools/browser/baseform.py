from five import grok

from z3c.form import button
from z3c.form.interfaces import ActionExecutionError
from plone.z3cform.fieldsets.extensible import ExtensibleForm

from zope.interface import Invalid

from plone.directives.form import Form

from seantis.plonetools import _
from seantis.plonetools.browser.shared import (
    TranslateMixin,
    StatusMessageMixin
)


class BaseForm(Form, ExtensibleForm, TranslateMixin, StatusMessageMixin):

    grok.baseclass()

    def update(self):
        self.prepare_actions()
        super(BaseForm, self).update()

    @property
    def available_actions(self):
        yield dict(name='save', title=_(u'Save'), css_class='context')
        yield dict(name='cancel', title=_(u'Cancel'))

    @property
    def success_url(self):
        return self.context.absolute_url()

    @property
    def cancel_url(self):
        return self.context.absolute_url()

    def prepare_actions(self):
        self.buttons = button.Buttons()
        self.handlers = button.Handlers()

        for action in self.available_actions:

            btn = button.Button(title=action['title'], name=action['name'])
            self.buttons += button.Buttons(btn)

            button_handler = button.Handler(btn, self.__class__.handle_action)
            self.handlers.addHandler(btn, button_handler)

    def handle_action(self, action):
        button_handler_id = 'handle_{name}'.format(name=action.__name__)
        button_handler_fn = getattr(self.__class__, button_handler_id)

        assert button_handler_fn, """Button {name} expects a button handler
        funnction named 'handle_{name}', this handler could not be found
        on class {cls}.""".format(name=action.__name__, cls=self.__class__)

        return button_handler_fn(self)

    def handle_save(self):
        data = self.parameters

        if data is None:
            return

        if self.applyChanges(data):
            self.message(_(u'Changes saved'))
        else:
            self.message(_(u'No changes saved'))

        self.request.response.redirect(self.success_url)

    def handle_cancel(self):
        self.request.response.redirect(self.cancel_url)

    @property
    def parameters(self):
        """ Extracts the form data and returns a dictionary or None if
        something went wrong. If something does go wrong, the error message
        is automatically set.

        """
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return None
        else:
            return data

    def raise_action_error(self, msg):
        """ Raise the given message as action execution error, which will
        pop up on top of the form.

        """
        raise ActionExecutionError(Invalid(msg))
