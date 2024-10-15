from src.core import cobros, jinetes_y_amazonas
from src.core.seeds_usuarios import cargar_usuarios

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

def run():

    cargar_usuarios()

    cargar_diagnosticos()

    j_y_a1= jinetes_y_amazonas.crear_j_o_a(nombre="Victor", apellido="Varela" , dni=32454245, edad= 32, fecha_nacimiento='1992/09/10 13:19:38', provincia_nacimiento='Buenos Aires', localidad_nacimiento='La Plata', domicilio_actual='32',telefono_actual=2214563564, contacto_emer_nombre='Alejo',contacto_emer_telefono=2214678864)
    j_y_a2= jinetes_y_amazonas.crear_j_o_a(nombre="Valeria", apellido="Vazquez", dni= 14234221, edad= 32, fecha_nacimiento='1992/09/10 13:19:38', provincia_nacimiento='La Pampa', localidad_nacimiento='Santa Rosa', domicilio_actual='32 n12',telefono_actual=2214569764, contacto_emer_nombre='Alvaro',contacto_emer_telefono=2214678864)
    j_y_a3= jinetes_y_amazonas.crear_j_o_a(nombre="Veronica", apellido="Vim", dni=12456786, edad= 32, fecha_nacimiento='1992/09/10 13:19:38', provincia_nacimiento='Tierra del Fuego', localidad_nacimiento='Ushuaia', domicilio_actual='32',telefono_actual=2215663564, contacto_emer_nombre='Alma',contacto_emer_telefono=2214677864)    
    cobro1 = cobros.crear_cobro(medio_de_pago='efectivo', fecha_pago = '2024/09/10 13:19:38',monto=400, observaciones="Nada para agregar", joa_id=j_y_a1.id)
    cobro2 = cobros.crear_cobro(medio_de_pago='credito', fecha_pago = '2024/09/12 13:19:38', monto=500, observaciones="Queda al día",joa_id=j_y_a1.id)
    cobro3 = cobros.crear_cobro(medio_de_pago='debito', fecha_pago = '2024/09/11 13:19:38', monto=600, observaciones="-",joa_id=j_y_a3.id)