<script>
export default {
  name: "SamplesLocation",
  inject: ["girderRest"],
  props: {
    filter: {
      type: Object,
      required: false
    }
  },
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
          return {
            type: "Feature",
            geometry: {
              type: "Point",
              coordinates: [
                parseFloat(location.longitude),
                parseFloat(location.latitude)
              ]
            },
            properties: {
              radius: 3 + (location.count / (max - min)) * 30
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
        bufferPercentage: 4
      });
    }
  },
  async mounted() {
    setTimeout(() => {
      window.dispatchEvent(new Event("resize"));
    }, 0);
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
    <GeojsGeojsonLayer :zIndex="1" :geojson="sitesFeature" />
  </GeojsMapViewport>
</template>

<style lang="scss" scoped>
.v-card {
  height: 100%;
}
</style>
