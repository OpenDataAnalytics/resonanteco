<script>
import { mapState, mapMutations } from "vuex";
import { isEmpty } from "lodash";

import NavigationBar from "@/components/NavigationBar";
import WidgetContainer from "@/components/WidgetContainer";
import SamplesLocation from "@/components/SamplesLocation";
import BiomeTreemap from "@/components/BiomeTreemap";
import FeatureVsMaterialChart from "@/components/FeatureVsMaterialChart";

import { calculateFilter } from "./utils";

export default {
  name: "Landing",
  components: {
    NavigationBar,
    WidgetContainer,
    SamplesLocation,
    BiomeTreemap,
    FeatureVsMaterialChart
  },
  data: () => ({
    filter: null,
    conditionChanged: false
  }),
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
    selectedRegion_: {
      get() {
        return this.selectedRegion;
      },
      set(values) {
        this.setSelectedRegion(values);
      }
    },
    conditions() {
      var conditions = {};
      if (this.selectedBiomes.length) {
        conditions.selectedBiomes = this.selectedBiomes;
      }
      if (this.selectedFeatures.length) {
        conditions.selectedFeatures = this.selectedFeatures;
      }
      if (this.selectedMaterials.length) {
        conditions.selectedMaterials = this.selectedMaterials;
      }
      return Object.keys(conditions).length ? conditions : null;
    }
  },
  watch: {
    conditions() {
      this.conditionChanged = true;
    }
  },
  created() {
    this.filter = calculateFilter(this);
  },
  methods: {
    isEmpty,
    ...mapMutations([
      "setSelectedBiomes",
      "setSelectedFeatures",
      "setSelectedMaterials",
      "setSelectedRegion"
    ]),
    search() {
      this.filter = calculateFilter(this);
      this.conditionChanged = false;
    },
    clear() {
      this.selectedBiomes_ = [];
      this.selectedFeatures_ = [];
      this.selectedMaterials_ = [];
      this.selectedRegion_ = null;
      this.filter = null;
      this.conditionChanged = false;
    }
  }
};
</script>

<template>
  <v-content>
    <NavigationBar />
    <v-row class="flex-column fill-height" no-gutters>
      <v-col class="flex-grow-0">
        <v-toolbar dense flat dark>
          <v-toolbar-title>Filter</v-toolbar-title>
          <div class="flex-grow-1 ml-2">
            <v-chip
              close
              v-if="selectedRegion_"
              @click:close="selectedRegion_ = null"
            >
              Selected Region
            </v-chip>
            <template v-for="(values, key) in conditions">
              <v-chip
                close
                v-for="value in values"
                :key="key + value"
                class="ml-1"
                @click:close="values.splice(values.indexOf(value), 1)"
              >
                {{ value }}
              </v-chip>
            </template>
          </div>
          <v-btn
            v-if="
              (conditionChanged && conditions) ||
                (!conditions && isEmpty(filter))
            "
            light
            small
            min-height="30"
            @click="search"
          >
            <v-icon left>mdi-magnify</v-icon>
            Search
          </v-btn>
          <template
            v-if="!isEmpty(filter) && (!conditionChanged || !conditions)"
          >
            <v-btn light small min-height="30" @click="clear">
              <v-icon left>mdi-delete</v-icon>
              Clear
            </v-btn>
            <v-btn class="ml-2" light small min-height="30" to="/data">
              Go to Data
              <v-icon right>mdi-arrow-right-bold</v-icon>
            </v-btn>
          </template>
        </v-toolbar>
      </v-col>
      <v-col
        ><v-row class="fill-height" no-gutters>
          <v-col>
            <v-row no-gutters class="flex-column fill-height">
              <v-col>
                <WidgetContainer>
                  <template #title>
                    Locations
                  </template>
                  <SamplesLocation
                    :filter="filter"
                    :selectedRegion.sync="selectedRegion_"
                  />
                </WidgetContainer>
              </v-col>
              <v-col>
                <WidgetContainer>
                  <template #title>
                    Biomes
                  </template>
                  <BiomeTreemap
                    :filter="filter"
                    :selections.sync="selectedBiomes_"
                  />
                </WidgetContainer>
              </v-col>
            </v-row>
          </v-col>
          <v-col>
            <WidgetContainer>
              <template #title>
                Features & Materials
              </template>
              <FeatureVsMaterialChart
                :filter="filter"
                :featureSelections.sync="selectedFeatures_"
                :materialSelections.sync="selectedMaterials_"
              />
            </WidgetContainer>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-content>
</template>
