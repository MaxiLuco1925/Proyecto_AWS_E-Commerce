from django import forms
from app1.models import Cliente

class InicioSesionForm(forms.Form):
    email = forms.EmailField(
        label='Correo',
        widget=forms.EmailInput(attrs={'class':  'form-control'})
    )
    contraseña = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class ClienteForm(forms.ModelForm):
    password1 = forms.CharField(
        label='contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

    def save(self, commit=True):
        cliente = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        cliente.set_password(password)
        if commit:
            cliente.save()
        return cliente