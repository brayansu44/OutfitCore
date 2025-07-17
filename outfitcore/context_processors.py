from usuarios.models import PerfilUsuario
from empresas.models import Empresa
from nomina.models import Contrato

def global_context(request):
    user = None
    perfil = None
    contrato = None
    empresas = None
    if request.user.is_authenticated:
        user = request.user
        perfil = PerfilUsuario.objects.filter(usuario=request.user).first()
        if perfil:
            contrato = Contrato.objects.filter(perfil=perfil).first()
    empresas = Empresa.objects.all
        
    empresa_id = request.session.get('empresa_id')
        
    empresa_activa = None
        
    if empresa_id:
        
        empresa_activa = Empresa.objects.filter(id=empresa_id).first()    
    
    return {
        'perfil': perfil,
        'user': user,
        'contrato': contrato,
        'empresas': empresas,
        'empresa_id': empresa_id,  
        'empresa_activa': empresa_activa,
    }