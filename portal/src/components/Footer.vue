<script setup>
import FooterLink from './FooterLink.vue'
import IconFacebook from './icons/IconFacebook.vue'
import IconInstagram from './icons/IconInstagram.vue'
import IconX from './icons/IconX.vue'
</script>

<script>
export default {
  name: 'FooterComponent',
}
</script>

<template>
  <footer class="text-center mt-auto w-full py-10 px-4 sm:px-6 lg:px-8 space-y-2">
    <a
      class="flex-none text-xl font-semibold text-black dark:text-white"
      href="#"
      aria-label="Cedica"
      >Cedica</a
    >

    <p class="text-gray-500 dark:text-neutral-500">
      © {{ new Date().getFullYear() }} Todos los derechos reservados.
    </p>

    <!-- Redes sociales -->
    <div class="space-x-2 text-black dark:text-white">
      <FooterLink href="https://www.facebook.com/cedica.equitacionparatodos/">
        <IconFacebook class="size-5 stroke-2"></IconFacebook>
      </FooterLink>
      <FooterLink href="https://www.instagram.com/cedica.equitacionparatodos/">
        <IconInstagram class="size-5"></IconInstagram>
      </FooterLink>
      <FooterLink href="https://x.com/cedica_">
        <IconX class="size-5"></IconX>
      </FooterLink>
    </div>
  </footer>
</template>
