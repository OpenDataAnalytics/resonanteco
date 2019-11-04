<script>
import { mapState, mapMutations } from "vuex";

import NavigationBar from "@/components/NavigationBar";
import SamplesLocation from "@/components/SamplesLocation";
import DataInsight from "@/components/DataInsight";
import AddFilter from "@/components/AddFilter";
import { calculateFilter } from "./utils";
import additionalFilterProperties from "@/components/additionalFilterProperties";

export default {
  name: "Data",
  components: {
    NavigationBar,
    DataInsight,
    SamplesLocation,
    AddFilter
  },
  inject: ["girderRest"],
  data: function() {
    return {
      self: this,
      additionalFilterProperties,
      additionalFilters: {},
      options: {
        itemsPerPage: 10,
        page: 1
      },
      addFilterDialog: false,
      inputWorkspaceName: false,
      workspaceName: ""
    };
  },
  computed: {
    ...mapState([
      "selectedBiomes",
      "selectedFeatures",
      "selectedMaterials",
      "selectedRegion"
    ]),
    selectedRegion_: {
      get() {
        return this.selectedRegion;
      },
      set(values) {
        this.setSelectedRegion(values);
      }
    },
    selectedBiomes_: {
      get() {
        return this.selectedBiomes;
      },
      set(values) {
        this.setSelectedBiomes(values);
      }
    },
    selectedFeatures_: {
      get() {
        return this.selectedFeatures;
      },
      set(values) {
        this.setSelectedFeatures(values);
      }
    },
    selectedMaterials_: {
      get() {
        return this.selectedMaterials;
      },
      set(values) {
        this.setSelectedMaterials(values);
      }
    },
    filter() {
      var filter = calculateFilter(this);
      return { ...filter, ...this.additionalFilters };
    }
  },
  asyncComputed: {
    async distinct() {
      var { data: categoryValues } = await this.girderRest.get("meta/distinct");
      return Object.freeze(categoryValues);
    },
    async records() {
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
  methods: {
    ...mapMutations([
      "setSelectedBiomes",
      "setSelectedFeatures",
      "setSelectedMaterials",
      "setSelectedRegion"
    ]),
    capitalizeFirstLetter(value) {
      return value.charAt(0).toUpperCase() + value.slice(1);
    },
    addFilter(filter) {
      this.additionalFilters = { ...this.additionalFilters, ...filter };
      this.addFilterDialog = false;
    },
    removeAdditionalFilter(property) {
      this.$delete(this.additionalFilters, property);
    },
    async createWorkspace() {
      if (!this.workspaceName) {
        return;
      }
      var { data: records } = await this.girderRest.get("record/filtered", {
        params: {
          fields: JSON.stringify(["1"]),
          filter: this.filter
        }
      });
      var { data: workspace } = await this.girderRest.post("workspace", {
        name: this.workspaceName,
        datasets: records.data.map(record => record._id),
        filter: this.filter
      });
      this.$router.push(`/workspace/${workspace._id}`);
    }
  }
};
</script>

<template>
  <v-content class="data">
    <NavigationBar />
    <v-navigation-drawer app permanent clipped dark width="360">
      <v-subheader
        >Filters<v-spacer /><v-btn
          outlined
          small
          @click="addFilterDialog = true"
          :filter="filter"
          >Add</v-btn
        ></v-subheader
      >
      <v-expansion-panels accordion>
        <v-expansion-panel>
          <v-expansion-panel-header>Location</v-expansion-panel-header>
          <v-expansion-panel-content class="sample-location-container">
            <SamplesLocation
              :filter="filter"
              :selectedRegion.sync="selectedRegion_"
            />
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel
          v-for="(values, category) in this.distinct"
          :key="category"
        >
          <v-expansion-panel-header>
            <div>
              <div>{{ capitalizeFirstLetter(category) }}</div>
              <div
                v-if="
                  self[`selected${capitalizeFirstLetter(category)}s_`].length
                "
                class="panel-header-caption grey--text"
              >
                {{
                  self[`selected${capitalizeFirstLetter(category)}s_`].length
                }}
                selected
              </div>
            </div>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-checkbox
              class="mt-1"
              dense
              hide-details
              v-for="item in values"
              :key="item"
              v-model="self[`selected${capitalizeFirstLetter(category)}s_`]"
              :label="String(item)"
              :value="item"
            ></v-checkbox>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel
          v-for="(value, property) in additionalFilters"
          :key="property"
        >
          <v-expansion-panel-header
            >{{
              additionalFilterProperties.find(
                ({ value, text }) => value === property
              ).text
            }}<v-spacer /><v-btn
              text
              icon
              x-small
              class="flex-grow-0"
              @click.stop="removeAdditionalFilter(property)"
              ><v-icon>mdi-close</v-icon></v-btn
            ></v-expansion-panel-header
          >
          <v-expansion-panel-content>
            {{ value.gt }} ~ {{ value.lt }}
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-navigation-drawer>
    <div class="d-flex flex-column fill-height parent" no-gutters>
      <v-toolbar class="flex-grow-0" dense flat dark>
        <v-spacer />
        <v-btn
          v-if="!inputWorkspaceName"
          small
          min-height="30"
          :disabled="!records || !records.count || records.count > 100"
          @click="inputWorkspaceName = true"
        >
          <div><div>Create workspace</div><div style="font-size: 80%;    text-transform: initial;">with filtered data</div></div>
        </v-btn>
        <div v-else style="width: 300px;">
          <v-text-field
            dense
            hide-details
            v-model="workspaceName"
            placeholder="Workspace name"
            append-outer-icon="mdi-check"
            @click:append-outer="createWorkspace"
          ></v-text-field>
        </div>
      </v-toolbar>
      <div class="children" style="flex-grow:1;">
        <DataInsight :filter="filter" />
      </div>
      <div class="children table-container" style="flex-grow:2;min-height:0;">
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
    </div>
    <v-dialog v-model="addFilterDialog" max-width="1200">
      <AddFilter :visible="addFilterDialog" :filter="filter" @add="addFilter" />
    </v-dialog>
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
.parent {
  .children {
    flex-shrink: 0;
    flex-basis: 0;

    &.table-container {
      height: 100%;

      .v-data-table {
        height: calc(100% - 60px);
      }
    }
  }
}

.panel-header-caption {
  font-size: 12px;
  margin-top: 5px;
}
</style>
