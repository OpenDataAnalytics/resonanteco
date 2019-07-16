<script>
import _ from "lodash";
import d3 from 'd3';

import NavigationBar from "@/components/NavigationBar";
import SampleList from "@/components/SampleList";
import SamplesLocation from "@/components/SamplesLocation";
import PhylogeneticDistribution from "@/components/PhylogeneticDistribution";
import FunctionalDiversity from "@/components/FunctionalDiversity";
import MetagenomePropertiesTable from "@/components/MetagenomePropertiesTable";
import Sunburst from "@/components/Sunburst";
import { dataset } from "../util/dataLoader";

export default {
  name: "Home",
  components: {
    NavigationBar,
    SampleList,
    SamplesLocation,
    PhylogeneticDistribution,
    FunctionalDiversity,
    MetagenomePropertiesTable,
    Sunburst
  },
  data() {
    return {
      selectedSamples: [],
      sc10: d3.scale.category10()
    };
  },
  computed: {
    dataset: () => dataset,
    metaNames() {
      return dataset.meta.map(meta => meta["Genome Name / Sample Name"]);
    },
    sampleTypes() {
      var types = this.metaNames
        .map(name => {
          if (/soil/i.exec(name)) {
            return "Soil";
          } else if (/water/.exec(name)) {
            return "Water";
          } else if (/vegetation/.exec(name)) {
            return "Vegetation";
          }
        })
        .filter(value => value);
      return _.uniq(types);
    },
    ecosystems() {
      var types = this.metaNames
        .map(name => {
          if (/arctic/i.exec(name)) {
            return "Arctic";
          }
        })
        .filter(value => value);
      return _.uniq(types);
    },
    numberOfMetagenomes() {
      return dataset.meta.filter(meta => meta.Sequencing === "Metagenome")
        .length;
    },
    numberOfMetatranscriptomes() {
      return dataset.meta.filter(
        meta => meta.Sequencing === "Metatranscriptomes"
      ).length;
    },
    // deprecating
    filteredTablesValues() {
      if (!this.selectedSamples.length) {
        return {
          table7: Object.values(dataset.table7),
          table8: Object.values(dataset.table8),
          table9: Object.values(dataset.table9),
          summary: dataset.summary
        };
      } else {
        var tables = {};
        var selectedProjectIds = this.selectedSamples.map(
          project => project["taxon_oid"]
        );
        ["table7", "table8", "table9"].forEach(tableName => {
          tables[tableName] = Object.entries(dataset[tableName])
            .filter(([sampleId]) => selectedProjectIds.indexOf(sampleId) !== -1)
            .map(([, values]) => values);
        });
        tables["summary"] = dataset.summary.filter(
          summary => selectedProjectIds.indexOf(summary["taxon_oid"]) !== -1
        );
        return tables;
      }
    },
    filteredTables() {
      if (!this.selectedSamples.length) {
        return {
          meta: dataset.meta,
          summary: dataset.summary,
          table7: dataset.table7,
          table8: dataset.table8,
          table9: dataset.table9
        };
      } else {
        var tables = {};
        var selectedProjectIds = this.selectedSamples.map(
          project => project["taxon_oid"]
        );
        ["table7", "table8", "table9"].forEach(tableName => {
          tables[tableName] = Object.entries(dataset[tableName])
            .filter(([sampleId]) => selectedProjectIds.indexOf(sampleId) !== -1)
            .reduce((obj, [key, values]) => {
              obj[key] = values;
              return obj;
            }, {});
        });
        tables["meta"] = dataset.meta.filter(
          meta => selectedProjectIds.indexOf(meta["taxon_oid"]) !== -1
        );
        tables["summary"] = dataset.summary.filter(
          summary => selectedProjectIds.indexOf(summary.taxon_oid) !== -1
        );
        return tables;
      }
    },
    cmap() {
      return v => {
        if (v === "") {
          return "#ffffff";
        }
        return this.sc10(v);
      };
    }
  },
  methods: {}
};
</script>

