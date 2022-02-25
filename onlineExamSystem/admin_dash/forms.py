from django import forms
from.models import Questions
class AddQFrm(forms.ModelForm):
    class Meta:
        model=Questions
        fields=[
            'qs_no',
           'subject',
            'testname',
            'questions',
            'answers',
            'option_a',
            'option_b',
            'option_c',
            'option_d',

        ]
