<template>
  <div class="grid grid-cols-4 gap-2 min-h-screen">
    <SideMenu />
    <div class="col-span-3">
      <NuxtPage />
    </div>
  </div>
</template>

<script setup>
import SideMenu from '~/components/SideMenu.vue';
</script>

<style scoped>
/* opcional: asegura que la altura ocupe toda la pantalla */
.min-h-screen {
  min-height: 100vh;
}
</style>
