from django import forms
from .models import Package, Lesson


class PackageForm(forms.ModelForm):

    class Meta:
        model = Package
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        lessons = Lesson.objects.all()
        friendly_names = [(l.id, l.get_friendly_name()) for l in lessons]

        self.fields['lesson'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
