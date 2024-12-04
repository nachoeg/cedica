# Sistema CEDICA
Trabajo integrador de la materia Proyecto de Software en la Facultad de Informática de la UNLP.


## Información para probar el sistema

### Usuarios disponibles:
| Email                           | Contraseña        | Es admin | Roles
| --------------------------------| ------------------|----------|-------
| admin@mail.com&#8204;           | admin             | sí       | -
| admin2@mail.com&#8204;          | admin2            | sí       | -
| roles@mail.com&#8204;           | 4.roles           | no       | Administración. Técnica. Ecuestre. Voluntariado
| administracion@mail.com&#8204;  | administracion    | no       | Administración
| ecuestre@mail.com&#8204;        | ecuestre          | no       | Ecuestre
| tecnica@mail.com&#8204;         | tecnica           | no       | Técnica
| voluntariado@mail.com&#8204;    | voluntariado      | no       | Voluntariado
| edicion@mail.com&#8204;         | edicion           | no       | Edición
| sinroles@mail.com&#8204;        | sinroles          | no       | -


### Módulo cobros: 
    Al crear un cobro, se puede marcar si el J&A tiene deuda. 
    Con cada nuevo cobro que se le carga a un J&A, se tiene que volver a marcar si tiene deuda o no. Esta información se puede ver en el listado
    de J&A y en la visualización de cada J&A.

    La deuda del jinete o amazona no se carga desde el módulo de cobros sino desde el listado de Jinetes y Amazonas

### Listados:
    Los listados en el sistema se muestran en tablas. Los campos por los cuales se deben ordenar las filas de la tabla tienen, junto al encabezado de columna, 
    un botón con dos símbolos: ∧ (ascendente) y ∨ (descendente). El orden que está activado se muestra en color celeste. 
    Si ninguno de los símbolos se encuentra en color celeste, los elementos de la tabla
    se encuentran ordenados por id. Al hacer clic sobre el encabezado de columna, se activa en un principio el orden ascendente. Con el siguiente clic se activa el orden descendente. Con el tercer clic se vuelve al estado inicial (orden por id)

<br>

<h2 style="text-align:center;">Grupo 17</h2>

- Ignacio Escudero González
- Lea Agustina Mankowski Kochubey
- Matías Geringer
- Verónica Cao

### Informacion sobre la API:

    La API tienen dos endpoints:
    
    /api/articles (get)
    
    Este metodo devuelve los aritculos de forma pagina, tiene 5 parametros opcionales que pueden pasarse: 
        author: permite filtar por nombre de autor de la noticias.
        published_from y published_to: permiten filtrar por fecha de creacion, estas fechas deben de ser enviadas siguendo
        el formato iso.
        page: numero de pagina
        per_page: cantidad de elementos por pagina.
    /api/articles devuelve los elementos de forma paginada, por defecto page toma el valor de 1 y per_page de 6

    /api/message (post)

    Este metodo permite cargar una consulta en el sistema, en el cuerpo del post se le debe pasar 3 valors que son de caracter obligatorio:
        title: titulo de la consulta:
        message: mensaje de la consulta
        email: email de la persona que realizo la consulta

    Es importante, admeas, que el endpoint recibe un atirbuto captcha_token por segurdad, el cual es validado y debe de proveerse o dara codigo de erro 400. 

    /api/article (get)

    Este endpoint devuelve una noticifica cargada en el sistema, se el debe de pasar un id, valor que es de caracter obligatorio para realizar la consulta, de lo contrario dara error 400