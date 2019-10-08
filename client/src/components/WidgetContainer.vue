<template functional>
  <div class="widget-container">
    <div class="grey darken-2 white--text body-2 pl-2">
      <slot name="title"></slot>
    </div>
    <div class="widget flex-grow-1">
      <slot />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.widget-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}
</style>
