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
    filteredTablesValues: {
      type: Object,
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
    alphaDiversivty() {
      return this.filteredTablesValues.table7.reduce(
        (total, values) => values["Alpha Diversity"] + total,
        0
      );
    },
    domainAndGroup() {
      var grouped = {};
      this.filteredTablesValues.table8.forEach(table => {
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
    domain() {
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
  <div class="phylogenetic-distribution">
    <h5>Domains</h5>
    <div class="domain-diversity-container">
      <v-tooltip
        top
        v-for="({ category, count, scaledCount }, i) in domain"
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
    <h5 style="margin-top:5px;">
      Alpha diversity
      <div style="font-weight:normal;">{{ alphaDiversivty }}</div>
    </h5>
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
  </div>
</template>

<style lang="scss" scoped>
.phylogenetic-distribution {
  flex: 1;
  display: flex;
  flex-direction: column;

  .domain-diversity-container {
    display: flex;
    height: 27px;

    .selected {
      border: 2px solid black;
    }
  }

  .gchart-container {
    flex-grow: 1;
    padding: 10px;
  }
}
</style>
