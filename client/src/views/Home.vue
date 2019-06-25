<script>
import { intersectionBy } from "lodash";

import NavigationBar from "@/components/NavigationBar";
import { Upload as GirderUpload } from "@girder/components/src/components";
import MetaUploader from "@/util/MetaUploader";

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
    filteredItems() {
      if (!this.itemsByGeometryFilter) {
        return this.itemsByFilenameFilter ? this.itemsByFilenameFilter : [];
      } else if (!this.itemsByFilenameFilter) {
        return this.itemsByGeometryFilter ? this.itemsByGeometryFilter : [];
      }
      return intersectionBy(
        this.itemsByGeometryFilter,
        this.itemsByFilenameFilter,
        "_id"
      );
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
    itemsByGeometryFilter: {
      default: null,
      async get() {
        var geometry = this.filterGeometry;
        if (!geometry) {
          return null;
        }
        var { data: items } = await this.girderRest.get("item/geometa", {
          params: {
            geojson: geometry,
            relation: "within"
          }
        });
        return items;
      }
    },
    itemsByFilenameFilter: {
      default: null,
      async get() {
        var filename = this.filterFilename;
        if (!filename) {
          return null;
        }
        var { data: items } = await this.girderRest.get("item", {
          params: {
            text: filename
          }
        });
        return items;
      }
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
    },
    filteredItems(value, oldValue) {
      if (value.length && !oldValue.length) {
        this.showResultPanel = true;
      } else if (
        !this.filterGeometry &&
        !this.filterFilename &&
        !value.length &&
        oldValue.length
      ) {
        this.showResultPanel = false;
      }
    }
  },
  mounted() {
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
    }
  }
};
</script>

<template>
  <v-content>
    <NavigationBar />
    <v-container fill-height fluid class="pa-0">
      <v-layout fill-height>
        <v-flex style="position: relative; flex-grow:5;">
          <v-speed-dial
            :top="true"
            :left="true"
            direction="bottom"
            open-on-hover
            absolute
            style="top:40px;">
            <template v-slot:activator>
              <v-btn
                color="primary"
                dark
                fab
              >
                <v-icon>add</v-icon>
              </v-btn>
            </template>
            <v-btn fab dark 
              color="orange" small @click="regionFilterClick">
              <v-icon>mdi-vector-rectangle</v-icon>
            </v-btn>
            <v-btn
              fab
              dark
              small
              color="green"
              @click="filenameDialog=true"
            >
              <v-icon>mdi-format-text-variant</v-icon>
            </v-btn>
          </v-speed-dial>
          <v-btn fab small absolute left color="primary" style="bottom: 20px;" @click="uploadDialog=true">
            <v-icon>mdi-file-upload</v-icon>
          </v-btn>
          <div style="position:absolute; top: 20px; left: 100px; z-index: 1;">
            <v-chip close v-if="this.filterGeometry" color="light-blue" dark @input="removeFilter('filterGeometry')">Region</v-chip>
            <v-chip close v-if="this.filterFilename" color="light-blue" dark @input="removeFilter('filterFilename')">{{this.filterFilename}}</v-chip>
          </div>
          <v-btn fab small absolute right color="primary" style="top: 20px;" @click="showResultPanel=!showResultPanel">
            <v-badge color="green" :value="filteredItems.length">
              <template #badge>
                <span>{{filteredItems.length}}</span>
              </template>
              <v-icon>mdi-table-of-contents</v-icon>
            </v-badge>
          </v-btn>
          <GeojsMapViewport
            class="map"
            :viewport="viewport"
            ref="map">
            <GeojsTileLayer
            url="https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png"
            attribution="© OpenStreetMap contributors, © CARTO"
            :zIndex="0" />
            <GeojsGeojsonLayer
              :zIndex="1"
              :geojson="filterGeometry"
            />
            <GeojsSimpleAnnotationLayer
              v-if="editing"
              :zIndex="2"
              :editing="editing"
              :geojson.sync="geojson"
            />
          </GeojsMapViewport>
        </v-flex>
        <v-flex style="flex-grow:3; flex-basis: 0; min-width: 0;" v-if="showResultPanel">
          <v-data-table
            :headers="resultTableHeaders"
            :items="filteredItems"
            :pagination.sync="pagination"
            :rows-per-page-items="[5,10,15]">
            <template v-slot:items="{item}">
              <td><router-link :to="`/item/${item._id}`">{{ item.meta._id }}</router-link></td>
              <td class="text-xs-right">{{ item.meta.file_name }}</td>
            </template>
          </v-data-table>
        </v-flex>
      </v-layout>
    </v-container>
    <v-dialog v-if="dataFolder" v-model="uploadDialog" full-width max-width="500px">
      <GirderUpload
        :dest="dataFolder"
        :uploadCls="MetaUploader"
        :multiple="false"
        accept=".json"
        ref="girderUpload"
        @postUpload="uploadDialog=false"
      />
    </v-dialog>
    <v-dialog v-model="filenameDialog" full-width max-width="300px">
      <v-card>
        <v-form @submit.prevent='addFilenameFilter'>
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
            <v-btn
              type="submit"
              color="primary"
            >
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
</style>
