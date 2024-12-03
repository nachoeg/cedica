<script setup>
import IconMoon from '@/components/icons/IconMoon.vue'
import IconSun from '@/components/icons/IconSun.vue'
</script>
<template>
  <div
    class="[&_button]:size-9 [&_button]:p-2 [&_button]:btn-outline [&_button]:border [&_button]:rounded-lg [&_button]:justify-center [&_button]:items-center"
  >
    <button
      type="button"
      class="hs-dark-mode-active:hidden inline-flex hs-dark-mode"
      data-hs-theme-click-value="dark"
    >
      <IconMoon class="shrink-0 size-4" />
    </button>
    <button
      type="button"
      class="hs-dark-mode-active:inline-flex hidden hs-dark-mode"
      data-hs-theme-click-value="light"
    >
      <IconSun class="shrink-0 size-4" />
    </button>
  </div>
</template>
