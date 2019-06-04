<script>
export default {
  name: "App",
  components: {},
  inject: ["girderRest"],
  computed: {},
  watch: {
    "girderRest.user"(user) {
      if (!user) {
        this.$router.push("/login");
      }
    }
  },
  methods: {}
};
</script>

<template>
  <v-app id="app">
    <keep-alive include="Home">
      <router-view />
    </keep-alive>
  </v-app>
</template>

<style lang="scss">
html {
  overflow-y: auto !important;
}
</style>
