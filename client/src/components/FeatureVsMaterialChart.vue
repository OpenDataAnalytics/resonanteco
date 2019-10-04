<script>
import * as d3 from "d3";

import { mapColor } from "@/util/colors";

export default {
  name: "FeatureVsMaterialChart",
  components: {},
  inject: ["girderRest"],
  props: {
    filter: {
      type: Object,
      required: false
    },
    featureSelections: {
      type: Array,
      required: false,
      default: () => []
    },
    materialSelections: {
      type: Array,
      required: false,
      default: () => []
    }
  },
  asyncComputed: {
    async records() {
      var params = {};
      if (this.filter) {
        params["filter"] = this.filter;
      }
      var { data: records } = await this.girderRest.get(
        "meta/feature_vs_material",
        { params }
      );
      records.sort((a, b) => (a.material > b.material ? 1 : -1));
      return [...records];
    }
  },
  watch: {
    records(value) {
      if (value) {
        this.initialize();
        this.update();
      }
    },
    featureSelections() {
      this.initialize();
      this.update();
    },
    materialSelections() {
      this.initialize();
      this.update();
    }
  },
  methods: {
    initialize() {
      var margin = { top: 70, right: 40, bottom: 70, left: 40 };
      var width = this.$el.clientWidth - margin.left - margin.right;
      this.width = width;
      var height = this.$el.clientHeight - margin.top - margin.bottom;
      this.height = height;

      d3.select(this.$el)
        .select("svg")
        .remove();

      var svg = d3
        .select(this.$el)
        .append("svg")
        .style("display", "block")
        .attr("width", this.$el.clientWidth)
        .attr("height", this.$el.clientHeight)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
      this.svg = svg;

      var x = d3
        .scaleBand()
        // .rangeRound([0, width])
        .rangeRound([0, Math.min(width, this.records.length * 80)])
        .padding(0.1);
      this.x = x;

      var y = d3.scaleLinear().rangeRound([height, 0]);
      this.y = y;
    },
    update() {
      var { records, svg, x, y, height } = this;
      x.domain(records.map((record, i) => i));
      y.domain([0, d3.max(records, record => record.count) + 5]);

      var topAxisGroup = svg
        .append("g")
        .call(d3.axisTop(x).tickFormat(d => records[d].feature));
      topAxisGroup
        .selectAll("text")
        .attr("class", "tick-label")
        .attr("y", -10)
        .attr("x", -10 * Math.tan((-30 * Math.PI) / 180))
        .attr("dy", ".35em")
        .attr("transform", "rotate(-30)")
        .style("text-anchor", "start")
        .classed(
          "selected",
          d => this.featureSelections.indexOf(records[d].feature) !== -1
        )
        .on("click", d => {
          var index = this.featureSelections.indexOf(records[d].feature);
          if (index !== -1) {
            var featureSelections = this.featureSelections.slice();
            featureSelections.splice(index, 1);
            this.$emit("update:featureSelections", featureSelections);
          } else {
            this.$emit("update:featureSelections", [
              ...this.featureSelections,
              records[d].feature
            ]);
          }
        })
        .append("title")
        .text(d => records[d].feature);
      topAxisGroup
        .append("text")
        .attr("fill", "#000")
        .attr("x", 20)
        .attr("y", -15)
        .attr("text-anchor", "end")
        .text("Feature");

      var bottomAxisGroup = svg
        .append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickFormat(d => records[d].material));
      bottomAxisGroup
        .selectAll("text")
        .attr("class", "tick-label")
        .attr("y", 10)
        .attr("x", 10 * Math.tan((30 * Math.PI) / 180))
        .attr("dy", ".35em")
        .attr("transform", "rotate(30)")
        .style("text-anchor", "start")
        .classed(
          "selected",
          d => this.materialSelections.indexOf(records[d].material) !== -1
        )
        .on("click", d => {
          var index = this.materialSelections.indexOf(records[d].material);
          if (index !== -1) {
            var materialSelections = this.materialSelections.slice();
            materialSelections.splice(index, 1);
            this.$emit("update:materialSelections", materialSelections);
          } else {
            this.$emit("update:materialSelections", [
              ...this.materialSelections,
              records[d].material
            ]);
          }
        })
        .append("title")
        .text(d => records[d].material);
      bottomAxisGroup
        .append("text")
        .attr("fill", "#000")
        .attr("x", 20)
        .attr("y", 20)
        .attr("text-anchor", "end")
        .text("Material");

      svg
        .append("g")
        .call(d3.axisLeft(y))
        .append("text")
        .attr("fill", "#000")
        .attr("transform", "rotate(-90)")
        .attr("y", -25)
        .attr("x", 10)
        .attr("dy", "0.71em")
        .attr("text-anchor", "end")
        .text("Count");

      var barContainer = svg
        .selectAll(".bar")
        .data(records, record => record.feature + record.material)
        .enter()
        .append("g")
        .attr("class", "bar-container")
        .attr(
          "transform",
          record => `translate(${x(records.indexOf(record))},0)`
        );

      barContainer
        .append("line")
        .attr("class", "indicator")
        .attr("x1", x.bandwidth() / 2)
        .attr("x2", x.bandwidth() / 2)
        .attr("y2", height);

      var bar = barContainer
        .append("rect")
        .attr("class", "bar")
        .attr("width", x.bandwidth())
        .attr("height", record => {
          return height - y(record.count);
        })
        .attr("y", record => {
          return y(record.count);
        })
        .attr("fill", d =>
          d3.interpolateRgb(
            mapColor("feature", d.feature),
            mapColor("material", d.material)
          )(0.5)
        )
        .attr("stroke", d =>
          this.featureSelections.indexOf(d.feature) !== -1 &&
          this.materialSelections.indexOf(d.material) !== -1
            ? "black"
            : "none"
        )
        .style(
          "transform-origin",
          record =>
            `${x.bandwidth() / 2}px ${y(record.count) +
              (height - y(record.count)) / 2}px`
        )
        .on("click", record => {
          var index = this.featureSelections.indexOf(record.feature);
          var index2 = this.materialSelections.indexOf(record.material);
          if (index !== -1 && index2 !== -1) {
            var featureSelections = this.featureSelections.slice();
            featureSelections.splice(index, 1);
            this.$emit("update:featureSelections", featureSelections);
          }
          if (index === -1) {
            this.$emit("update:featureSelections", [
              ...this.featureSelections,
              record.feature
            ]);
          }
          if (index !== -1 && index2 !== -1) {
            var materialSelections = this.materialSelections.slice();
            materialSelections.splice(index2, 1);
            this.$emit("update:materialSelections", materialSelections);
          }
          if (index2 === -1) {
            this.$emit("update:materialSelections", [
              ...this.materialSelections,
              record.material
            ]);
          }
        });

      bar.append("title").text(d => `${d.material} / ${d.feature}\n${d.count}`);
    },
    out() {
      console.log(arguments);
    }
  }
};
</script>

<template>
  <div class="feature-material-chart"></div>
</template>

<style lang="scss" scoped>
.feature-material-chart {
  height: 100%;
}
</style>

<style lang="scss">
.feature-material-chart {
  .bar-container {
    .indicator {
      visibility: hidden;
      fill: none;
      stroke: grey;
      stroke-dasharray: 3 5;
      stroke-width: 1;
    }

    &:hover {
      .indicator {
        visibility: visible;
      }
    }

    .bar {
      transition: transform 0.2s;
      stroke-width: 2px;

      &:hover {
        transform: scaleX(0.93) scaleY(0.98);
      }
    }
  }

  .tick-label {
    cursor: pointer;

    &.selected {
      font-weight: bolder;
      text-decoration: underline;
    }
  }
}
</style>
