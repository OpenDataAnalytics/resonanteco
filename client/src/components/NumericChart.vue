<script>
import * as d3 from "d3";
import _ from "lodash";

export default {
  name: "NumericChart",
  props: {
    records: {
      type: Array
    },
    max: {
      type: Number,
      default: null
    },
    min: {
      type: Number,
      default: null
    }
  },
  data: () => ({ sort: false }),
  computed: {
    records_() {
      if (!this.sort) {
        return this.records;
      } else {
        return _.orderBy(this.records, ["value"], ["desc"]);
      }
    }
  },
  watch: {
    records_(value) {
      if (value) {
        this.update();
      }
    }
  },
  mounted() {
    this.initialize();
    this.update();
  },
  methods: {
    initialize() {
      var margin = { top: 20, right: 30, bottom: 20, left: 60 };
      var { records } = this;
      var width = this.$el.clientWidth - margin.left - margin.right;
      this.width = width;
      var height = this.$el.clientHeight - margin.top - margin.bottom;
      this.height = height;

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
        .range([0, width])
        .padding(0.1);
      this.x = x;

      var y = d3.scaleLinear().rangeRound([height, 0]);
      this.y = y;
    },
    update() {
      var { records_: records, svg, x, y, height, width } = this;
      x.domain(records.map(record => record._id));
      y.domain([
        this.min ? this.min : d3.min(records, record => record.value),
        this.max ? this.max : d3.max(records, record => record.value)
      ]);

      svg.selectAll(".axes").remove();

      var xAxis = svg
        .append("g")
        .attr("class", "axes")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickValues([]))
        .append("text")
        .attr("fill", "#000")
        .attr("x", width)
        .attr("y", 20)
        .text("Records");

      svg
        .append("g")
        .attr("class", "axes")
        .call(d3.axisLeft(y))
        .append("text")
        .attr("fill", "#000")
        .attr("y", -10)
        .attr("x", 10)
        .text("Value");

      svg
        .selectAll(".bar")
        .data(records, record => record._id)
        .join(
          enter => {
            enter
              .append("rect")
              .attr("class", "bar")
              .attr("x", function(record) {
                return x(record._id);
              })
              .attr("y", height)
              .attr("width", x.bandwidth())
              .attr("height", 0)
              .transition()
              .duration(300)
              .attr("y", record => {
                return y(record.value);
              })
              .attr("height", record => {
                var h = height - y(record.value);
                return h < 0 ? 0 : h;
              });
          },
          update => {
            update
              .transition()
              .duration(300)
              .attr("x", function(record) {
                return x(record._id);
              })
              .attr("y", record => {
                return y(record.value);
              })
              .attr("width", x.bandwidth())
              .attr("height", record => {
                var h = height - y(record.value);
                return h < 0 ? 0 : h;
              });
          },
          remove => {
            remove
              .transition()
              .duration(300)
              .attr("height", 0)
              .attr("y", height)
              .remove();
          }
        );
    }
  }
};
</script>

<template>
  <div class="numeric-chart">
    <div class="sort-button" @click="sort=!sort"><span>{{sort?'unsort':'sort'}}</span></div>
  </div>
</template>

<style lang="scss" scoped>
.numeric-chart {
  height: 100%;
  position: relative;

  .sort-button {
    position: absolute;
    font-size: 12px;
    bottom: -2px;
    left: 18px;
    text-decoration: underline;
    width: 40px;
    text-align: center;
    cursor: pointer;
  }
}
</style>

<style lang="scss">
.numeric-chart {
  .bar {
    stroke: steelblue;
    fill: steelblue;
  }
}
</style>
