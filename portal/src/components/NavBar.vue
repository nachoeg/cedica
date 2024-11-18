<script setup>
import IconHamburger from '@/components/icons/IconHamburger.vue'
import IconClose from '@/components/icons/IconClose.vue'
import { RouterLink } from 'vue-router'
</script>

<template>
  <header
    class="fixed z-50 flex flex-wrap sm:justify-start sm:flex-nowrap w-full bg-white/65 backdrop-blur-md dark:bg-neutral-800/65 text-sm py-2.5 border-b dark:border-neutral-700"
  >
    <nav
      class="max-w-[90rem] w-full mx-auto px-2 sm:px-5 lg:px-8 flex flex-wrap basis-full items-center justify-between"
    >
      <!-- Logo -->
      <RouterLink
        class="flex gap-1 text-xl font-semibold dark:text-white focus:outline-none focus:opacity-80"
        to="/"
      >
        <img src="@/assets/cedica-isotipo.webp" alt="cedica-logo" class="max-h-7" />
        <img
          src="@/assets/cedica-logotipo.webp"
          alt="cedica-logo"
          class="max-h-7 dark:brightness-200 dark:contrast-150"
        />
      </RouterLink>

      <!-- Hamburger Button -->
      <div class="flex items-center gap-x-2">
        <button
          type="button"
          class="sm:hidden hs-collapse-toggle btn btn-outline relative size-[34px]"
          id="hs-navbar-alignment-collapse"
          aria-expanded="false"
          aria-controls="hs-navbar-alignment"
          aria-label="Toggle navigation"
          data-hs-collapse="#hs-navbar-alignment"
        >
          <IconHamburger class="hs-collapse-open:hidden shrink-0 size-5"></IconHamburger>
          <IconClose class="hs-collapse-open:block hidden shrink-0 size-5"></IconClose>
          <span class="sr-only">Toggle</span>
        </button>
      </div>

      <!-- Links -->
      <div
        id="hs-navbar-alignment"
        class="hs-collapse hidden overflow-hidden transition-all duration-300 basis-full grow sm:grow-0 sm:basis-auto sm:block"
        aria-labelledby="hs-navbar-alignment-collapse"
      >
        <div
          class="flex flex-col gap-x-2 gap-y-3 mt-4 sm:flex-row sm:items-center sm:my-0 [&>*]:btn [&>*]:px-2 [&>*]:py-1.5 [&>*]:btn-outline [&>.router-link-active]:btn-secondary"
        >
          <RouterLink to="/contacto">Contacto</RouterLink>
          <RouterLink to="/noticias">Noticias</RouterLink>
        </div>
      </div>
    </nav>
  </header>

  <!-- Relleno para evitar que el contenido se oculte detrás del navbar -->
  <div class="h-14"></div>
</template>
