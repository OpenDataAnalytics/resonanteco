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
  <v-toolbar app clipped-left dense>
    <v-toolbar-title>
      <v-tooltip open-delay="2000" bottom>
        <template #activator="{ on }">
          <span v-on="on">ResonantEco</span>
        </template>
        <span>v{{ version }}</span>
      </v-tooltip>
    </v-toolbar-title>
    <v-tabs class="navigation-tabs ml-3" color="transparent">
      <v-tab to="/">
        Explore
      </v-tab>
    </v-tabs>
    <v-spacer></v-spacer>
    <UserButton @user="girderRest.logout()" />
  </v-toolbar>
</template>

<style lang="scss">
.v-toolbar .navigation-tabs.v-tabs {
  width: unset;

  .v-tabs__container--icons-and-text .v-tabs__div {
    min-width: 120px;
  }
}
</style>
