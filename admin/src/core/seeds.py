from src.core import auth, cobros


def run():
    user1 = auth.create_user(email="juan@mail.com", alias="Juan", activo=True)
    user2 = auth.create_user(email="jorge@mail.com", alias="Jorge", activo=False)
    user3 = auth.create_user(email="maria@mail.com", alias="Maria", activo=True)
    cobro1 = cobros.crear_cobro(medio_de_pago='efectivo', fecha_pago = '2024/09/10 13:19:38',monto=400, observaciones="Nada para agregar")
    cobro2 = cobros.crear_cobro(medio_de_pago='credito', fecha_pago = '2024/09/12 13:19:38', monto=500, observaciones="Queda al día")
    cobro3 = cobros.crear_cobro(medio_de_pago='debito', fecha_pago = '2024/09/11 13:19:38', monto=600, observaciones="-")