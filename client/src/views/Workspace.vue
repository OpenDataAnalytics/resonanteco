<script>
import { mapState, mapMutations } from "vuex";

import NavigationBar from "@/components/NavigationBar";
import PhylogeneticDistribution from "@/components/PhylogeneticDistribution";
import FunctionalDiversity from "@/components/FunctionalDiversity";
// import AddFilter from "@/components/AddFilter";
// import { calculateFilter } from "./utils";
// import additionalFilterProperties from "@/components/additionalFilterProperties";

export default {
  name: "Workspace",
  components: {
    NavigationBar,
    PhylogeneticDistribution,
    FunctionalDiversity
  },
  inject: ["girderRest"],
  data: function() {
    return {
      selectedWorkspaceId: null,
      options: {
        itemsPerPage: 15,
        page: 1
      }
    };
  },
  computed: {
    ...mapState([]),
    selectedWorkspace() {
      if (!this.workspaces) {
        return null;
      }
      return this.workspaces.find(
        workspace => workspace._id === this.selectedWorkspaceId
      );
    },
    panelIndex: {
      get() {
        return this.selectedWorkspace
          ? this.workspaces.indexOf(this.selectedWorkspace)
          : null;
      },
      set(index) {
        if (index === undefined) {
          this.selectedWorkspaceId = null;
        } else {
          this.options.page = 1;
          this.selectedWorkspaceId = this.workspaces[index]._id;
        }
      }
    },
    filter() {
      if (!this.selectedWorkspace) {
        return null;
      }
      return { _id: this.selectedWorkspace.meta.datasets };
    }
  },
  asyncComputed: {
    async workspaces() {
      var { data: workspaces } = await this.girderRest.get("workspace");
      return workspaces;
    },
    async records() {
      if (!this.selectedWorkspace) {
        return null;
      }
      var { data: records } = await this.girderRest.get("record/filtered", {
        params: {
          fields: JSON.stringify(["meta.name"]),
          filter: this.filter,
          skip: (this.options.page - 1) * this.options.itemsPerPage,
          limit: this.options.itemsPerPage
        }
      });
      return Object.freeze(records);
    }
  },
  watch: {
    selectedWorkspace(workspace) {
      this.$router.replace(
        workspace ? `/workspace/${workspace._id}` : "/workspace"
      );
    }
  },
  async created() {
    var { workspaceId } = this.$route.params;
    this.selectedWorkspaceId = workspaceId;
  },
  methods: {
    ...mapMutations([]),
    async deleteWorkspace(workspace) {
      var result = await this.$prompt({
        title: "Confirm",
        text: "Do you want to delete this workspace?",
        positiveButton: "Confirm",
        negativeButton: "Cancel",
        confirm: true //show negative button
      });
      if (result) {
        await this.girderRest.delete(`workspace/${workspace._id}`);
        this.workspaces.splice(this.workspaces.indexOf(workspace), 1);
      }
    }
  }
};
</script>

<template>
  <v-content class="data">
    <NavigationBar />
    <v-navigation-drawer permanent app clipped dark width="300">
      <v-subheader>Workspaces</v-subheader>
      <v-expansion-panels accordion v-model="panelIndex">
        <v-expansion-panel v-for="workspace in workspaces" :key="workspace._id">
          <v-expansion-panel-header>
            {{ workspace._id }}
            <v-spacer /><v-btn
              text
              icon
              x-small
              class="flex-grow-0"
              @click.stop="deleteWorkspace(workspace)"
              ><v-icon>mdi-close</v-icon></v-btn
            >
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-select
              outlined
              dense
              :items="['algorithm A', 'algorithm B']"
              label="Choose Algorithm"
              hide-details
            ></v-select>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-navigation-drawer>

    <v-row class="fill-height" no-gutters>
      <template v-if="selectedWorkspace">
        <v-col>
          <v-row class="flex-column fill-height pa-2" no-gutters>
            <v-col>
              <PhylogeneticDistribution v-if="filter" :filter="filter" />
            </v-col>
            <v-col>
              <FunctionalDiversity v-if="filter" :filter="filter" />
            </v-col>
          </v-row>
        </v-col>
        <v-col>
          <div
            class="children table-container"
            style="flex-grow:2;min-height:0;"
          >
            <v-data-table
              v-if="records"
              height="100%"
              :headers="[
                { text: 'ID', value: '_id', sortable: false },
                { text: 'Name', value: 'meta.name', sortable: false }
              ]"
              :items="records.data"
              :server-items-length="records.count"
              :options.sync="options"
              :loading="$asyncComputed.records.updating"
            >
            </v-data-table>
          </div>
        </v-col>
      </template>
      <div v-else class="flex-grow-1 align-self-center text-center">
        Select a workspace
      </div>
    </v-row>
  </v-content>
</template>

<style lang="scss">
.v-input__slider.two-line .v-input__slot {
  display: block;
}

.flex-column > [class*="col-"] {
  max-width: unset;
}

.data .sample-location-container {
  .v-expansion-panel-content__wrap {
    padding: 0;
    height: 200px;
  }
}
</style>

<style lang="scss" scoped>
.table-container {
  height: 100%;

  .v-data-table {
    height: calc(100% - 60px);
  }
}
</style>
