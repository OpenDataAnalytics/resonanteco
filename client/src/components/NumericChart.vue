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
    },
    rangeSelection: {
      type: Boolean,
      default: false
    },
    mean: {
      type: Number,
      required: false
    },
    median: {
      type: Number,
      required: false
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
    },
    guidelines() {
      var lines = [];
      if (this.mean) {
        lines.push({
          name: "Mean",
          value: this.mean
        });
      }
      if (this.median) {
        lines.push({
          name: "Median",
          value: this.median,
          strokeDasharray: "6, 2"
        });
      }
      return lines;
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
      var width = this.$el.clientWidth - margin.left - margin.right;
      this.width = width;
      var height = this.$el.clientHeight - margin.top - margin.bottom;
      this.height = height;

      var svg = d3
        .select(this.$el)
        .append("svg")
        .style("display", "block")
        // .attr("viewBox", `0.5 0.5 ${this.$el.clientWidth} ${this.$el.clientHeight}`)
        .attr("width", this.$el.clientWidth)
        .attr("height", this.$el.clientHeight)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      this.svg = svg;

      var tooltip = d3
        .select(this.$el)
        .append("div")
        .attr("class", "tooltip")
        .style("display", "none");

      var workRegion = svg.append("g");
      this.workRegion = workRegion;

      var barContainer = workRegion.append("g");
      this.barContainer = barContainer;

      var rangeOverlay = workRegion
        .append("rect")
        .attr("class", "range-overlay");

      workRegion
        .append("rect")
        .attr("width", width)
        .attr("height", height)
        .attr("fill", "transparent");

      workRegion.on("mousemove", () => {
        clearTimeout(this.tooltipHandle);
        var { offsetX, offsetY } = d3.event;
        tooltip.style("display", "none");
        var value = y.invert(offsetY - margin.top);
        this.tooltipHandle = setTimeout(() => {
          tooltip
            .style("left", offsetX + 18 + "px")
            .style("top", offsetY + "px")
            .text(y.tickFormat()(value))
            .style("display", "block");
        }, 300);

        if (dragging) {
          rangeOverlay.style("visibility", "visible");
          var value2 = y.invert(dragStartPosition[1] - margin.top);
          rangeSelection = [Math.min(value, value2), Math.max(value, value2)];
          var start = [
            Math.min(dragStartPosition[0], offsetX),
            Math.min(dragStartPosition[1], offsetY)
          ];
          rangeOverlay
            .attr("x", 0)
            .attr("width", width)
            .attr("y", start[1] - margin.top)
            .attr("height", Math.abs(offsetY - dragStartPosition[1]));
        }
      });

      workRegion.on("mouseleave", () => {
        clearTimeout(this.tooltipHandle);
        tooltip.style("display", "none");
      });

      var dragging = false;
      var dragStartPosition = null;
      var rangeSelection = null;
      workRegion.on("mousedown", () => {
        if (!this.rangeSelection) {
          return;
        }
        var e = d3.event;
        var { offsetX, offsetY } = e;
        e.preventDefault();
        dragStartPosition = [offsetX, offsetY];
        dragging = true;
      });

      workRegion.on("mouseup", () => {
        if (!dragging) {
          return;
        }
        var e = d3.event;
        d3.event.preventDefault();
        rangeOverlay.style("visibility", "hidden");
        dragging = false;
        if (e.which === 1) {
          this.$emit("range-selected", rangeSelection);
        }
      });

      workRegion.on("contextmenu", () => {
        d3.event.preventDefault();
      });

      var x = d3
        .scaleBand()
        .range([0, width])
        .padding(0.1);
      this.x = x;

      var y = d3.scaleLinear().rangeRound([height, 0]);
      // y.tickFormat(d3.format(".3n"));
      y.tickFormat(".3n");
      // console.log(y.tickFormat());
      this.y = y;
    },
    update() {
      var { records_: records, svg, x, y, height, width, mean, median } = this;
      var min = this.min ? this.min : d3.min(records, record => record.value);
      var max = this.max ? this.max : d3.max(records, record => record.value);
      x.domain(records.map(record => record._id));
      y.domain([min, max + (max - min) / 10]);

      svg.selectAll(".axes").remove();

      svg
        .append("g")
        .attr("class", "axes")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickValues([]))
        .append("text")
        .attr("class", "axis-label")
        .attr("fill", "#000")
        .attr("x", width)
        .attr("y", 20)
        .text("Records");

      var formatter = value => {
        return d3
          .format(".3n")(value)
          .replace("+", "")
          .replace("e", "E");
      };

      svg
        .append("g")
        .attr("class", "axes")
        .call(d3.axisLeft(y).tickFormat(formatter))
        .append("text")
        .attr("class", "axis-label")
        .attr("fill", "#000")
        .attr("y", -10)
        .attr("x", 10)
        .text("Value");

      this.barContainer
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

      svg
        .selectAll(".guideline")
        .data(this.guidelines)
        .join(
          enter => {
            enter
              .append("line")
              .attr("class", "guideline")
              .attr("x1", 0)
              .attr("x2", width)
              .attr("y1", guideline => {
                return y(guideline.value);
              })
              .attr("y2", guideline => {
                return y(guideline.value);
              })
              .attr("stroke-dasharray", guideline => {
                return guideline.strokeDasharray
                  ? guideline.strokeDasharray
                  : null;
              })
              .append("title")
              .text(guideline => guideline.name);
          },
          update => {
            update
              .transition()
              .duration(300)
              .attr("x1", 0)
              .attr("x2", width)
              .attr("y1", guideline => {
                return y(guideline.value);
              })
              .attr("y2", guideline => {
                return y(guideline.value);
              });
          },
          remove => {
            remove.remove();
          }
        );
    }
  }
};
</script>

<template>
  <div class="numeric-chart">
    <div class="sort-button" @click="sort = !sort">
      <span>{{ sort ? "unsort" : "sort" }}</span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.numeric-chart {
  height: 100%;
  position: relative;
  overflow-x: hidden;
  overflow-y: hidden;

  .sort-button {
    position: absolute;
    font-size: 12px;
    bottom: -4px;
    left: 13px;
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

  .axes {
    .tick text {
      font-size: 12px;
    }
  }

  .axis-label {
    font-size: 12px;
  }

  .range-overlay {
    fill: rgba(255, 166, 0, 0.253);
  }

  .guideline {
    stroke: red;
    stroke-width: 1px;
    shape-rendering: crispEdges;
  }

  .tooltip {
    position: absolute;
    background: white;
    border: 1px solid black;
    color: black;
    padding: 0px 5px;
    font-size: 14px;
  }
}
</style>
