<script>
import d3 from "d3";
import { schemeCategory10 } from "d3-scale-chromatic";
import { GChart } from "vue-google-charts";

export default {
  name: "PhylogeneticDistribution",
  components: {
    GChart
  },
  props: {
    filteredTable8Values: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      selectedDomain: "Bacteria"
    };
  },
  computed: {
    schemeCategory10: () => schemeCategory10,
    domainAndGroup() {
      var grouped = {};
      this.filteredTable8Values.forEach(table => {
        Object.entries(table).forEach(([key, value]) => {
          var [category, subCategory] = key.split(":").slice(-2);
          if (!(category in grouped)) {
            grouped[category] = {};
          }
          if (!(subCategory in grouped[category])) {
            grouped[category][subCategory] = 0;
          }
          grouped[category][subCategory] += value;
        });
      });
      // Object.values(grouped).forEach(group=>group.sort((a,b)=>a.))
      return grouped;
    },
    alpha() {
      var categoryWithCounts = Object.entries(this.domainAndGroup)
        .map(([category, subCategory]) => {
          return {
            category,
            count: Object.values(subCategory).reduce(
              (total, current) => total + current,
              0
            )
          };
        })
        .filter(({ count }) => count)
        .sort((a, b) => b.count - a.count);
      var scale = d3.scale
        .sqrt()
        .domain([
          Math.min(
            ...categoryWithCounts.map(
              categoryWithCount => categoryWithCount.count
            )
          ),
          Math.max(
            ...categoryWithCounts.map(
              categoryWithCount => categoryWithCount.count
            )
          )
        ])
        .range([5, 100]);
      return categoryWithCounts.map(categoryWithCount => ({
        ...categoryWithCount,
        scaledCount: scale(categoryWithCount.count)
      }));
    },
    sortedTopSelectedDomainChartData() {
      return [
        ["Group", "Count"],
        ...Object.entries(this.domainAndGroup[this.selectedDomain])
          .sort((a, b) => b[1] - a[1])
          .slice(0, 12)
      ];
    }
  },
  methods: {
    selectDomain(domain) {
      this.selectedDomain = domain;
    }
  }
};
</script>

<template>
  <v-card class="fill-height bordered ecosystem">
    <v-card-title>
      <h4>Phylogenetic Distribution</h4>
    </v-card-title>
    <v-card-text>
      <h5>Alpha diversity</h5>
      <div class="alpha-diversity-container">
        <v-tooltip
          top
          v-for="({ category, count, scaledCount }, i) in alpha"
          :key="category"
        >
          <template #activator="data">
            <div
              v-on="data.on"
              :class="{ selected: selectedDomain === category }"
              :style="{
                'flex-grow': scaledCount,
                'background-color': schemeCategory10[i]
              }"
              @mouseenter="selectDomain(category)"
            ></div>
          </template>
          <span>{{ category }}: {{ count | separator }}</span>
        </v-tooltip>
      </div>
      <div class="gchart-container">
        <GChart
          style="height: 100%;"
          type="PieChart"
          :data="sortedTopSelectedDomainChartData"
          :options="{
            chartArea: { width: '95%', height: '95%' },
            legend: { alignment: 'center' }
          }"
        />
      </div>
    </v-card-text>
  </v-card>
</template>

<style lang="scss" scoped>
.alpha-diversity-container {
  display: flex;
  height: 30px;

  .selected {
    border: 2px solid black;
  }
}

.v-card {
  display: flex;
  flex-direction: column;
  .v-card__text {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    .gchart-container {
      flex-grow: 1;
      padding: 10px;
    }
  }
}
</style>
