from django import forms
from.models import User
from admin_dash.models import Questions

ANS_CHOICES= [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ]

class RegistrationForm(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'','id':'username','placeholder':'username'}))
    email=forms.CharField(widget=forms.TextInput(attrs={'class':'email','id':'email','placeholder':'email'}))
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'name','id':'name','placeholder':'Full Name'}))
    class Meta:
        model=User
        fields=[
			'username',
            'name',
            'email',
            'subject',

        ]
class LoginForm(forms.Form):
	username=forms.CharField(widget=forms.TextInput(attrs={'class':'','id':'username','placeholder':'username'}))
	email=forms.CharField(widget=forms.TextInput(attrs={'class':'email','id':'email','placeholder':'email'}))

	def clean(self,*args,**kwargs):
		email=self.cleaned_data.get('email')
		username=self.cleaned_data.get('username')
		return super(LoginForm,self).clean(*args,**kwargs)

class ExamChoiceFrm(forms.ModelForm):
    class Meta:
        model=Questions
        fields=[
            'testname',
        ]
class AnsChoice(forms.Form):
    ans= forms.CharField(label='Select a oprion', widget=forms.RadioSelect(choices=ANS_CHOICES))
    def clean(self,*args,**kwargs):
        ans=self.cleaned_data.get('ans')
        return super(AnsChoice,self).clean(*args,**kwargs)