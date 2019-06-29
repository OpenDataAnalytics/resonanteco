<script>
import { schemeCategory10 } from "d3-scale-chromatic";
import { GChart } from "vue-google-charts";

export default {
  name: "FunctionalDiversity",
  components: {
    GChart
  },
  props: {
    filteredTable9Values: {
      type: Array,
      required: true
    }
  },
  computed: {
    chartData() {
      var aggregated = {};
      this.filteredTable9Values.forEach(values => {
        Object.entries(values).forEach(([key, count]) => {
          if (!(key in aggregated)) {
            aggregated[key] = 0;
          }
          aggregated[key] += count;
        });
      });
      return [
        ["Function", "Count", { role: "style" }],
        ...Object.entries(aggregated).map((values, i) => [
          ...values,
          schemeCategory10[i]
        ])
      ];
    }
  }
};
</script>

<template>
  <GChart
    style="height: 100%;"
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
