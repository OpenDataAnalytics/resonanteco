<script>
import { mapState, mapMutations } from "vuex";

import NavigationBar from "@/components/NavigationBar";
import Sunburst from "@/components/Sunburst";
import { calculateFilter } from "./utils";

export default {
  name: "Data",
  components: {
    NavigationBar,
    Sunburst
  },
  inject: ["girderRest"],
  data: function() {
    return {
      self: this,
      alphaDiversityRange: [null, null],
      options: {
        itemsPerPage: 10,
        page: 1
      }
    };
  },
  computed: {
    ...mapState([
      "selectedBiomes",
      "selectedFeatures",
      "selectedMaterials",
      "selectedRegion"
    ]),
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
      if (this.alphaDiversityRange[0] && this.alphaDiversityRange[1]) {
        filter["table7.Alpha Diversity"] = {
          $gt: this.alphaDiversityRange[0],
          $lt: this.alphaDiversityRange[1]
        };
      }
      return filter;
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
  created() {},
  methods: {
    ...mapMutations([
      "setSelectedBiomes",
      "setSelectedFeatures",
      "setSelectedMaterials",
      "setSelectedRegion"
    ]),
    capitalizeFirstLetter(value) {
      return value.charAt(0).toUpperCase() + value.slice(1);
    }
  }
};
</script>

<template>
  <v-content>
    <NavigationBar />
    <v-navigation-drawer app permanent dark width="300">
      <v-subheader>Filters</v-subheader>
      <v-expansion-panels accordion>
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
                {{self[`selected${capitalizeFirstLetter(category)}s_`].length}} selected
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
              :label="item"
              :value="item"
            ></v-checkbox>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>Properties</v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-range-slider
              class="two-line"
              :value="alphaDiversityRange"
              @change="alphaDiversityRange = $event"
              :max="11032"
              :min="6982"
              label="Alpha diversity"
              hide-details
            />
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-navigation-drawer>
    <div class="d-flex flex-column fill-height parent" no-gutters>
      <div class="children d-flex" style="flex-grow:1;">
        <Sunburst :filter="filter" />
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
  </v-content>
</template>

<style lang="scss">
.v-input__slider.two-line .v-input__slot {
  display: block;
}

.flex-column > [class*="col-"] {
  max-width: unset;
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