<template>
  <v-content>
    <NavigationBar />
    <v-navigation-drawer app permanent clipped width="310">
      <SampleList :selectedSamples.sync="selectedSamples" />
    </v-navigation-drawer>
    <v-layout fill-height column>
      <v-flex shrink>
        <v-subheader>Summary</v-subheader>
        <v-container class="py-0 px-2" fluid grid-list-lg>
          <v-layout class="tile-row">
            <v-flex>
              <SamplesLocation />
            </v-flex>
            <v-flex>
              <v-card class="fill-height" color="teal darken-1" dark>
                <v-responsive :aspect-ratio="16 / 10">
                  <v-card-title>
                    <h3>Sample types</h3>
                  </v-card-title>
                  <v-card-text>
                    <h4>{{ sampleTypes.join(",") }}</h4>
                  </v-card-text>
                </v-responsive>
              </v-card>
            </v-flex>
            <v-flex>
              <v-card class="fill-height" color="blue-grey darken-1" dark>
                <v-card-title>
                  <h3>Ecosystems</h3>
                </v-card-title>
                <v-card-text>
                  <h4>{{ ecosystems.join(",") }}</h4>
                </v-card-text>
              </v-card>
            </v-flex>
            <!-- 4 -->
            <v-flex>
              <v-card class="fill-height" color="indigo darken-1" dark>
                <v-card-title>
                  <h3># metagenome</h3>
                </v-card-title>
                <v-card-text
                  ><h4>{{ numberOfMetagenomes }}</h4>
                </v-card-text>
              </v-card>
            </v-flex>
            <!-- 5 -->
            <v-flex>
              <v-card class="fill-height" color="orange darken-2" dark>
                <v-card-title>
                  <h3># Metatranscriptomes</h3>
                </v-card-title>
                <v-card-text>
                  <h4>{{ numberOfMetatranscriptomes }}</h4>
                </v-card-text>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-flex>
      <v-subheader class="mt-2">
        <template v-if="!selectedSamples.length">
          Across all projects and samples
        </template>
        <template v-else-if="selectedSamples.length === 1">
          {{ selectedSamples[0]["Genome Name / Sample Name"] }}
        </template>
        <template v-else>
          Multiple items
        </template>
      </v-subheader>
      <v-flex>
        <v-container class="py-0 px-2" fluid grid-list-lg fill-height>
          <v-layout class="tile-row">
            <v-flex>
              <v-card
                v-if="selectedSamples.length === 0"
                class="fill-height my-flex"
              >
                <v-card-title class="color-labeled grey lighten-3">
                  <div class="color-label orange darken-2"></div>
                  <h4>Metatranscriptome properties</h4>
                </v-card-title>
                <v-card-text> </v-card-text>
              </v-card>
              <v-card v-else class="fill-height my-flex">
                <v-card-title class="color-labeled grey lighten-3">
                  <div class="color-label cyan darken-1"></div>
                  <h4>Phylogenetic Distribution</h4>
                </v-card-title>
                <v-card-text class="white-card-text px-3 py-2">
                  <PhylogeneticDistribution
                    :filteredTablesValues="filteredTablesValues"
                    :cmap="cmap"
                /></v-card-text>
              </v-card>
            </v-flex>

            <v-flex>
              <v-card class="fill-height my-flex">
                <v-card-title class="color-labeled grey lighten-3">
                  <div class="color-label cyan darken-1"></div>
                  <h4>Sunburst</h4>
                </v-card-title>
                <v-card-text class="white-card-text">
                  <Sunburst
                    :filteredTablesValues="filteredTablesValues"
                    :cmap="cmap"
                  />
                </v-card-text>
              </v-card>
            </v-flex>

            <v-flex>
              <v-card
                v-if="selectedSamples.length === 0"
                class="fill-height my-flex"
              >
                <v-card-title class="color-labeled grey lighten-3">
                  <div class="color-label teal darken-1"></div>
                  <h4>Sample characteristics</h4>
                </v-card-title>
                <v-card-text> </v-card-text>
              </v-card>
              <v-card v-else class="fill-height my-flex">
                <v-card-title class="color-labeled grey lighten-3">
                  <div class="color-label teal darken-1"></div>
                  <h4>Functional Diversity</h4>
                </v-card-title>

                <v-card-text class="white-card-text pa-3">
                  <FunctionalDiversity
                    :filteredTable9Values="filteredTablesValues.table9"
                  />
                </v-card-text>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-flex>
      <v-subheader>
        Metagenome properties
      </v-subheader>
      <v-flex shrink>
        <v-container class="py-0 px-2" fluid grid-list-lg>
          <MetagenomePropertiesTable :filteredTables="filteredTables" />
        </v-container>
      </v-flex>
    </v-layout>
  </v-content>
</template>

<style lang="scss" scoped>
.v-navigation-drawer {
  display: flex;
  flex-direction: column;
}

.tile-row {
  .flex {
    flex-basis: 0;
    flex-shrink: 0;
  }
}

.v-card.my-flex {
  display: flex;
  flex-direction: column;

  .v-card__title.color-labeled {
    position: relative;
    overflow: hidden;
    padding: 14px 16px 14px 24px;

    div.color-label {
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 8px;
    }
  }

  .v-card__text {
    flex: 1;

    &.white-card-text {
      background: white;
      display: flex;
      flex-direction: column;
    }
  }
}
</style>
