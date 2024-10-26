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
| sinroles@mail.com&#8204;        | sinroles          | no       | -


### Módulo cobros: 
    Al crear un cobro, se puede marcar si el J&A tiene deuda. 
    Con cada nuevo cobro que se le carga a un J&A, se tiene que volver a marcar si tiene deuda o no. Esta información se puede ver en el listado
    de J&A y en la visualización de cada J&A.

    Con cada nuevo cobro cargado en el sistema, se sobreescribe el valor de la variable "tiene_deuda" de J&A, por lo que el valor válido
    siempre será el correspondiente al último cobro cargado (independientemente de la fecha de cobro que se haya ingresado al hacer el alta del cobro).

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