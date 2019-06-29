<script>
import _ from "lodash";

import NavigationBar from "@/components/NavigationBar";
import SampleList from "@/components/SampleList";
import SamplesLocation from "@/components/SamplesLocation";
import PhylogeneticDistribution from "@/components/PhylogeneticDistribution";
import FunctionalDiversity from "@/components/FunctionalDiversity";
import { dataset } from "../util/dataLoader";
console.log(dataset);

export default {
  name: "Home",
  components: {
    NavigationBar,
    SampleList,
    SamplesLocation,
    PhylogeneticDistribution,
    FunctionalDiversity
  },
  data() {
    return {
      selectedSamples: []
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
          summary => selectedProjectIds.indexOf(summary.taxon_oid) !== -1
        );
        return tables;
      }
    },
    metagenomeProperties() {
      return ["GBp", "Number of features identified", "CDS", "rRNA"];
    },
    gcNumbers() {
      if (this.filteredTablesValues.summary.length === 1) {
        return this.filteredTablesValues.summary[0].GC;
      } else {
        var gcNumbers = this.filteredTablesValues.summary.map(summary =>
          parseFloat(summary.GC)
        );
        var min = Math.min(...gcNumbers);
        var max = Math.max(...gcNumbers);
        var mean = _.mean(gcNumbers);
        return { min, max, mean };
      }
    }
  },
  methods: {
    table7Sum(property) {
      return _.sum(
        this.filteredTablesValues.table7.map(values => values[property])
      );
    }
  }
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
        <v-container class="py-0" fluid grid-list-lg>
          <v-layout class="tile-row">
            <v-flex>
              <SamplesLocation />
            </v-flex>
            <v-flex>
              <v-card class="fill-height" color="teal darken-1" dark>
                <v-responsive :aspect-ratio="16 / 10">
                  <v-card-title>
                    <h4>Sample types</h4>
                  </v-card-title>
                  <v-card-text>
                    {{ sampleTypes.join(",") }}
                  </v-card-text>
                </v-responsive>
              </v-card>
            </v-flex>
            <v-flex>
              <v-card class="fill-height" color="blue-grey darken-1" dark>
                <v-card-title>
                  <h4>Ecosystems</h4>
                </v-card-title>
                <v-card-text>
                  {{ ecosystems.join(",") }}
                </v-card-text>
              </v-card>
            </v-flex>
            <!-- 4 -->
            <v-flex>
              <v-card class="fill-height" color="indigo darken-1" dark>
                <v-card-title>
                  <h4># metagenome</h4>
                </v-card-title>
                <v-card-text>{{ numberOfMetagenomes }} </v-card-text>
              </v-card>
            </v-flex>
            <!-- 5 -->
            <v-flex>
              <v-card class="fill-height" color="orange darken-2" dark>
                <v-card-title>
                  <h4># Metatranscriptomes</h4>
                </v-card-title>
                <v-card-text>
                  {{ numberOfMetatranscriptomes }}
                </v-card-text>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-flex>
      <v-subheader class="mt-4">
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
      <v-flex class="mb-5">
        <v-container class="py-0" fluid grid-list-lg fill-height>
          <v-layout class="tile-row">
            <v-flex>
              <v-card class="fill-height my-flex">
                <v-card-title class="indigo darken-1 my-dark">
                  <h4>Metagenome properties</h4>
                </v-card-title>
                <v-card-text class="white-card-text theme--light">
                  <h5>
                    <template v-if="!selectedSamples.length">
                      Total
                    </template>
                    <template v-else-if="selectedSamples.length === 1">
                      Single
                    </template>
                    <template v-else>
                      Sum
                    </template>
                  </h5>
                  <v-list dense light>
                    <v-list-tile
                      v-for="property of metagenomeProperties"
                      :key="property"
                    >
                      <v-list-tile-content>{{ property }}</v-list-tile-content>
                      <v-list-tile-content class="align-end">{{
                        table7Sum(property) | numeral("0,0.[000]")
                      }}</v-list-tile-content>
                    </v-list-tile>
                    <v-list-tile>
                      <v-list-tile-content>GC</v-list-tile-content>
                      <v-list-tile-content class="align-end">
                        <template v-if="typeof gcNumbers === 'string'">
                          {{ gcNumbers | numeral("0.[00]") }}%
                        </template>
                        <template v-else>
                          {{ gcNumbers.min | numeral("0.[00]") }}% ~
                          {{ gcNumbers.max | numeral("0.[00]") }}% ({{
                            gcNumbers.mean | numeral("0.[00]")
                          }}%)
                        </template>
                      </v-list-tile-content>
                    </v-list-tile>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-flex>
            <v-flex>
              <v-card
                v-if="selectedSamples.length === 0"
                class="fill-height my-flex"
              >
                <v-card-title class="orange darken-2 my-dark">
                  <h4>Metatranscriptome properties</h4>
                </v-card-title>
                <v-card-text> </v-card-text>
              </v-card>
              <v-card v-else class="fill-height my-flex">
                <v-card-title class="cyan darken-1 my-dark">
                  <h4>Phylogenetic Distribution</h4>
                </v-card-title>
                <v-card-text class="white-card-text">
                  <PhylogeneticDistribution
                    :filteredTablesValues="filteredTablesValues"
                /></v-card-text>
              </v-card>
            </v-flex>
            <v-flex>
              <v-card
                v-if="selectedSamples.length === 0"
                class="fill-height my-flex"
              >
                <v-card-title class="teal darken-1 my-dark">
                  <h4>Sample characteristics</h4>
                </v-card-title>
                <v-card-text> </v-card-text>
              </v-card>
              <v-card v-else class="fill-height my-flex">
                <v-card-title class="blue-grey darken-1 my-dark">
                  <h4>Functional Diversity</h4>
                </v-card-title>

                <v-card-text class="white-card-text">
                  <FunctionalDiversity
                    :filteredTable9Values="filteredTablesValues.table9"
                  />
                </v-card-text>
              </v-card>
            </v-flex>
          </v-layout>
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

  .v-card__title.my-dark {
    color: white;
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
