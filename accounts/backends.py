from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class DNIAuthBackend(ModelBackend):
    """
    Backend de autenticación que permite a los usuarios iniciar sesión usando su DNI 
    en lugar del nombre de usuario ('username').
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # El formulario de login enviará el DNI en el campo 'username', o explícitamente como 'dni'
        dni = kwargs.get('dni') or username
        
        if not dni:
            return None
            
        try:
            user = Usuario.objects.get(dni=dni)
        except Usuario.DoesNotExist:
            return None
            
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
