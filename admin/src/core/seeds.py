from src.core import auth
from src.core import miembro

def run():
    user1 = auth.create_user(email="juan@mail.com", alias="Juan", activo=True)
    user2 = auth.create_user(email="jorge@mail.com", alias="Jorge", activo=False)
    user3 = auth.create_user(email="maria@mail.com", alias="Maria", activo=True)
    
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
