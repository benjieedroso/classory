from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML
from crispy_tailwind.templatetags.tailwind_field import CrispyTailwindFieldNode, CSSContainer

# Match the inputs styling used across the app
_input_style = (
    "w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 "
    "focus:bg-white focus:border-brand-500 focus:ring-4 focus:ring-brand-100 "
    "outline-none transition"
)
CrispyTailwindFieldNode.default_container = CSSContainer({
    "base": "",
    "text": _input_style,
    "number": _input_style,
    "email": _input_style,
    "url": _input_style,
    "password": _input_style,
    "textarea": _input_style,
    "date": _input_style,
    "datetime": _input_style,
    "time": _input_style,
    "error_border": "border-red-500",
})

SUBJECT_CHOICES = [
    ('Mathematics', 'Mathematics'),
    ('Science', 'Science'),
    ('English', 'English'),
    ('Filipino', 'Filipino'),
    ('Social Studies', 'Social Studies'),
    ('MAPEH', 'MAPEH'),
    ('Computer / ICT', 'Computer / ICT'),
]

GRADE_CHOICES = [
    ('Grade 7', 'Grade 7'),
    ('Grade 8', 'Grade 8'),
    ('Grade 9', 'Grade 9'),
    ('Grade 10', 'Grade 10'),
    ('Grade 11', 'Grade 11'),
    ('Grade 12', 'Grade 12'),
]


class CreateClassroomForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    grade_level = forms.ChoiceField(choices=GRADE_CHOICES)
    excel_file = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'e.g. Mathematics 101 — Section A'
        self.fields['description'].widget.attrs['placeholder'] = 'What is this classroom about?'
        self.fields['name'].label = 'Classroom name'
        self.fields['grade_level'].label = 'Grade level'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'block text-sm font-semibold text-slate-700 mb-1.5'
        self.helper.field_class = ''
        self.helper.layout = Layout(
            'name',
            'description',
            Div('subject', 'grade_level', css_class='grid grid-cols-2 gap-4'),
        )


class UploadScoresForm(forms.Form):
    test_name = forms.CharField()
    total_score = forms.IntegerField(min_value=1)
    excel_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['test_name'].widget.attrs['placeholder'] = 'e.g. Quiz 3 — Algebra'
        self.fields['total_score'].widget.attrs['placeholder'] = 'e.g. 50'
        self.fields['test_name'].label = 'Test name'
        self.fields['total_score'].label = 'Total score'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'block text-sm font-semibold text-slate-700 mb-1.5'
        self.helper.field_class = ''
        self.helper.layout = Layout(
            'test_name',
            'total_score',
        )
