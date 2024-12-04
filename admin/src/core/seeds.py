from src.core import miembro
from src.core import cobros, jinetes_y_amazonas
from src.core.seeds_usuarios import cargar_usuarios, cargar_solicitudes
from src.core import ecuestre
from src.core import pago
from src.core import anuncios
from src.core.seeds_anuncios import cargar_anuncios
from src.core import contacto


def run():

    print("Cargando la base de datos...")
    cargar_usuarios()
    print("Usuarios OK")
    cargar_solicitudes()
    print("Solicitudes OK")

    profesiones = [
        "Psicólogo/a", "Psicomotricista", "Médico/a", "Kinesiólogo/a",
        "Terapista Ocupacional", "Psicopedagogo/a", "Docente", "Profesor",
        "Fonoaudiólogo/a", "Veterinario/a", "Otro"
    ]
    for profesion in profesiones:
        miembro.crear_profesion(nombre=profesion)

    puestos = [
        "Administrativo/a", "Terapeuta", "Conductor",
        "Auxiliar de pista", "Herrero",
        "Veterinario", "Entrenador de Caballos", "Domador",
        "Profesor de Equitación",
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

    cargar_diagnosticos()
    cargar_dias()
    cargar_tipos_de_discapacidad()

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
    
    # Creo un miembro con con puesto entrenador
    # de caballos para asignarlo a un ecuestre
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
    
    # Creo un miembro con con puesto conductor para asignarlo a un ecuestre
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
    miembro.crear_miembro(
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
    miembro.crear_miembro(
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
    miembro.crear_miembro(
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
    miembro.crear_miembro(
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
    miembro.crear_miembro(
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
    miembro.crear_miembro(
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

    jinetes_y_amazonas.cargar_deuda(j_y_a1, True)
    jinetes_y_amazonas.cargar_propuesta_trabajo(j_y_a1, 'hipoterapia')
    jinetes_y_amazonas.cargar_condicion(j_y_a1, 'regular')
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a1, 1)
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a1, 2)
    jinetes_y_amazonas.cargar_tipo_discapacidad(j_y_a1, 1)
    jinetes_y_amazonas.cargar_tipo_discapacidad(j_y_a1, 2)
    j_y_a2 = jinetes_y_amazonas.crear_j_o_a(nombre="Tatiana",
                                            apellido="Tomassi",
                                            dni=36234222,
                                            fecha_nacimiento='1992/09/10',
                                            provincia_nacimiento='La Pampa',
                                            localidad_nacimiento='Santa Rosa',
                                            domicilio_actual='62 n312',
                                            telefono_actual='2214569794',
                                            contacto_emer_nombre='Martin',
                                            contacto_emer_telefono='2214678864',
                                            becado=True, porcentaje_beca=30)
    jinetes_y_amazonas.cargar_deuda(j_y_a2, False)
    jinetes_y_amazonas.cargar_propuesta_trabajo(j_y_a2, 'hipoterapia')
    jinetes_y_amazonas.cargar_condicion(j_y_a2, 'regular')
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a2, 1)
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a2, 5)
    jinetes_y_amazonas.cargar_tipo_discapacidad(j_y_a2, 2)
    jinetes_y_amazonas.cargar_tipo_discapacidad(j_y_a2, 4)
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
    jinetes_y_amazonas.cargar_deuda(j_y_a3, True)
    jinetes_y_amazonas.cargar_propuesta_trabajo(j_y_a3, 'monta_terapeutica')
    jinetes_y_amazonas.cargar_condicion(j_y_a3, 'regular')
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a3, 4)
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a3, 5)
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a3, 6)
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a3, 1)
    jinetes_y_amazonas.cargar_tipo_discapacidad(j_y_a3, 4)
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
    jinetes_y_amazonas.cargar_deuda(j_y_a4, False)
    jinetes_y_amazonas.cargar_propuesta_trabajo(j_y_a4, 'deporte_ecuestre')
    jinetes_y_amazonas.cargar_condicion(j_y_a4, 'de_baja')
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a4, 2)
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a4, 3)
    jinetes_y_amazonas.cargar_tipo_discapacidad(j_y_a4, 3)
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
    jinetes_y_amazonas.cargar_deuda(j_y_a5, False)
    jinetes_y_amazonas.cargar_propuesta_trabajo(j_y_a5,
                                                'actividades_recreativas')
    jinetes_y_amazonas.cargar_condicion(j_y_a5, 'de_baja')
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a5, 7)
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a5, 1)
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a5, 2)
    jinetes_y_amazonas.cargar_tipo_discapacidad(j_y_a5, 1)
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
    jinetes_y_amazonas.cargar_deuda(j_y_a6, False)
    jinetes_y_amazonas.cargar_propuesta_trabajo(j_y_a6, 'equitacion')
    jinetes_y_amazonas.cargar_condicion(j_y_a6, 'regular')
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a6, 3)
    jinetes_y_amazonas.cargar_tipo_discapacidad(j_y_a6, 1)
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
    jinetes_y_amazonas.cargar_deuda(j_y_a7, True)
    jinetes_y_amazonas.cargar_propuesta_trabajo(j_y_a7, 'equitacion')
    jinetes_y_amazonas.cargar_condicion(j_y_a7, 'regular')
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a7, 2)
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a7, 5)
    jinetes_y_amazonas.cargar_tipo_discapacidad(j_y_a7, 1)
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
    jinetes_y_amazonas.cargar_deuda(j_y_a8, False)
    jinetes_y_amazonas.cargar_propuesta_trabajo(j_y_a8, 'equitacion')
    jinetes_y_amazonas.cargar_condicion(j_y_a8, 'de_baja')
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a8, 2)
    jinetes_y_amazonas.cargar_tipo_discapacidad(j_y_a8, 2)
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
    jinetes_y_amazonas.cargar_deuda(j_y_a9, False)
    jinetes_y_amazonas.cargar_propuesta_trabajo(j_y_a9, 'equitacion')
    jinetes_y_amazonas.cargar_condicion(j_y_a9, 'regular')
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a9, 4)
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a9, 6)
    jinetes_y_amazonas.cargar_tipo_discapacidad(j_y_a9, 4)
    jinetes_y_amazonas.cargar_tipo_discapacidad(j_y_a9, 3)
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
    jinetes_y_amazonas.cargar_deuda(j_y_a10, False)
    jinetes_y_amazonas.cargar_propuesta_trabajo(j_y_a10, 'deporte_ecuestre')
    jinetes_y_amazonas.cargar_condicion(j_y_a10, 'regular')
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a10, 1)
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a10, 2)
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a10, 4)
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a10, 5)
    jinetes_y_amazonas.cargar_tipo_discapacidad(j_y_a10, 1)

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
    jinetes_y_amazonas.cargar_deuda(j_y_a11, False)
    jinetes_y_amazonas.cargar_propuesta_trabajo(j_y_a11, 'monta_terapeutica')
    jinetes_y_amazonas.cargar_condicion(j_y_a11, 'regular')
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a11, 4)
    jinetes_y_amazonas.cargar_dia_a_jinete(j_y_a11, 5)
    jinetes_y_amazonas.cargar_tipo_discapacidad(j_y_a11, 1)

    cobros.crear_cobro(
        medio_de_pago="efectivo",
        fecha_pago="2024/08/10 13:19:38",
        monto=4000,
        observaciones="Nada para agregar",
        joa_id=j_y_a1.id,
        recibio_el_dinero_id=miembro1.id,
    )
    cobros.crear_cobro(
        medio_de_pago="credito",
        fecha_pago="2024/09/12 13:19:38",
        monto=5000,
        observaciones="Queda al día",
        joa_id=j_y_a1.id,
        recibio_el_dinero_id=miembro1.id,
    )
    cobros.crear_cobro(
        medio_de_pago="debito",
        fecha_pago="2024/10/11 13:19:38",
        monto=6000,
        observaciones="-",
        joa_id=j_y_a3.id,
        recibio_el_dinero_id=miembro2.id,
    )
    cobros.crear_cobro(
        medio_de_pago="efectivo",
        fecha_pago="2024/07/10 13:19:38",
        monto=4000,
        observaciones="Nada para agregar",
        joa_id=j_y_a5.id,
        recibio_el_dinero_id=miembro1.id,
    )
    cobros.crear_cobro(
        medio_de_pago="credito",
        fecha_pago="2024/08/12 13:19:38",
        monto=5600,
        observaciones="Queda al día",
        joa_id=j_y_a7.id,
        recibio_el_dinero_id=miembro1.id,
    )
    cobros.crear_cobro(
        medio_de_pago="debito",
        fecha_pago="2024/06/11 13:19:38",
        monto=6400,
        observaciones="-",
        joa_id=j_y_a8.id,
        recibio_el_dinero_id=miembro2.id,
    )
    cobros.crear_cobro(
        medio_de_pago="efectivo",
        fecha_pago="2024/08/10 13:19:38",
        monto=4000,
        observaciones="Nada para agregar",
        joa_id=j_y_a9.id,
        recibio_el_dinero_id=miembro1.id,
    )
    cobros.crear_cobro(
        medio_de_pago="credito",
        fecha_pago="2024/10/12 13:19:38",
        monto=7000,
        observaciones="Queda al día",
        joa_id=j_y_a10.id,
        recibio_el_dinero_id=miembro1.id,
    )
    cobros.crear_cobro(
        medio_de_pago="debito",
        fecha_pago="2024/11/11 13:19:38",
        monto=8000,
        observaciones="-",
        joa_id=j_y_a11.id,
        recibio_el_dinero_id=miembro2.id,
    )

    ecuestre1 = ecuestre.crear_ecuestre(
        nombre="Relámpago",
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
        nombre="Hipo",
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

    anuncio = anuncios.crear_anuncio("Título", "Copete", "Contenido", 1)
    cargar_anuncios()

    contacto1 = contacto.crear_consulta("consulta1", "consulta1@gmail.com", "consulta1")
    contacto2 = contacto.crear_consulta("consulta2", "consulta2@gmail.com", "consulta2")
    contacto3 = contacto.crear_consulta("consulta3", "consulta3@gmail.com", "consulta3")


def cargar_diagnosticos():
    """
    Función que carga todos los diagnósticos que se deben mostrar en el sistema
    """
    jinetes_y_amazonas.crear_diagnostico(nombre="ECNE")
    jinetes_y_amazonas.crear_diagnostico(nombre="Lesión post traumática")
    jinetes_y_amazonas.crear_diagnostico(nombre="Mielomeningocele")
    jinetes_y_amazonas.crear_diagnostico(nombre="Esclerosis múltiple")
    jinetes_y_amazonas.crear_diagnostico(nombre="Escoliosis leve")
    jinetes_y_amazonas.crear_diagnostico(nombre="Secuelas de ACV")
    jinetes_y_amazonas.crear_diagnostico(nombre="Discapacidad intelectual")
    jinetes_y_amazonas.crear_diagnostico(
        nombre="Trastorno del espectro autista")
    jinetes_y_amazonas.crear_diagnostico(nombre="Trastorno del aprendizaje")
    jinetes_y_amazonas.crear_diagnostico(
        nombre="Trastorno por déficit de atención/hiperactividad")
    jinetes_y_amazonas.crear_diagnostico(nombre="Trastorno de la comunicación")
    jinetes_y_amazonas.crear_diagnostico(nombre="Trastorno de ansiedad")
    jinetes_y_amazonas.crear_diagnostico(nombre="Síndrome de Down")
    jinetes_y_amazonas.crear_diagnostico(nombre="Retraso madurativo")
    jinetes_y_amazonas.crear_diagnostico(nombre="Psicosis")
    jinetes_y_amazonas.crear_diagnostico(nombre="Trastorno de conducta")
    jinetes_y_amazonas.crear_diagnostico(
        nombre="Trastorno del ánimo y afectivos")
    jinetes_y_amazonas.crear_diagnostico(nombre="Trastorno alimentario")
    jinetes_y_amazonas.crear_diagnostico(nombre="Otro")


def cargar_dias():
    jinetes_y_amazonas.crear_dia(nombre="Lunes")
    jinetes_y_amazonas.crear_dia(nombre="Martes")
    jinetes_y_amazonas.crear_dia(nombre="Miércoles")
    jinetes_y_amazonas.crear_dia(nombre="Jueves")
    jinetes_y_amazonas.crear_dia(nombre="Viernes")
    jinetes_y_amazonas.crear_dia(nombre="Sábado")
    jinetes_y_amazonas.crear_dia(nombre="Domingo")


def cargar_tipos_de_discapacidad():
    jinetes_y_amazonas.crear_tipo_discapacidad(nombre="Mental")
    jinetes_y_amazonas.crear_tipo_discapacidad(nombre="Motora")
    jinetes_y_amazonas.crear_tipo_discapacidad(nombre="Sensorial")
    jinetes_y_amazonas.crear_tipo_discapacidad(nombre="Visceral")
