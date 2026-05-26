from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PerfilAventurero, Registro  # <-- IMPORTANTE: Importa el nuevo modelo aquí

# --- VISTA DE CARGA GENERAL ---
def pantalla_carga(request):
    return render(request, 'core/carga.html')


# --- CREACIÓN DE PERFILES (PASITOS AL SABER) ---
def crear_perfil(request):
    if request.method == 'POST':
        # CASO A: El niño seleccionó un perfil ya existente en el dispositivo
        perfil_id_existente = request.POST.get('perfil_id_existente')
        if perfil_id_existente:
            try:
                perfil = PerfilAventurero.objects.get(id=perfil_id_existente)
                request.session['perfil_id'] = perfil.id
                if perfil.edad in [3, 4]:
                    return redirect('dashboard_infantil_baja')
                else:
                    return redirect('dashboard_infantil_alta')
            except PerfilAventurero.DoesNotExist:
                return redirect('crear_perfil')

        # CASO B: Es la creación de un perfil totalmente nuevo
        nombre = request.POST.get('nombre_usuario')
        edad = int(request.POST.get('edad'))
        avatar = request.POST.get('avatar')

        # 1. Guardar el perfil en la base de datos MySQL (Tu código original)
        nuevo_perfil = PerfilAventurero.objects.create(
            nombre_usuario=nombre,
            edad=edad,
            avatar=avatar
        )

        # ====================================================================
        # NUEVO CAMBIO: Guardamos el historial en la nueva tabla 'registro'
        # ====================================================================
        # Django se encarga de rellenar id_usuario y fecha_creacion automáticamente
        Registro.objects.create(perfil=nuevo_perfil)
        # ====================================================================

        # Guardamos el ID en la sesión
        request.session['perfil_id'] = nuevo_perfil.id

        # Renderizamos la pantalla intermedia para el almacenamiento local del dispositivo
        return render(request, 'core/crear_perfil.html', {
            'perfil_recien_creado_id': nuevo_perfil.id,
            'edad_redireccion': edad
        })

    # Si es GET, consultamos todos los perfiles de la base de datos para que el navegador los filtre
    perfiles_bd = PerfilAventurero.objects.all()
    return render(request, 'core/crear_perfil.html', {'perfiles_guardados': perfiles_bd})


# --- DASHBOARDS EDUCATIVOS SEGÚN RANGO DE EDAD ---

# Vista real para niños de 3 a 4 años (Envía los datos del avatar al Parque de Juegos)
def dashboard_baja(request):
    # CORREGIDO: Buscamos primero el perfil de la sesión actual
    perfil_id = request.session.get('perfil_id')
    perfil_activo = None
    
    if perfil_id:
        try:
            perfil_activo = PerfilAventurero.objects.get(id=perfil_id)
        except PerfilAventurero.DoesNotExist:
            pass
            
    # Fallback: Si no hay sesión válida, tomamos el último perfil como respaldo
    if not perfil_activo:
        perfil_activo = PerfilAventurero.objects.order_by('-id').first()
    
    # Si la base de datos está completamente vacía, evitamos errores con un diccionario por defecto
    if not perfil_activo:
        perfil_activo = {
            'nombre_usuario': 'Aventurero',
            'avatar': 'avatar1'
        }
        
    return render(request, 'core/dashboard_3_4.html', {'perfil': perfil_activo})


# Vista real para niños de 5 a 7 años (Envía los datos del avatar a la Isla de Desafíos)
def dashboard_alta(request):
    # CORREGIDO: Buscamos primero el perfil de la sesión actual
    perfil_id = request.session.get('perfil_id')
    perfil_activo = None
    
    if perfil_id:
        try:
            perfil_activo = PerfilAventurero.objects.get(id=perfil_id)
        except PerfilAventurero.DoesNotExist:
            pass
            
    # Fallback: Si no hay sesión válida, tomamos el último perfil como respaldo
    if not perfil_activo:
        perfil_activo = PerfilAventurero.objects.order_by('-id').first()
    
    # Si la base de datos está vacía, usamos un avatar de respaldo para evitar errores
    if not perfil_activo:
        perfil_activo = {
            'nombre_usuario': 'Aventurero',
            'avatar': 'avatar1'
        }
        
    return render(request, 'core/dashboard_5_7.html', {'perfil': perfil_activo})


# --- SECCIÓN DE PERFIL DEL ALUMNO Y MONITOREO ---

# Vista para ver el perfil del alumno activo
def perfil_alumno_view(request):
    # Intentamos obtener el perfil activo del niño por sesión
    perfil = None
    if 'perfil_id' in request.session:
        try:
            perfil = PerfilAventurero.objects.get(id=request.session['perfil_id'])
        except PerfilAventurero.DoesNotExist:
            pass
            
    if not perfil:
        # Fallback de respaldo por si estás haciendo pruebas locales sin sesión iniciada
        perfil = PerfilAventurero.objects.first()

    return render(request, 'core/perfil_alumno.html', {'perfil': perfil})


# --- CONTROL DE PADRES (CORREGIDO Y AJUSTADO AL ALUMNO ACTIVO) ---

def panel_tutores(request):
    # 1. Intentamos buscar al niño que está jugando actualmente usando el ID de la sesión
    niño_activo = None
    if 'perfil_id' in request.session:
        try:
            niño_activo = PerfilAventurero.objects.get(id=request.session['perfil_id'])
        except PerfilAventurero.DoesNotExist:
            pass

    # 2. Si no hay sesión activa por alguna razón, tomamos el último registrado como respaldo
    if not niño_activo:
        niño_activo = PerfilAventurero.objects.order_by('-id').first()

    context = {
        'hijo': niño_activo,
    }
    return render(request, 'core/panel_tutores.html', context)