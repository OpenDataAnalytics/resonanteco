<script>
import * as d3 from "d3";
import { GChart } from "vue-google-charts";

export default {
  name: "PhylogeneticDistribution",
  components: {
    GChart
  },
  inject: ["girderRest"],
  props: {
    filter: {
      type: Object,
      required: false
    }
    // filteredTables: {
    //   type: Object,
    //   required: true
    // },
    // cmap: {
    //   required: true
    // }
  },
  data() {
    return {
      selectedDomain: "Bacteria"
    };
  },
  computed: {
    alphaDiversivty() {
      return null;
      // return this.filteredTables.table7.reduce(
      //   (total, values) => values["Alpha Diversity"] + total,
      //   0
      // );
    },
    domainAndGroup() {
      if (!this.tableData) {
        return null;
      }
      var grouped = {};
      this.tableData.forEach(table => {
        Object.entries(table).forEach(([key, value]) => {
          var [category, subCategory] = key.split(":").slice(-2);
          if (!category || !subCategory) {
            return;
          }
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
      var scale = d3
        .scaleSqrt()
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
      if (!this.domainAndGroup) {
        return null;
      }
      return [
        ["Group", "Count"],
        ...Object.entries(this.domainAndGroup[this.selectedDomain])
          .sort((a, b) => b[1] - a[1])
          .slice(0, 12)
      ];
    },
    sortedTopSelectedDomainChartColors() {
      if (!this.sortedTopSelectedDomainChartData) {
        return null;
      }
      return this.sortedTopSelectedDomainChartData
        .slice(1)
        .map(d => d[0])
        .map(this.cmap);
    },
    gChartOptions() {
      if (!this.sortedTopSelectedDomainChartColors) {
        return null;
      }
      return {
        chartArea: { width: "95%", height: "95%" },
        legend: { alignment: "center" },
        colors: this.sortedTopSelectedDomainChartColors
      };
    },
    sc10() {
      return d3.scaleOrdinal().range(d3.schemeCategory10);
    },
    cmap() {
      return v => {
        if (v === "") {
          return "#ffffff";
        }
        return this.sc10(v);
      };
    }
  },
  asyncComputed: {
    async tableData() {
      var { data: records } = await this.girderRest.get("record/filtered", {
        params: {
          fields: JSON.stringify(["table8"]),
          filter: this.filter
        }
      });
      return records.data.map(record => record.table8).filter(d => d);
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
  <div class="phylogenetic-distribution" v-if="domainAndGroup">
    <h5>Domains</h5>
    <div class="domain-diversity-container mx-5">
      <v-tooltip
        top
        v-for="{ category, count, scaledCount } in domain"
        :key="category"
      >
        <template #activator="data">
          <div
            v-on="data.on"
            :class="{ selected: selectedDomain === category }"
            :style="{
              'flex-grow': scaledCount,
              'background-color': cmap(category)
            }"
            @mouseenter="selectDomain(category)"
          ></div>
        </template>
        <span>{{ category }}: {{ count | separator }}</span>
      </v-tooltip>
    </div>
    <div class="bottom">
      <div class="gchart-container">
        <GChart
          style="height: 100%;"
          type="PieChart"
          :data="sortedTopSelectedDomainChartData"
          :options="gChartOptions"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.phylogenetic-distribution {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: white;

  .domain-diversity-container {
    display: flex;
    height: 27px;

    .selected {
      border: 2px solid black;
    }
  }

  .bottom {
    flex: 1;
    display: flex;

    .alpha-diversity-container {
      position: absolute;
      margin-top: 5px;
      z-index: 1;
    }

    .gchart-container {
      flex-grow: 1;
      padding: 10px;
    }
  }
}
</style>
