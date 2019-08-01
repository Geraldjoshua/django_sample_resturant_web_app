from django import forms

class NameForm(forms.Form):
	First_name=forms.CharField(label='First name',max_length=100)
	Last_name=forms.CharField(label='Surname',max_length=100)
	Country=forms.CharField(label='Country',initial='South Africa')
	City=forms.CharField(label='City',max_length=100)
	Street_address=forms.CharField(label='Street address',max_length=100)
	Province=forms.CharField(label='Province',max_length=100)
	Zip=forms.CharField(label='Zip',max_length=100)
	Phone=forms.CharField(label='Phone number',max_length=100)
	Email_address=forms.EmailField(label='Email address',max_length=100)
	cash_or_card=forms.CharField(label='cash or card',max_length=100)