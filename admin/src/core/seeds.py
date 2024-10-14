from src.core import auth
from src.core import miembro
from src.core import cobros, jinetes_y_amazonas
from src.core.seeds_usuarios import cargar_usuarios

def run():
    
    profesiones = [
        "Psicólogo/a", "Psicomotricista", "Médico/a", "Kinesiólogo/a",
        "Terapista Ocupacional", "Psicopedagogo/a", "Docente", "Profesor",
        "Fonoaudiólogo/a", "Veterinario/a", "Otro"
    ]
    for profesion in profesiones:
        miembro.crear_profesion(nombre=profesion)

    puestos = [
        "Administrativo/a", "Terapeuta", "Conductor", "Auxiliar de pista", "Herrero",
        "Veterinario", "Entrenador de Caballos", "Domador", "Profesor de Equitación",
        "Docente de Capacitación", "Auxiliar de mantenimiento", "Otro"
    ]
    for puesto in puestos:
        miembro.crear_puesto_laboral(nombre=puesto)

    condiciones = ["Voluntario", "Personal Rentado"]
    for condicion in condiciones:
        miembro.crear_condicion(nombre=condicion)

    domicilio1 = miembro.crear_domicilio(
        calle="Calle 123",
        numero="456",
        piso="2",
        dpto="A",
        localidad="Ciudad A"
    )
    
    domicilio2 = miembro.crear_domicilio(
        calle="Calle 789",
        numero="101",
        localidad="Ciudad B"
    )

    miembro1 = miembro.crear_miembro(
        nombre="Jose",
        apellido="Maria",
        dni="12345678",
        nombreContactoEmergencia="Pedro",
        telefonoContactoEmergencia="123456789",
        obraSocial="OSDE",
        numeroAfiliado="987654321",
        condicion_id=1,
        domicilio_id=domicilio1.id,
        email="jose@mail.com",
        telefono="111222333",
        profesion_id=1,
        puesto_laboral_id=1,
        user_id=user1.id,
        activo=True
    )

    miembro2 = miembro.crear_miembro(
        nombre="Ana",
        apellido="Perez",
        dni="87654321",
        nombreContactoEmergencia="Laura",
        telefonoContactoEmergencia="987654321",
        obraSocial="Swiss Medical",
        numeroAfiliado="123456789",
        condicion_id=1,
        domicilio_id=domicilio2.id,
        email="ana@mail.com",
        telefono="222333444",
        profesion_id=1,
        puesto_laboral_id=1,
        user_id=user2.id,
        activo=False
    )

    
    cargar_usuarios()

    cargar_diagnosticos()

    j_y_a1= jinetes_y_amazonas.crear_j_o_a(nombre="Victor", apellido="Varela")
    j_y_a3= jinetes_y_amazonas.crear_j_o_a(nombre="Veronica", apellido="Vim")    
    cobro1 = cobros.crear_cobro(medio_de_pago='efectivo', fecha_pago = '2024/09/10 13:19:38',monto=400, observaciones="Nada para agregar", joa_id=j_y_a1.id)
    cobro2 = cobros.crear_cobro(medio_de_pago='credito', fecha_pago = '2024/09/12 13:19:38', monto=500, observaciones="Queda al día",joa_id=j_y_a1.id)
    cobro3 = cobros.crear_cobro(medio_de_pago='debito', fecha_pago = '2024/09/11 13:19:38', monto=600, observaciones="-",joa_id=j_y_a3.id)


# función que carga todos los diagnósticos que se deben mostrar en el sistema
def cargar_diagnosticos():
    diagnostico1 = jinetes_y_amazonas.crear_diagnostico(nombre="ECNE")
    diagnostico2 = jinetes_y_amazonas.crear_diagnostico(nombre="Lesión post traumática")
    diagnostico3 = jinetes_y_amazonas.crear_diagnostico(nombre="Mielomeningocele")
    diagnostico4 = jinetes_y_amazonas.crear_diagnostico(nombre="Esclerosis múltiple")
    diagnostico5 = jinetes_y_amazonas.crear_diagnostico(nombre="Escoliosis leve")
    diagnostico6 = jinetes_y_amazonas.crear_diagnostico(nombre="Secuelas de ACV")
    diagnostico7 = jinetes_y_amazonas.crear_diagnostico(nombre="Discapacidad intelectual")
    diagnostico8 = jinetes_y_amazonas.crear_diagnostico(nombre="Trastorno del espectro autista")
    diagnostico9 = jinetes_y_amazonas.crear_diagnostico(nombre="Trastorno del aprendizaje")
    diagnostico10 = jinetes_y_amazonas.crear_diagnostico(nombre="Trastorno por déficit de atención/hiperactividad")
    diagnostico11 = jinetes_y_amazonas.crear_diagnostico(nombre="Trastorno de la comunicación")
    diagnostico12 = jinetes_y_amazonas.crear_diagnostico(nombre="Trastorno de ansiedad")
    diagnostico13 = jinetes_y_amazonas.crear_diagnostico(nombre="Síndrome de Down")
    diagnostico14 = jinetes_y_amazonas.crear_diagnostico(nombre="Retraso madurativo")
    diagnostico15 = jinetes_y_amazonas.crear_diagnostico(nombre="Psicosis")
    diagnostico16 = jinetes_y_amazonas.crear_diagnostico(nombre="Trastorno de conducta")
    diagnostico17 = jinetes_y_amazonas.crear_diagnostico(nombre="Trastorno del ánimo y afectivos")
    diagnostico18 = jinetes_y_amazonas.crear_diagnostico(nombre="Trastorno alimentario")
    diagnostico19 = jinetes_y_amazonas.crear_diagnostico(nombre="Otro")
