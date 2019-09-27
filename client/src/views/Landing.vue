<script>
import NavigationBar from "@/components/NavigationBar";
import SamplesLocation from "@/components/SamplesLocation";
import BiomeTreemap from "@/components/BiomeTreemap";
import FeatureVsMaterialChart from "@/components/FeatureVsMaterialChart";

export default {
  name: "Landing",
  components: {
    NavigationBar,
    SamplesLocation,
    BiomeTreemap,
    FeatureVsMaterialChart
  },
  data: () => ({
    selectedBiomes: [],
    selectedFeatures: [],
    selectedMaterials: [],
    filter: null,
    conditionChanged: false
  }),
  computed: {
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
  methods: {
    calculateFilter() {
      var filter = {};
      if (this.selectedBiomes.length) {
        filter["biome"] = this.selectedBiomes;
      }
      if (this.selectedFeatures.length) {
        filter["feature"] = this.selectedFeatures;
      }
      if (this.selectedMaterials.length) {
        filter["material"] = this.selectedMaterials;
      }
      if (Object.keys(filter).length !== 0) {
        return filter;
      }
      return null;
    },
    search() {
      this.filter = this.calculateFilter();
      this.conditionChanged = false;
    },
    clear() {
      this.selectedBiomes = [];
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
          <v-toolbar-title>Query</v-toolbar-title>
          <div class="flex-grow-1 ml-2">
            <template v-for="(values, key) in conditions">
              <v-chip
                close
                v-for="value in values"
                :key="key + value"
                class="ml-1"
                @click:close="
                  values.splice(values.indexOf(value), 1)
                "
                >{{ value }}</v-chip
              >
            </template>
          </div>
          <v-btn
            v-if="(conditionChanged && conditions) || (!conditions && !filter)"
            :disabled="!conditions"
            light
            small
            min-height="30"
            @click="search"
          >
            <v-icon left>mdi-magnify</v-icon>
            Search
          </v-btn>
          <v-btn
            v-if="filter && (!conditionChanged || !conditions)"
            light
            small
            min-height="30"
            @click="clear"
          >
            <v-icon left>mdi-delete</v-icon>
            Clear
          </v-btn>
        </v-toolbar>
      </v-col>
      <v-col
        ><v-row class="fill-height" no-gutters>
          <v-col>
            <v-row no-gutters class="flex-column fill-height">
              <v-col>
                <SamplesLocation :filter="filter" />
              </v-col>
              <v-col>
                <BiomeTreemap
                  :filter="filter"
                  :selections.sync="selectedBiomes"
                />
              </v-col>
            </v-row>
          </v-col>
          <v-col>
            <FeatureVsMaterialChart
              :filter="filter"
              :featureSelections.sync="selectedFeatures"
              :materialSelections.sync="selectedMaterials"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-content>
</template>
