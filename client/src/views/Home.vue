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
          table9: Object.values(dataset.table9)
        };
      } else {
        return ["table7", "table8", "table9"].reduce((tables, tableName) => {
          tables[tableName] = Object.entries(dataset[tableName])
            .filter(
              ([sampleId]) =>
                this.selectedSamples
                  .map(project => project["taxon_oid"])
                  .indexOf(sampleId) !== -1
            )
            .map(([, values]) => values);
          return tables;
        }, {});
      }
    },
    MetagenomeProperties() {
      return ["GBp", "Number of features identified", "CDS", "rRNA"];
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
    <v-navigation-drawer app permanent clipped width="350">
      <v-subheader>Projects and samples</v-subheader>
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
              <v-card class="fill-height bordered sample">
                <v-responsive :aspect-ratio="1">
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
              <v-card class="fill-height bordered ecosystem">
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
              <v-card class="fill-height bordered metagenome">
                <v-card-title>
                  <h4># metagenome</h4>
                </v-card-title>
                <v-card-text>{{ numberOfMetagenomes }} </v-card-text>
              </v-card>
            </v-flex>
            <!-- 5 -->
            <v-flex>
              <v-card class="fill-height bordered metatranscriptome">
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
          All projects and samples
        </template>
        <template v-else-if="selectedSamples.length === 1">
          {{ selectedSamples[0]["Genome Name / Sample Name"] }}
        </template>
        <template v-else>
          Multiple
        </template>
      </v-subheader>
      <v-flex class="mb-5">
        <v-container class="py-0" fluid grid-list-lg fill-height>
          <v-layout class="tile-row">
            <v-flex>
              <v-card class="fill-height bordered metagenome">
                <v-card-title>
                  <h4>Metagenome properties</h4>
                </v-card-title>
                <v-card-text>
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
                  <v-list dense>
                    <v-list-tile
                      v-for="property of MetagenomeProperties"
                      :key="property"
                    >
                      <v-list-tile-content>{{ property }}</v-list-tile-content>
                      <v-list-tile-content class="align-end">{{
                        table7Sum(property) | numeral("0,0.[000]")
                      }}</v-list-tile-content>
                    </v-list-tile>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-flex>
            <v-flex>
              <v-card
                v-if="selectedSamples.length === 0"
                class="fill-height bordered metatranscriptome"
              >
                <v-card-title>
                  <h4>Metatranscriptome properties</h4>
                </v-card-title>
                <v-card-text> </v-card-text>
              </v-card>
              <PhylogeneticDistribution
                v-else
                :filteredTable8Values="filteredTablesValues.table8"
              />
            </v-flex>
            <v-flex>
              <v-card
                v-if="selectedSamples.length === 0"
                class="fill-height bordered sample"
              >
                <v-card-title>
                  <h4>Sample characteristics</h4>
                </v-card-title>
                <v-card-text> </v-card-text>
              </v-card>
              <FunctionalDiversity
                v-else
                :filteredTable9Values="filteredTablesValues.table9"
              />
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

  .v-list {
    flex: 1;
    overflow-y: auto;
  }
}
.tile-row {
  .flex {
    flex-basis: 0;
    flex-shrink: 0;
  }
}

.v-card.bordered {
  border-width: 2px;
  border-style: solid;

  &.sample {
    border-color: #7f7f7f;
  }

  &.ecosystem {
    border-color: #cb6c2b;
  }

  &.metagenome {
    border-color: #41719c;
  }

  &.metatranscriptome {
    border-color: #548235;
  }
}
</style>
