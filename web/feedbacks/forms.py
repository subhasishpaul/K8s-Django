from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError
from feedbacks.models import Mobile, Circle, Ssa

# from django.forms import ModelChoiceField

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    last_name = forms.CharField()
    first_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'last_name', 'first_name']


choice = (
    ('not_answered', 'Not Answered'),
    ('poor_network_coverage', 'Poor network coverage'),    
    ('low_data_speed', 'Low data speed'),
    ('absence_of_4g', 'Absence of 4G'),
    ('poor_customer_care', 'Poor customer care'),
    ('recharge_issues', 'Recharge issues'),
    ('billing_issues', 'Billing issues'),
    ('high_tariff', 'High Tariff'),
    ('vas', 'Value Added Services'),
    ('others', 'Others'),
)


CIRCLE_CHOICES =( 
    ("0", "BSNL - Circle-wise"), 
    ("1", "BSNL - Andaman"), 
    ("2", "BSNL - Assam"),
    ("3", "BSNL - Bihar"), 
    ("4", "BSNL - Jharkhand"), 
    ("5", "BSNL - Kolkata"),
    ("6", "BSNL - North East-I"), 
    ("7", "BSNL - North East-II"), 
    ("8", "BSNL - Orissa"), 
    ("9", "BSNL - West Bengal")
) 

FEEDBACK_STATUS= [
    ('Completed', 'Completed'),
    ('Pending', 'Pending'),
]

REPORT_TYPE= [
    ('Report', 'Report'),
    ('Chart', 'Chart'),
]

PO_REASON = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]

FEEDBACK_STS = [
    ('feed_pend', 'Pending'),
    ('feed_comp', 'Completed'),
]

PORT_STS = [
    ('port_pend', 'UPC / PORT Applied'),
    ('port_comp', 'Completed'),
    ('all', 'All')
]

# creating a form  
class SearchForm(forms.Form): 
    circle_id = forms.ChoiceField(choices = CIRCLE_CHOICES) 
    feed_status = forms.CharField(widget=forms.RadioSelect(choices=FEEDBACK_STATUS))
    # feed_pend = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=FEEDBACK_PENDING)
    # feed_comp = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=FEEDBACK_COMPLETED)
    feed_sts = forms.CharField(widget=forms.RadioSelect(choices=FEEDBACK_STS))
    port_sts = forms.CharField(widget=forms.RadioSelect(choices=PORT_STS))
    report_type = forms.CharField(widget=forms.RadioSelect(choices=REPORT_TYPE))
    po_reason = forms.CharField(widget=forms.RadioSelect(choices=PO_REASON))
    # port_pend = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=PORT_PENDING)
    # port_comp = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=PORT_COMPLETED)


class FeedbackModelForm(forms.Form):
    
    remarks = forms.CharField(widget=forms.Textarea)
    # reason_for_PO = forms.CharField(label='Reason', widget=forms.RadioSelect(choices=choice))
    reason_for_PO = forms.ChoiceField(required=True, choices=choice)

    def clean_remarks(self):
        data = self.cleaned_data['remarks']
        
        if len(data) > 3:
            return data 
        else:
            raise forms.ValidationError("This is not long enough")

# class FeedbackModelForm(forms.ModelForm):
#     class Meta:
#         model = Mobile
#         fields = ['msisdn', 'address', 'remarks', 'reason_for_PO']

#         widgets = {
#             'msisdn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MSISDN'}),
#             'address': forms.TextInput(attrs={'class': 'form-control'}),
#             'reason_for_PO': forms.Select(attrs={'class': 'form-control'}),
#             'remarks': forms.Textarea(attrs={'class': 'form-control'}),
#         }
    


class QueryForm(forms.Form):

    upc_date = forms.DateField(
        label='',
        required=False,
        # initial = datetime.datetime.now(),
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'id':'datepicker1',
                'placeholder':'upc_date'
            }))

    keywords = forms.CharField(
        required=False,
        label='TT',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'msisdn'
            }))


# Testing dependent Drop down option

class SsaForm(forms.ModelForm):
    class Meta:
        model = Mobile
        fields = ('circle', 'ssa')

    def __init__(self, data, **kwargs):
        
        super().__init__(data, **kwargs)
        self.fields['ssa'].queryset = Ssa.objects.none()
        self.fields['feed_sts'] = forms.CharField(widget=forms.RadioSelect(choices=FEEDBACK_STS))
        self.fields['port_sts'] = forms.CharField(widget=forms.RadioSelect(choices=PORT_STS))
        
        
        # Probably following code is not required
        if 'circle' in self.data:
            try:
                circle_id = int(self.data.get('circle'))
                # print("GGG", circle_id)
                self.fields['ssa'].queryset = Ssa.objects.filter(circle_id=circle_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['ssa'].queryset = self.instance.circle.ssa_set.order_by('name')