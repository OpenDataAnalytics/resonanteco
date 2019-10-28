<script>
import * as d3 from "d3";

import { mapColor } from "@/util/colors";

export default {
  name: "SamplesLocation",
  inject: ["girderRest"],
  props: {
    filter: {
      type: Object,
      required: false
    },
    selectedRegion: {
      type: Object,
      required: false
    },
    readOnly:{
      type:Boolean
    }
  },
  data: () => ({
    annotationGeojson: null,
    editing: false
  }),
  computed: {
    sitesFeature() {
      if (!this.locations) {
        return null;
      }
      var counts = this.locations.map(location => location.count);
      var min = Math.min(...counts);
      var max = Math.max(...counts);
      return {
        type: "FeatureCollection",
        features: this.locations.map(location => {
          var colors = [
            ...location.features.map(feature => mapColor("feature", feature)),
            ...location.materials.map(material =>
              mapColor("material", material)
            ),
            ...location.biomes.map(biome => mapColor("biome", biome))
          ];
          // console.log();
          return {
            type: "Feature",
            geometry: {
              type: "Point",
              coordinates: [location.longitude, location.latitude]
            },
            properties: {
              radius: 3 + (location.count / (max - min)) * 30,
              fillColor: this.averageColor(colors).hex()
            }
          };
        })
      };
    }
  },
  asyncComputed: {
    async locations() {
      var params = {};
      if (this.filter) {
        params["filter"] = this.filter;
      }
      var { data: meta } = await this.girderRest.get("meta", { params });
      return meta.location;
    }
  },
  watch: {
    sitesFeature() {
      this.$refs.map.toGeoJSON(this.sitesFeature, {
        animate: 1000,
        bufferDistance: 20
      });
    },
    annotationGeojson(value) {
      if (value) {
        this.$emit("update:selectedRegion", value);
        this.geojson = value;
      }
      this.annotationGeojson = null;
    }
  },
  async mounted() {
    setTimeout(() => {
      window.dispatchEvent(new Event("resize"));
    }, 0);
  },
  methods: {
    averageColor(colors) {
      var colorList = colors.map(color => d3.color(color));
      return d3.rgb(
        colorList.map(color => color.r).reduce((a, b) => a + b, 0) /
          colorList.length,
        colorList.map(color => color.g).reduce((a, b) => a + b, 0) /
          colorList.length,
        colorList.map(color => color.b).reduce((a, b) => a + b, 0) /
          colorList.length
      );
    }
  }
};
</script>

<template>
  <GeojsMapViewport ref="map">
    <GeojsTileLayer
      url="https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png"
      attribution="© OpenStreetMap contributors, © CARTO"
      :zIndex="0"
    />
    <GeojsGeojsonLayer
      :zIndex="1"
      :geojson="sitesFeature"
      :featureStyle="{
        point: { stroke: false }
      }"
    />
    <GeojsGeojsonLayer
      :zIndex="2"
      :geojson="selectedRegion"
      :featureStyle="{
        polygon: { fill: false, strokeColor: 'black', strokeWidth: 2 }
      }"
    />
    <GeojsSimpleAnnotationLayer
      :zIndex="3"
      :geojson.sync="annotationGeojson"
      :editing.sync="editing"
    />
    <div v-if="!readOnly" class="draw">
      <v-btn
        fab
        small
        v-if="!selectedRegion"
        @mousedown.stop
        @click="editing = editing ? null : 'rectangle'"
      >
        <v-icon dark>{{
          editing ? "mdi-close" : "mdi-shape-rectangle-plus"
        }}</v-icon>
      </v-btn>
      <v-btn
        fab
        small
        v-if="selectedRegion"
        @mousedown.stop
        @click="$emit('update:selectedRegion', null)"
        ><v-icon dark>mdi-delete</v-icon>
      </v-btn>
    </div>
  </GeojsMapViewport>
</template>

<style lang="scss" scoped>
.draw {
  position: absolute;
  z-index: 2;
  left: 15px;
  top: 15px;
}
</style>
