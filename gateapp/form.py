from django import forms


class UserDetailsForm(forms.Form):
    operating_system = forms.ChoiceField(
        label='Operating System',
        choices=[('windows', 'Windows'), ('linux', 'Linux')],
        widget=forms.RadioSelect
    )
    request_limit_unit = forms.ChoiceField(
        label='Request Limit Unit', 
        choices=[('r/s', 'req per sec '), ('r/m', 'req per min')],
        widget=forms.RadioSelect
    )
    request_limit = forms.IntegerField(label='Request Limit', min_value=1)

    proxy_URL = forms.URLField(label='Proxy URL', max_length=200)
    end_point = forms.CharField(label='End Point', max_length=200)
    block_all_private_ips = forms.ChoiceField(
        label='Block All Private IPs',
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect
    )
    number_of_private_ips = forms.IntegerField(
        label='Number of Specific Private IPs',
        min_value=1,
        required=False
    )
    block_all_public_ips = forms.ChoiceField(
        label='Block All Public IPs',
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect
    )
    number_of_public_ips = forms.IntegerField(
        label='Number of Specific Public IPs',
        min_value=1,
        required=False
    )
