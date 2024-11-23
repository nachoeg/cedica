<script setup>
import FooterLink from './FooterLink.vue'
import IconFacebook from './icons/IconFacebook.vue'
import IconInstagram from './icons/IconInstagram.vue'
import IconX from './icons/IconX.vue'
import IconWhatsapp from './icons/IconWhatsapp.vue'
import IconMail from './icons/IconMail.vue'
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
    <div class="flex gap-x-2 justify-center text-black dark:text-white">
      <FooterLink href="https://www.facebook.com/cedica.equitacionparatodos/">
        <IconFacebook class="size-6"></IconFacebook>
      </FooterLink>
      <FooterLink href="https://www.instagram.com/cedica.equitacionparatodos/">
        <IconInstagram class="size-6"></IconInstagram>
      </FooterLink>
      <FooterLink href="https://x.com/cedica_">
        <IconX class="size-6"></IconX>
      </FooterLink>
      <FooterLink href="https://web.whatsapp.com/send?phone=542215066291">
        <IconWhatsapp class="size-6"></IconWhatsapp>
      </FooterLink>
      <FooterLink href="mailto:equitacionparatodos@gmail.com">
        <IconMail class="size-6"></IconMail>
      </FooterLink>
    </div>
  </footer>
</template>
