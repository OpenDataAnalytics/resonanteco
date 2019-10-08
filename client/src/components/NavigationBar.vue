<script>
import { mapState } from "vuex";

import UserButton from "@/components/girder/UserButton";

export default {
  name: "NavigationBar",
  components: {
    UserButton
  },
  inject: ["girderRest"],
  computed: {
    ...mapState(["currentItemId"]),
    version() {
      return process.env.VERSION;
    }
  },
  methods: {}
};
</script>

<template>
  <v-app-bar app>
    <v-toolbar-title>
      <v-tooltip open-delay="2000" bottom>
        <template #activator="{ on }">
          <span v-on="on">ResonantEco</span>
        </template>
        <span>v{{ version }}</span>
      </v-tooltip>
    </v-toolbar-title>
    <v-tabs class="navigation-tabs" right icons-and-text>
      <v-tab to="/">
        Home
        <v-icon>mdi-home</v-icon>
      </v-tab>
      <v-tab to="/data">
        Data
        <v-icon>mdi-chart-donut</v-icon>
      </v-tab>
      <v-tab to="/workspace">
        Workspaces
        <v-icon>mdi-sitemap</v-icon>
      </v-tab>
      <v-tab to="/analysis">
        Analysis
        <v-icon>mdi-chart-timeline-variant</v-icon>
      </v-tab>
    </v-tabs>
    <UserButton @user="girderRest.logout()" />
  </v-app-bar>
</template>

<style lang="scss">
.v-toolbar .navigation-tabs.v-tabs {
  width: unset;

  .v-tabs__container--icons-and-text .v-tabs__div {
    min-width: 120px;
  }
}
</style>
