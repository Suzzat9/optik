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
    # Validations 
    min_duration_mins = forms.IntegerField(label="Minimum Survey Duration in minutes")
    max_duration_mins = forms.IntegerField(label="Maximum Survey Duration in minutes")

    # Total number of surveys completed till date, number of surveys done daily 

    # Columns to plot - column names separated by commas (no spaces)
    categorical_fields = forms.CharField(max_length=2000, label="Categorical Variables to Plot", required=False)
    
    file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=["xlsx", "csv"])],
        required=True,
    )
