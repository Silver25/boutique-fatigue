# Django widgets deal with rendering of HTML form input elements on the web page and extraction of raw submitted data.
# Django Forms deal with the logic of input validation and are used directly in templates.
# Forms work with widgets, and can be customized with widgets. Widgets provide the actual UI with which form fields take their values.
from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    template_name = 'products/custom_widget_templates/custom_clearable_file_input.html'
