from django import forms
from .models import *

class Member(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['reg_id','name','tel','des','pay','current_time','start_date','end_date','remain_day']

class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['user_id','name','des','pay','current_time','date']