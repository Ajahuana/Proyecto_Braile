<template>
  <div>
    <el-menu default-active="2">
        <el-menu-item index="1">
          <NuxtLink :to="`/`"><span>Inicio</span></NuxtLink>
        </el-menu-item>
        <el-menu-item index="2">
          <NuxtLink :to="`/transcripcion`"><span>Transcripcion</span></NuxtLink>
        </el-menu-item>
        <el-menu-item index="3">
          <NuxtLink :to="`/imprimir`"><span>Impresion</span></NuxtLink>
        </el-menu-item>
        <el-menu-item index="4">
          <NuxtLink :to="`/libreria`"><span>Biblioteca</span></NuxtLink>
          <span></span>
        </el-menu-item>
        <el-menu-item index="5">
          <NuxtLink :to="`/`"><span>Importar documentos</span></NuxtLink>
          <span></span>
        </el-menu-item>
      </el-menu>
  </div>
</template>

<script lang="ts" setup>
  const index = ref('1');
</script>
