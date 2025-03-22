from usuarios.models import PerfilUsuario
from empresas.models import Empresa

def global_context(request):
    perfil = None
    empresas = None
    if request.user.is_authenticated:
        perfil = PerfilUsuario.objects.filter(usuario=request.user).first()
        empresas = Empresa.objects.all()

    empresa_id = request.session.get('empresa_id')
    empresa_activa = None
    if empresa_id:
        empresa_activa = Empresa.objects.filter(id=empresa_id).first()
    
    return {
        'perfil': perfil,
        'empresas': empresas,
        'empresa_id': empresa_id,  
        'empresa_activa': empresa_activa,
    }