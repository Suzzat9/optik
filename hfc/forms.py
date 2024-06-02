from django import forms
from django.core.validators import FileExtensionValidator


class DataDetails(forms.Form):
    respondent_id_field = forms.CharField(
        max_length=50, label="Respondent ID field", required=True
    )
    surveyor_id_field = forms.CharField(
        max_length=50, label="Surveyor ID field", required=True
    )
    date_field = forms.CharField(
        max_length=50, label="Survey date field", required=True
    )
    start_time_field = forms.CharField(
        max_length=50, label="Survey start time field", required=True
    )
    end_time_field = forms.CharField(
        max_length=50, label="Survey end time field", required=True
    )
    file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=["xlsx", "csv"])],
        required=True,
    )
