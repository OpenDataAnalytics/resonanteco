<script>
import * as d3 from "d3";
import { GChart } from "vue-google-charts";

export default {
  name: "FunctionalDiversity",
  components: {
    GChart
  },
  inject: ["girderRest"],
  props: {
    filter: {
      type: Object,
      required: false
    }
  },
  computed: {
    chartData() {
      if (!this.table9Data) {
        return null;
      }
      var aggregated = {};
      this.table9Data.forEach(values => {
        Object.entries(values)
          .filter(([key]) => key !== "_id" && key !== "taxon_oid")
          .forEach(([key, count]) => {
            if (!(key in aggregated)) {
              aggregated[key] = 0;
            }
            aggregated[key] += count;
          });
      });
      var colors = d3.schemeCategory10;
      return [
        ["Function", "Count", { role: "style" }],
        ...Object.entries(aggregated).map((values, i) => [...values, colors[i]])
      ];
    }
  },
  asyncComputed: {
    async table9Data() {
      var { data: records } = await this.girderRest.get("record/filtered", {
        params: {
          fields: JSON.stringify(["table9"]),
          filter: this.filter
        }
      });
      return records.data.map(record => record.table9).filter(d => d);
    }
  }
};
</script>

<template>
  <GChart
    v-if="chartData"
    style="height: 95%;"
    type="BarChart"
    :data="chartData"
    :options="{
      chartArea: { width: '70%', height: '85%', right: 0 },
      legend: 'none'
    }"
  />
</template>

<style lang="scss" scoped>
.v-card {
  display: flex;
  flex-direction: column;
  .v-card__text {
    flex-grow: 1;
  }
}
</style>
