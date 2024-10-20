from src.core import miembro
from src.core import cobros, jinetes_y_amazonas
from src.core.seeds_usuarios import cargar_usuarios
from src.core import ecuestre
from src.core import pago

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

    cargar_usuarios()

    cargar_diagnosticos()

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
        usuario_id=1,
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
        usuario_id=2,
        activo=False
    )

    tipos_de_jya = [
        "Hipoterapia",
        "Monta Terapéutica",
        "Deporte Ecuestre Adaptado",
        "Actividades Recreativas",
        "Equitación",
    ]
    
    for tipo in tipos_de_jya:
        ecuestre.crear_tipo_de_jya(tipo=tipo)
        
    tipos_de_documento_ecuestre = [
        "Ficha general del caballo",
        "Planificación de entrenamiento",
        "Informe de Evolución",
        "Carga de Imágenes",
        "Registro veterinario"
    ]
    
    for tipo in tipos_de_documento_ecuestre:
        ecuestre.crear_tipo_de_documento(tipo=tipo)

    j_y_a1 = jinetes_y_amazonas.crear_j_o_a(nombre="Victor", apellido="Varela", dni= 14234221, edad= 32, fecha_nacimiento='1992/09/10 13:19:38', provincia_nacimiento='San Luis', localidad_nacimiento='San Luis', domicilio_actual='12 n122',telefono_actual=2214569744, contacto_emer_nombre='Alvaro',contacto_emer_telefono=2214428864)
    j_y_a2= jinetes_y_amazonas.crear_j_o_a(nombre="Valeria", apellido="Vazquez", dni= 14234221, edad= 32, fecha_nacimiento='1992/09/10 13:19:38', provincia_nacimiento='La Pampa', localidad_nacimiento='Santa Rosa', domicilio_actual='62 n312',telefono_actual=2214569794, contacto_emer_nombre='Alvaro',contacto_emer_telefono=2214678864)
    j_y_a3 = jinetes_y_amazonas.crear_j_o_a(nombre="Veronica", apellido="Vim", dni= 14234221, edad= 32, fecha_nacimiento='1992/09/10 13:19:38', provincia_nacimiento='Buenos Aires', localidad_nacimiento='La Plata', domicilio_actual='20 n67',telefono_actual=2214569784, contacto_emer_nombre='Jimena',contacto_emer_telefono=2214671264)

    cobro1 = cobros.crear_cobro(
        medio_de_pago="efectivo",
        fecha_pago="2024/09/10 13:19:38",
        monto=400,
        observaciones="Nada para agregar",
        joa_id=j_y_a1.id,
        recibio_el_dinero_id = miembro1.id
    )
    cobro2 = cobros.crear_cobro(
        medio_de_pago="credito",
        fecha_pago="2024/09/12 13:19:38",
        monto=500,
        observaciones="Queda al día",
        joa_id=j_y_a1.id,
        recibio_el_dinero_id = miembro1.id
    )
    cobro3 = cobros.crear_cobro(
        medio_de_pago="debito",
        fecha_pago="2024/09/11 13:19:38",
        monto=600,
        observaciones="-",
        joa_id=j_y_a3.id,
        recibio_el_dinero_id = miembro2.id
    )

    ecuestre1 = ecuestre.crear_ecuestre(
        nombre="Caballo1",
        fecha_nacimiento="2020-01-01",
        sexo="M",
        raza="Criollo",
        pelaje="Tostado",
        es_compra=True,
        fecha_ingreso="2020-01-01",
        sede="Sede1",
        tipo_de_jya_id=1,
    )
    ecuestre2 = ecuestre.crear_ecuestre(
        nombre="Caballo2",
        fecha_nacimiento="2012-05-10",
        sexo="F",
        raza="Criollo",
        pelaje="Tostado",
        es_compra=False,
        fecha_ingreso="2020-01-01",
        sede="Sede2",
        tipo_de_jya_id=2,
    )
    
    ecuestre.asignar_conductor(ecuestre1, miembro1)
    ecuestre.asignar_conductor(ecuestre1, miembro2)
    ecuestre.asignar_entrenador(ecuestre1, miembro2)
    ecuestre.asignar_conductor(ecuestre2, miembro2)
    ecuestre.asignar_entrenador(ecuestre2, miembro2)

    tipos_de_pagos = [
        "Honorario",
        "Provedor",
        "Gastos varios"
    ]

    for tipo in tipos_de_pagos:
        pago.cargar_tipo_pago(nombre=tipo)

    pago1 = pago.crear_pago(
        monto=10000,
        descripcion="Horas extras",
        fecha_pago="2024-02-11",
        miembro_id=miembro1.id,
        tipo_id=1
    )

    pago2 = pago.crear_pago(
        monto=20000,
        descripcion="Mantenimiento",
        fecha_pago="2024-03-12",
        tipo_id=2
    )

    tipos_de_documento_miembro = [
        "Titulo",
        "Copia del DNI",
        "CV",
        "Certificado",
        "Vacunacion",
        "Otro"
    ]
    
    for tipo in tipos_de_documento_miembro:
        miembro.crear_tipo_de_documento(tipo=tipo)


# función que carga todos los diagnósticos que se deben mostrar en el sistema
def cargar_diagnosticos():
    diagnostico1 = jinetes_y_amazonas.crear_diagnostico(nombre="ECNE")
    diagnostico2 = jinetes_y_amazonas.crear_diagnostico(nombre="Lesión post traumática")
    diagnostico3 = jinetes_y_amazonas.crear_diagnostico(nombre="Mielomeningocele")
    diagnostico4 = jinetes_y_amazonas.crear_diagnostico(nombre="Esclerosis múltiple")
    diagnostico5 = jinetes_y_amazonas.crear_diagnostico(nombre="Escoliosis leve")
    diagnostico6 = jinetes_y_amazonas.crear_diagnostico(nombre="Secuelas de ACV")
    diagnostico7 = jinetes_y_amazonas.crear_diagnostico(
        nombre="Discapacidad intelectual"
    )
    diagnostico8 = jinetes_y_amazonas.crear_diagnostico(
        nombre="Trastorno del espectro autista"
    )
    diagnostico9 = jinetes_y_amazonas.crear_diagnostico(
        nombre="Trastorno del aprendizaje"
    )
    diagnostico10 = jinetes_y_amazonas.crear_diagnostico(
        nombre="Trastorno por déficit de atención/hiperactividad"
    )
    diagnostico11 = jinetes_y_amazonas.crear_diagnostico(
        nombre="Trastorno de la comunicación"
    )
    diagnostico12 = jinetes_y_amazonas.crear_diagnostico(nombre="Trastorno de ansiedad")
    diagnostico13 = jinetes_y_amazonas.crear_diagnostico(nombre="Síndrome de Down")
    diagnostico14 = jinetes_y_amazonas.crear_diagnostico(nombre="Retraso madurativo")
    diagnostico15 = jinetes_y_amazonas.crear_diagnostico(nombre="Psicosis")
    diagnostico16 = jinetes_y_amazonas.crear_diagnostico(nombre="Trastorno de conducta")
    diagnostico17 = jinetes_y_amazonas.crear_diagnostico(
        nombre="Trastorno del ánimo y afectivos"
    )
    diagnostico18 = jinetes_y_amazonas.crear_diagnostico(nombre="Trastorno alimentario")
    diagnostico19 = jinetes_y_amazonas.crear_diagnostico(nombre="Otro")
