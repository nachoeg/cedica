<template>

<div class="max-w-[85rem] px-4 py-10 sm:px-6 lg:px-8 lg:py-14 mx-auto">
  <div class="relative p-6 md:p-16">
    <!-- Grilla -->
    <div class="relative z-10 lg:grid lg:grid-cols-12 lg:gap-5 ">
      <!-- Columna -->
      <div class="mb-10 lg:mb-0 lg:col-span-6 lg:col-start-8 lg:order-2">
        <h1 class="text-2xl font-bold sm:text-4xl dark:text-neutral-200 mt-5">
          Tareas que realizamos
        </h1>

        <!-- Navs botones -->
        <nav class="grid gap-4 mt-5 md:mt-10" aria-label="Tabs" role="tablist" aria-orientation="vertical">
          <button type="button" class="hs-tab-active:bg-white hs-tab-active:shadow-md hs-tab-active:hover:border-transparent text-start hover:bg-gray-200 focus:outline-none focus:bg-gray-200 p-4 md:p-5 rounded-xl dark:hs-tab-active:bg-neutral-900 dark:hover:bg-neutral-900 dark:focus:bg-neutral-900 active" id="tabs-with-card-item-1" aria-selected="true" data-hs-tab="#tabs-with-card-1" aria-controls="tabs-with-card-1" role="tab">
            <span class="flex gap-x-6 items-center">
              <svg class="shrink-0 size-6 md:size-7 hs-tab-active:text-[rgba(67,140,147,1)] text-gray-800 dark:hs-tab-active:text-[rgba(107,180,187,255)] dark:text-neutral-200" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="m11 17-5-5 5-5"/>
              <path d="m18 17-5-5 5-5"/>
              </svg>
              <span class="grow">
                <span class="text-lg font-semibold hs-tab-active:text-[rgba(67,140,147,1)] text-gray-800 dark:hs-tab-active:text-[rgba(107,180,187,255)] dark:text-neutral-200">Clases de Tacas/Equinoterapia</span>
              </span>
            </span>
          </button>

          <button type="button" class="hs-tab-active:bg-white hs-tab-active:shadow-md hs-tab-active:hover:border-transparent text-start hover:bg-gray-200 focus:outline-none focus:bg-gray-200 p-4 md:p-5 rounded-xl dark:hs-tab-active:bg-neutral-900 dark:hover:bg-neutral-900 dark:focus:bg-neutral-900" id="tabs-with-card-item-2" aria-selected="false" data-hs-tab="#tabs-with-card-2" aria-controls="tabs-with-card-2" role="tab">
            <span class="flex gap-x-6 items-center">
              <svg class="shrink-0 size-6 md:size-7 hs-tab-active:text-[rgba(67,140,147,1)] text-gray-800 dark:hs-tab-active:text-[rgba(107,180,187,255)] dark:text-neutral-200" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="m11 17-5-5 5-5"/>
              <path d="m18 17-5-5 5-5"/>
              </svg>
              <span class="grow">
                <span class="text-lg font-semibold hs-tab-active:text-[rgba(67,140,147,1)] text-gray-800 dark:hs-tab-active:text-[rgba(107,180,187,255)] dark:text-neutral-200">Cursos on line y presenciales</span>
              </span>
            </span>
          </button>

          <button type="button" class="hs-tab-active:bg-white hs-tab-active:shadow-md hs-tab-active:hover:border-transparent text-start hover:bg-gray-200 focus:outline-none focus:bg-gray-200 p-4 md:p-5 rounded-xl dark:hs-tab-active:bg-neutral-900 dark:hover:bg-neutral-900 dark:focus:bg-neutral-900" id="tabs-with-card-item-3" aria-selected="false" data-hs-tab="#tabs-with-card-3" aria-controls="tabs-with-card-3" role="tab">
            <span class="flex gap-x-6 items-center">
              <svg class="shrink-0 size-6 md:size-7 hs-tab-active:text-[rgba(67,140,147,1)] text-gray-800 dark:hs-tab-active:text-[rgba(107,180,187,255)] dark:text-neutral-200" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="m11 17-5-5 5-5"/>
              <path d="m18 17-5-5 5-5"/>
              </svg>
              <span class="grow">
                <span class="text-lg font-semibold hs-tab-active:text-[rgba(67,140,147,1)] text-gray-800 dark:hs-tab-active:text-[rgba(107,180,187,255)] dark:text-neutral-200">Desarrollo de tecnología adaptada</span>
              </span>
            </span>
          </button>
        </nav>
        <!-- Fin Nav botones -->
      </div>
      <!-- Fin Columna -->

      <!-- Columna -->
      <div class="lg:col-span-6 h-full">
        <div class="relative w-full h-full z-20">
          <!-- Tab Contenido -->
          <div class="w-full h-full">
            <div id="tabs-with-card-1" class="w-full h-full bg-white shadow-xl shadow-gray-200 rounded-xl dark:bg-transparent dark:shadow-gray-200/20 p-4 " role="tabpanel" aria-labelledby="tabs-with-card-item-1">
              <h2 class="text-xl text-gray-800 font-bold sm:text-3xl dark:text-neutral-200 pb-5">
                Clases de TACAs/Equinoterapia
              </h2>
              <p class="text-md sm:text-xl text-gray-600 text-justify dark:text-neutral-200">
                Nuestra principal actividad es ofrecer Terapias y Actividades Asistidas con Caballos/ Equinoterapia y deporte ecuestre adaptado.
                Contamos con un equipo de profesionales formados para brindar asistencia interdisciplinaria de calidad.
              </p>
              <p class="text-md sm:text-xl text-gray-600 text-justify dark:text-neutral-200">
                Desarrollamos un método específico para personas con discapacidades y bajos recursos que de otro modo no podrían afrontar los gastos de este tipo de terapia.
                 </p>
            </div>

            <div id="tabs-with-card-2" class="w-full h-full bg-white shadow-xl shadow-gray-200 rounded-xl dark:bg-transparent dark:shadow-gray-200/20 p-4 hidden" role="tabpanel" aria-labelledby="tabs-with-card-item-2">
              <h2 class="text-xl text-gray-800 font-bold sm:text-3xl dark:text-neutral-200 pb-5">
                Cursos on line y presenciales
              </h2>
              <p class="text-md sm:text-xl text-gray-600 text-justify dark:text-neutral-200">
                Uno de nuestros objetivos es brindar cursos y capacitaciones tanto a amazonas y jinetes como a los profesionales que los acompañan. A través de estos, se permite que las personas puedan adquirir distintas destrezas y habilidades prácticas, técnicas y teóricas.</p>
              <p class="text-md sm:text-xl text-gray-600 text-justify dark:text-neutral-200">
                Buscamos estimular la profesionalización de la práctica y el desarrollo de tareas específicas para la gestión eficaz de los diferentes centros de TACAs de nuestro país y Latinoamérica.</p>
              <p class="text-md sm:text-lg text-gray-600 text-justify dark:text-neutral-200 mt-3">
              Entre los cursos que hemos dictado en el último tiempo podemos mencionar:</p>
              <p class="text-md sm:text-lg italic text-gray-600 text-justify dark:text-neutral-200 ml-2 mt-1">
                · Clínica de Biomécanica de la PELVIS</p>
              <p class="text-md sm:text-md text-gray-600 text-justify dark:text-neutral-200 ml-2">
                Consistió en diversos ejercicios para mejorar y profundizar el asiento de amazonas y jinetes desde la conciencia de su propio cuerpo.</p>
              <p class="text-md sm:text-lg italic text-gray-600 text-justify dark:text-neutral-200 ml-2 mt-1">
                · Importancia del posicionamiento del paciente durante la monta gemela</p>
              <p class="text-md sm:text-md text-gray-600 text-justify dark:text-neutral-200 ml-2">
                Cuidados y recomendaciones, dictado durante la última jornada de actualización profesional en TACAs.</p>
            </div>

            <div id="tabs-with-card-3" class="w-full h-full bg-white shadow-xl shadow-gray-200 rounded-xl dark:bg-transparent dark:shadow-gray-200/20 p-4 hidden" role="tabpanel" aria-labelledby="tabs-with-card-item-3">
              <h2 class="text-xl text-gray-800 font-bold sm:text-3xl dark:text-neutral-200 pb-5">
                Desarrollo de tecnología adaptada
              </h2>
              <p class="text-md sm:text-xl text-gray-600 text-justify mr-2 dark:text-neutral-200">
                A lo largo de los años, hemos llevado a cabo la elaboración de distintos dispositivos y videojuegos adaptados que enriquezcan la experiencia de nuestra comunidad. 
              </p>
              <p class="text-md sm:text-xl text-gray-600 text-justify mr-2 dark:text-neutral-200">
                Algunos ejemplos son: eQUINO, Hermes, Aprendemos a Ensillar, Juego de la Memoria.</p>
              <p class="text-md sm:text-lg text-gray-600 text-justify mr-2 dark:text-neutral-200 mt-3">
                Te contamos sobre <strong>eQUINO</strong>:</p>
              <p class="text-md sm:text-lg text-gray-600 text-justify mr-2 dark:text-neutral-200 mt-1">
                Videojuego para la pandemia (nov 2020) este videojuego recrea en un entorno virtual, similar al real, las actividades que los alumnos realizan en una sesión de TACAS, haciendo que funcione como un complemento a la terapia y prolongando el estado de bienestar en los momentos en que los alumnos no pueden realizar la terapia de manera habitual.</p>
            </div>
          </div>
          <!-- Fin Tab Contenido -->

          <!-- SVG decor -->
          <div class="hidden absolute top-0 end-12 translate-x-20 -translate-y-9 md:block lg:translate-x-20">
            <svg class="w-12 h-auto text-[rgba(252,180,72,255)]" width="121" height="135" viewBox="0 0 121 135" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 16.4754C11.7688 27.4499 21.2452 57.3224 5 89.0164" stroke="currentColor" stroke-width="10" stroke-linecap="round"/>
              <path d="M33.6761 112.104C44.6984 98.1239 74.2618 57.6776 83.4821 5" stroke="currentColor" stroke-width="10" stroke-linecap="round"/>
              <path d="M50.5525 130C68.2064 127.495 110.731 117.541 116 78.0874" stroke="currentColor" stroke-width="10" stroke-linecap="round"/>
            </svg>
          </div>
          <!-- Fin SVG decor -->
        </div>
      </div>
      <!-- Fin Columna -->
    </div>
    <!-- Fin Grilla -->

    <!-- Color fondo -->
    <div class="absolute inset-0 grid grid-cols-12 size-full">
      <div class="col-span-full lg:col-span-7 lg:col-start-6 bg-gray-100 w-full h-5/6 rounded-xl sm:h-3/4 lg:h-full dark:bg-neutral-800"></div>
    </div>
    <!-- Fin Color fondo -->
  </div>
</div>

</template>

<script>
  export default {
    name: 'TareasComponent',
  }
</script>