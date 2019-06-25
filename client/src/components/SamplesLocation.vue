<script>
import _ from "lodash";

import { dataset } from "@/util/dataLoader";

export default {
  name: "SamplesLocation",

  async mounted() {
    setTimeout(() => {
      window.dispatchEvent(new Event("resize"));
      this.$refs.map.toGeoJSON(this.sitesFeature, {
        animate: 1000,
        bufferPercentage: 4
      });
    }, 0);
  },
  computed: {
    sitesFeature() {
      var grouped = _.groupBy(dataset.meta, sample => {
        return sample.Lat + sample.Long;
      });
      return {
        type: "FeatureCollection",
        features: Object.values(grouped).map(group => {
          return {
            type: "Feature",
            geometry: {
              type: "Point",
              coordinates: [parseFloat(group[0].Long), parseFloat(group[0].Lat)]
            },
            properties: {
              radius: 5 + 25 * (group.length / dataset.meta.length)
            }
          };
        })
      };
    }
  }
};
</script>

<template>
  <v-card>
    <GeojsMapViewport ref="map">
      <GeojsTileLayer
        url="https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png"
        attribution="© OpenStreetMap contributors, © CARTO"
        :zIndex="0"
      />
      <GeojsGeojsonLayer :zIndex="1" :geojson="sitesFeature" />
    </GeojsMapViewport>
  </v-card>
</template>

<style lang="scss" scoped>
.v-card {
  height: 100%;
}
</style>
