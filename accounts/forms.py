from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML
from crispy_tailwind.templatetags.tailwind_field import CrispyTailwindFieldNode, CSSContainer

User = get_user_model()

# Style crispy-tailwind inputs to match the original UI
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


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['password'].widget.attrs['placeholder'] = '••••••••'
        self.fields['password'].label = ''
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'block text-sm font-semibold text-slate-700 mb-1.5'
        self.helper.field_class = ''
        self.helper.layout = Layout(
            'username',
            HTML(
                '<div class="flex items-center justify-between mb-1.5">'
                '<label for="id_password" class="block text-sm font-semibold text-slate-700">Password</label>'
                '<a href="#" class="text-sm font-medium text-brand-600 hover:text-brand-700">Forgot password?</a>'
                '</div>'
            ),
            'password',
        )


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('student', 'Student'), ('teacher', 'Teacher')])

    class Meta:
        model = User
        fields = ['role', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'e.g. juan.delacruz'
        self.fields['email'].widget.attrs['placeholder'] = 'you@example.com'
        self.fields['password1'].widget.attrs['placeholder'] = '••••••••'
        self.fields['password2'].widget.attrs['placeholder'] = '••••••••'
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email address'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'block text-sm font-semibold text-slate-700 mb-1.5'
        self.helper.field_class = ''
        self.helper.layout = Layout(
            'username',
            'email',
            Div('password1', 'password2', css_class='grid grid-cols-2 gap-4'),
        )


class ProfileSetupStudentForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    section = forms.ChoiceField(choices=[
        ('Grade 7 — Rizal', 'Grade 7 — Rizal'),
        ('Grade 7 — Mabini', 'Grade 7 — Mabini'),
        ('Grade 8 — Luna', 'Grade 8 — Luna'),
        ('Grade 8 — Bonifacio', 'Grade 8 — Bonifacio'),
        ('Grade 9 — Aguinaldo', 'Grade 9 — Aguinaldo'),
        ('Grade 9 — Quezon', 'Grade 9 — Quezon'),
        ('Grade 10 — Osmeña', 'Grade 10 — Osmeña'),
        ('Grade 10 — Roxas', 'Grade 10 — Roxas'),
    ])
    student_id = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Juan'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Dela Cruz'
        self.fields['student_id'].widget.attrs['placeholder'] = 'e.g. 2024-00123'
        self.fields['student_id'].label = 'Student ID'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'block text-sm font-semibold text-slate-700 mb-1.5'
        self.helper.field_class = ''
        self.helper.layout = Layout(
            Div('first_name', 'last_name', css_class='grid grid-cols-2 gap-4'),
            'section',
            'student_id',
        )


class ProfileSetupTeacherForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    department = forms.ChoiceField(choices=[
        ('Mathematics', 'Mathematics'),
        ('Science', 'Science'),
        ('English', 'English'),
        ('Filipino', 'Filipino'),
        ('Social Studies', 'Social Studies'),
        ('MAPEH', 'MAPEH'),
        ('Computer / ICT', 'Computer / ICT'),
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Juan'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Dela Cruz'
        self.fields['department'].label = 'Subject / Department'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'block text-sm font-semibold text-slate-700 mb-1.5'
        self.helper.field_class = ''
        self.helper.layout = Layout(
            Div('first_name', 'last_name', css_class='grid grid-cols-2 gap-4'),
            'department',
        )
