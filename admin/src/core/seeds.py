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
        dni="31732976",
        nombre_contacto_emergencia="Pedro",
        telefono_contacto_emergencia="123456789",
        obra_social="OSDE",
        numero_afiliado="763",
        condicion_id=1,
        domicilio_id=domicilio1.id,
        email="jose@mail.com",
        telefono="211579341",
        profesion_id=1,
        puesto_laboral_id=2,
        usuario_id=1,
        activo=True
    )

    miembro2 = miembro.crear_miembro(
        nombre="Ana",
        apellido="Garcia",
        dni="23455902",
        nombre_contacto_emergencia="Laura",
        telefono_contacto_emergencia="987654321",
        obra_social="Swiss Medical",
        numero_afiliado="891",
        condicion_id=1,
        domicilio_id=domicilio2.id,
        email="ana@mail.com",
        telefono="211986321",
        profesion_id=10,
        puesto_laboral_id=6,
        usuario_id=2,
        activo=True
    )
    
    #Creo un miembro con con puesto entrenador de caballos para asignarlo a un ecuestre
    miembro3 = miembro.crear_miembro(
        nombre="Fernando",
        apellido="Gomez",
        dni="34567890",
        nombre_contacto_emergencia="Juan",
        telefono_contacto_emergencia="345678901",
        obra_social="OSDE",
        numero_afiliado="345678901",
        condicion_id=1,
        domicilio_id=domicilio2.id,
        email="fer@mail.com",
        telefono="333444555",
        profesion_id=11,
        puesto_laboral_id=7,
        usuario_id=3,
        activo=True
    )
    
    #Creo un miembro con con puesto conductor para asignarlo a un ecuestre
    miembro4 = miembro.crear_miembro(
        nombre="Carlos",
        apellido="Gimenez",
        dni="45678901",
        nombre_contacto_emergencia="Pedro",
        telefono_contacto_emergencia="345678902",
        obra_social="OSDE",
        numero_afiliado="456789012",
        condicion_id=1,
        domicilio_id=domicilio2.id,
        email="carlos@mail.com",
        telefono="444555666",
        profesion_id=11,
        puesto_laboral_id=3,
        usuario_id=4,
        activo=True
    )

    # Creo un miembro con puesto Conductor de caballo
    miembro5 = miembro.crear_miembro(
        nombre="Gisela",
        apellido="Gimenez",
        dni="16543345",
        nombre_contacto_emergencia="Valeria",
        telefono_contacto_emergencia="2214566655",
        obra_social="OSDE",
        numero_afiliado="345678903",
        condicion_id=1,
        domicilio_id=domicilio2.id,
        email="giselagimenez@mail.com",
        telefono="2214567766",
        profesion_id=11,
        puesto_laboral_id=3,
        usuario_id=9,
        activo=True
    )

    # Creo un miembro con puesto Conductor de caballo
    miembro6 = miembro.crear_miembro(
        nombre="Gloria",
        apellido="Valente",
        dni="16548875",
        nombre_contacto_emergencia="Cristian",
        telefono_contacto_emergencia="2214511155",
        obra_social="IOMA",
        numero_afiliado="115678905",
        condicion_id=1,
        domicilio_id=domicilio2.id,
        email="gloriavalente@mail.com",
        telefono="2214567766",
        profesion_id=11,
        puesto_laboral_id=3,
        usuario_id=10,
        activo=True
    )

    # Creo un miembro con puesto Profesor de equitación
    miembro7 = miembro.crear_miembro(
        nombre="Leandro",
        apellido="Larez",
        dni="18548875",
        nombre_contacto_emergencia="Cristian",
        telefono_contacto_emergencia="2214511155",
        obra_social="IOMA",
        numero_afiliado="116789017",
        condicion_id=1,
        domicilio_id=domicilio2.id,
        email="leandrolarez@mail.com",
        telefono="2214567766",
        profesion_id=11,
        puesto_laboral_id=9,
        usuario_id=11,
        activo=True
    )


    # Creo un miembro con puesto Profesor de equitación
    miembro8 = miembro.crear_miembro(
        nombre="Vanesa",
        apellido="Velazquez",
        dni="18548899",
        nombre_contacto_emergencia="Javier",
        telefono_contacto_emergencia="2214511155",
        obra_social="OSESAC",
        numero_afiliado="345678908",
        condicion_id=1,
        domicilio_id=domicilio2.id,
        email="vanesavelazquez@mail.com",
        telefono="2214567766",
        profesion_id=11,
        puesto_laboral_id=9,
        usuario_id=12,
        activo=True
    )

    # Creo un miembro con puesto Auxiliar de pista
    miembro8 = miembro.crear_miembro(
        nombre="Guillermo",
        apellido="Limbo",
        dni="18533449",
        nombre_contacto_emergencia="Lorena",
        telefono_contacto_emergencia="2214511155",
        obra_social="IOMA",
        numero_afiliado="345678902",
        condicion_id=1,
        domicilio_id=domicilio2.id,
        email="guillermolimbo@mail.com",
        telefono="2214567766",
        profesion_id=11,
        puesto_laboral_id=4,
        usuario_id=13,
        activo=True
    )

    # Creo un miembro con puesto Auxiliar de pista
    miembro8 = miembro.crear_miembro(
        nombre="Lucas",
        apellido="Luquez",
        dni="184438919",
        nombre_contacto_emergencia="Sofia",
        telefono_contacto_emergencia="2214511155",
        obra_social="Sancor Salud",
        numero_afiliado="1456789067",
        condicion_id=1,
        domicilio_id=domicilio2.id,
        email="lucasluquez@mail.com",
        telefono="2214567766",
        profesion_id=11,
        puesto_laboral_id=4,
        usuario_id=14,
        activo=True
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

    j_y_a1 = jinetes_y_amazonas.crear_j_o_a(nombre="Victor", apellido="Varela",
                                            dni=36234221,
                                            fecha_nacimiento='1992/09/10',
                                            provincia_nacimiento='San Luis',
                                            localidad_nacimiento='San Luis',
                                            domicilio_actual='12 n122',
                                            telefono_actual='2214569744',
                                            contacto_emer_nombre='Alvaro',
                                            contacto_emer_telefono='2214428864',
                                            becado=True, porcentaje_beca=25)
    j_y_a2= jinetes_y_amazonas.crear_j_o_a(nombre="Tatiana", apellido="Tomassi",
                                           dni=36234222,
                                           fecha_nacimiento='1992/09/10',
                                           provincia_nacimiento='La Pampa',
                                           localidad_nacimiento='Santa Rosa',
                                           domicilio_actual='62 n312',
                                           telefono_actual='2214569794',
                                           contacto_emer_nombre='Martin',
                                           contacto_emer_telefono='2214678864',
                                           becado=True, porcentaje_beca=30)
    j_y_a3 = jinetes_y_amazonas.crear_j_o_a(nombre="Saul", apellido="Sosa",
                                            dni=36234223,
                                            fecha_nacimiento='1992/09/10',
                                            provincia_nacimiento='Buenos Aires',
                                            localidad_nacimiento='La Plata',
                                            domicilio_actual='20 n67',
                                            telefono_actual='2214569784',
                                            contacto_emer_nombre='Jimena',
                                            contacto_emer_telefono='2214671264',
                                            becado=True, porcentaje_beca=30)
    j_y_a4 = jinetes_y_amazonas.crear_j_o_a(nombre="Romina", apellido="Rodriguez",
                                            dni=36234224,
                                            fecha_nacimiento='1992/09/10',
                                            provincia_nacimiento='San Luis',
                                            localidad_nacimiento='San Luis',
                                            domicilio_actual='12 n122',
                                            telefono_actual='2214569744',
                                            contacto_emer_nombre='Valentina',
                                            contacto_emer_telefono='2214428864',
                                            becado=True, porcentaje_beca=25)
    j_y_a5 = jinetes_y_amazonas.crear_j_o_a(nombre="Quimey", apellido="Quiroga",
                                            dni=36234225,
                                            fecha_nacimiento='1992/09/10',
                                            provincia_nacimiento='San Luis',
                                            localidad_nacimiento='San Luis',
                                            domicilio_actual='12 n122',
                                            telefono_actual='2214569744',
                                            contacto_emer_nombre='Paloma',
                                            contacto_emer_telefono='2214428864',
                                            becado=True, porcentaje_beca=25)
    j_y_a6 = jinetes_y_amazonas.crear_j_o_a(nombre="Paula", apellido="Paredes",
                                            dni=36234226,
                                            fecha_nacimiento='1992/09/10',
                                            provincia_nacimiento='San Luis',
                                            localidad_nacimiento='San Luis',
                                            domicilio_actual='12 n122',
                                            telefono_actual='2214569744',
                                            contacto_emer_nombre='Valentin',
                                            contacto_emer_telefono='2214428864',
                                            becado=True, porcentaje_beca=30)
    j_y_a7 = jinetes_y_amazonas.crear_j_o_a(nombre="Omar", apellido="Ortega",
                                            dni=36234227,
                                            fecha_nacimiento='1992/09/10',
                                            provincia_nacimiento='San Luis',
                                            localidad_nacimiento='San Luis',
                                            domicilio_actual='12 n122',
                                            telefono_actual='2214569744',
                                            contacto_emer_nombre='Carlos',
                                            contacto_emer_telefono='2214428864',
                                            becado=True, porcentaje_beca=50)
    j_y_a8 = jinetes_y_amazonas.crear_j_o_a(nombre="Nicol", apellido="Nivez",
                                            dni=36234228,
                                            fecha_nacimiento='1992/09/10',
                                            provincia_nacimiento='San Luis',
                                            localidad_nacimiento='San Luis',
                                            domicilio_actual='12 n122',
                                            telefono_actual='2214569744',
                                            contacto_emer_nombre='Miranda',
                                            contacto_emer_telefono='2214428864',
                                            becado=True, porcentaje_beca=30)
    j_y_a9 = jinetes_y_amazonas.crear_j_o_a(nombre="Mario", apellido="Muccio",
                                            dni=36234229,
                                            fecha_nacimiento='1992/09/10',
                                            provincia_nacimiento='San Luis',
                                            localidad_nacimiento='San Luis',
                                            domicilio_actual='12 n122',
                                            telefono_actual='2214569744',
                                            contacto_emer_nombre='Mabel',
                                            contacto_emer_telefono='2214428864',
                                            becado=True, porcentaje_beca=25)
    j_y_a10 = jinetes_y_amazonas.crear_j_o_a(nombre="Lourdes",
                                             apellido="Lampa",
                                             dni=36234231,
                                             fecha_nacimiento='1992/09/10',
                                             provincia_nacimiento='San Luis',
                                             localidad_nacimiento='San Luis',
                                             domicilio_actual='12 n122',
                                             telefono_actual='2214569744',
                                             contacto_emer_nombre='Pablo',
                                             contacto_emer_telefono='2214428864',
                                             becado=False)
    j_y_a11 = jinetes_y_amazonas.crear_j_o_a(nombre="Juan", apellido="Juarez",
                                             dni=36234232,
                                             fecha_nacimiento='1992/09/10',
                                             provincia_nacimiento='San Luis',
                                             localidad_nacimiento='San Luis',
                                             domicilio_actual='12 n122',
                                             telefono_actual='2214569744',
                                             contacto_emer_nombre='Juan',
                                             contacto_emer_telefono='2214428864',
                                             becado=False)

    cobro1 = cobros.crear_cobro(
        medio_de_pago="efectivo",
        fecha_pago="2024/09/10 13:19:38",
        monto=400,
        observaciones="Nada para agregar",
        joa_id=j_y_a1.id,
        recibio_el_dinero_id=miembro1.id,
        tiene_deuda=False
    )
    cobro2 = cobros.crear_cobro(
        medio_de_pago="credito",
        fecha_pago="2024/09/12 13:19:38",
        monto=500,
        observaciones="Queda al día",
        joa_id=j_y_a1.id,
        recibio_el_dinero_id=miembro1.id,
        tiene_deuda=True
    )
    cobro3 = cobros.crear_cobro(
        medio_de_pago="debito",
        fecha_pago="2024/09/11 13:19:38",
        monto=600,
        observaciones="-",
        joa_id=j_y_a3.id,
        recibio_el_dinero_id=miembro2.id,
        tiene_deuda=False
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
        conductores=[miembro4],
        entrenadores=[miembro3]
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
        conductores=[],
        entrenadores=[]
    )

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
