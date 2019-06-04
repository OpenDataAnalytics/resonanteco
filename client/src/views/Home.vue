<script>
import { intersectionBy } from "lodash";

import NavigationBar from "@/components/NavigationBar";
import { Upload as GirderUpload } from "@girder/components/src/components";
import MetaUploader from "@/util/MetaUploader";

import eventAggregator from "../util/eventAggregator";

export default {
  name: "Home",
  components: {
    NavigationBar,
    GirderUpload
  },
  inject: ["girderRest"],
  data() {
    return {
      viewport: {
        center: [-100, 30],
        zoom: 4
      },
      uploadDialog: false,
      editing: null,
      geojson: null,
      filenameDialog: false,
      filename: "",
      filterGeometry: null,
      filterFilename: null,
      siteData: null,
      showResultPanel: false,
      pagination: {
        page: 1,
        rowsPerPage: 15
      }
    };
  },
  computed: {
    resultTableHeaders() {
      return [
        {
          text: "Id",
          align: "left",
          sortable: false,
          value: "meta._id"
        },
        { text: "Filename", value: "meta.file_name" }
      ];
    },
    sitesFeature() {
      var sites = this.sites;
      if (!this.sites) {
        return;
      }
      var counts = sites.map(site => site.count);
      var range = Math.max(...counts) - Math.min(...counts);
      return {
        type: "FeatureCollection",
        features: sites.map(site => {
          return {
            type: "Feature",
            geometry: site.location,
            properties: {
              radius: 5 + (25 * site.count) / range,
              name: site.name
            }
          };
        })
      };
    }
  },
  asyncComputed: {
    async dataFolder() {
      var collection = (await this.girderRest.get("collection", {
        params: {
          text: "ResonantEco"
        }
      })).data[0];
      if (collection) {
        return (await this.girderRest.get("folder", {
          params: {
            parentId: collection._id,
            parentType: "collection"
          }
        })).data[0];
      }
    },
    async sites() {
      var { data: datasets } = await this.girderRest.get("site");
      return datasets;
    }
  },
  watch: {
    geojson(value) {
      if (value) {
        this.filterGeometry = this.geojson.geometry;
        this.editing = null;
        this.geojson = null;
      }
    },
    filterGeometry(value) {
      if (value) {
      }
    },
    showResultPanel() {
      this.$nextTick(() => {
        window.dispatchEvent(new Event("resize"));
      }, 100);
    }
  },
  created() {
    this.featuresClicked = eventAggregator(this.featuresClicked);
  },
  async mounted() {
    setTimeout(() => {
      window.dispatchEvent(new Event("resize"));
      window.dispatchEvent(new Event("resize"));
    }, 0);
  },
  methods: {
    MetaUploader,
    regionFilterClick() {
      if (!this.editing) {
        this.editing = "rectangle";
      } else {
        this.editing = null;
      }
    },
    addFilenameFilter() {
      this.filterFilename = this.filename;
      this.filename = "";
      this.filenameDialog = false;
    },
    removeFilter(filterName) {
      this[filterName] = null;
    },
    featuresClicked(events) {
      var events = events.map(event => event[0]);
      var geo = events[0].mouse.geo;
      this.siteData = {
        position: [geo.x, geo.y],
        features: events.map(({ data }) => data)
      };
    },
    closeSitesDialog() {
      this.siteData = null;
    },
    log() {
      console.log("123");
    }
  }
};
</script>

<template>
  <v-content>
    <NavigationBar />
    <v-container fill-height fluid class="pa-0">
      <v-layout fill-height>
        <v-flex style="position: relative;">
          <v-btn
            fab
            small
            absolute
            left
            color="primary"
            style="bottom: 20px;"
            @click="uploadDialog = true"
          >
            <v-icon>mdi-file-upload</v-icon>
          </v-btn>
          <GeojsMapViewport
            class="map"
            :viewport="viewport"
            ref="map"
            @click="closeSitesDialog"
          >
            <GeojsTileLayer
              url="https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png"
              attribution="© OpenStreetMap contributors, © CARTO"
              :zIndex="0"
            />
            <GeojsGeojsonLayer
              :zIndex="1"
              :geojson="sitesFeature"
              @feature-click="featuresClicked"
            />
            <GeojsWidgetLayer
              :zIndex="2"
              v-if="siteData"
              :position="siteData.position"
            >
              <v-card @mousedown.native.stop>
                <v-toolbar card color="white">
                  <v-toolbar-title>Sites</v-toolbar-title>
                  <v-spacer></v-spacer>
                  <v-btn icon @click="closeSitesDialog">
                    <v-icon>close</v-icon>
                  </v-btn>
                </v-toolbar>
                <v-card-text class="site-content pt-0">
                  <v-list-tile
                    class="site-link"
                    v-for="(feature, i) in siteData.features"
                    :key="i"
                    :to="`site/${feature.properties.name}`"
                    color="primary"
                  >
                    <v-list-tile-content>
                      <v-list-tile-title>{{
                        feature.properties.name
                      }}</v-list-tile-title>
                    </v-list-tile-content>
                  </v-list-tile>
                </v-card-text>
              </v-card>
            </GeojsWidgetLayer>
          </GeojsMapViewport>
        </v-flex>
      </v-layout>
    </v-container>
    <v-dialog
      v-if="dataFolder"
      v-model="uploadDialog"
      full-width
      max-width="500px"
    >
      <GirderUpload
        :dest="dataFolder"
        :uploadCls="MetaUploader"
        :multiple="false"
        accept=".json"
        ref="girderUpload"
        @postUpload="uploadDialog = false"
      />
    </v-dialog>
    <v-dialog v-model="filenameDialog" full-width max-width="300px">
      <v-card>
        <v-form @submit.prevent="addFilenameFilter">
          <v-card-title class="headline">
            Filter by file_name
          </v-card-title>
          <v-card-text>
            <v-text-field
              label="name"
              v-model="filename"
              browser-autocomplete="on"
              name="resonanteco_file_name"
            ></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn type="submit" color="primary">
              Add
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>
  </v-content>
</template>

<style lang="scss">
.v-badge__badge {
  top: -15px;
  font-size: 12px;
}

.site-content {
  width: 300px;
}

.site-link:hover {
  text-decoration: underline;
}
</style>
