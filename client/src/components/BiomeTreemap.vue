<script>
import * as d3 from "d3";

import { mapColor } from "@/util/colors";

export default {
  name: "BiomeTreemap",
  components: {},
  inject: ["girderRest"],
  props: {
    filter: {
      type: Object,
      required: false
    },
    selections: {
      type: Array,
      required: false,
      default: () => []
    }
  },
  computed: {
    treemapData() {
      if (!this.biomeCounts) {
        return null;
      }
      var data = {
        name: "biome",
        children: this.biomeCounts.map(biome => ({
          id: biome.key.replace(/ /g, "-"),
          name: biome.key,
          value: biome.count
        }))
      };
      return d3
        .hierarchy(data)
        .sum(d => d.value)
        .sort((a, b) => b.value - a.value);
    }
  },
  asyncComputed: {
    async biomeCounts() {
      var params = {};
      if (this.filter) {
        params["filter"] = this.filter;
      }
      var { data: meta } = await this.girderRest.get("meta", { params });
      return meta.biome;
    }
  },
  watch: {
    treemapData(value) {
      if (value) {
        this.update();
      }
    },
    selections() {
      this.update();
    }
  },
  methods: {
    update() {
      var width = this.$el.clientWidth;
      this.width = width;
      var height = this.$el.clientHeight;
      this.height = height;

      var layout = d3
        .treemap()
        .tile(d3.treemapSquarify)
        .size([width, height])
        .paddingInner(2);
      var nodes = layout(this.treemapData);

      var leaves = nodes.leaves();
      if (leaves.length === 1 && leaves[0].data.name === "biome") {
        d3.select(this.$el)
          .selectAll(".leaf")
          .remove();
        return;
      }

      var svg = d3.select(this.$el);
      svg
        .selectAll(".leaf")
        .data(leaves, d => d.data.name)
        .join(
          enter => {
            var leaves = enter
              .append("div")
              .attr("class", "leaf")
              .classed(
                "selected",
                d => this.selections.indexOf(d.data.name) !== -1
              )
              .attr(
                "title",
                d =>
                  `${d
                    .ancestors()
                    .reverse()
                    .map(d => d.data.name)
                    .join(" / ")}\n${d.value}`
              )
              .style("left", d => `${d.x0}px`)
              .style("top", d => `${d.y0}px`)
              .style("width", d => `${d.x1 - d.x0}px`)
              .style("height", d => `${d.y1 - d.y0}px`)
              .style("background-color", d => mapColor("biome", d.data.name))
              .on("click", d => {
                var index = this.selections.indexOf(d.data.name);
                if (index !== -1) {
                  var selections = this.selections.slice();
                  selections.splice(index, 1);
                  this.$emit("update:selections", selections);
                } else {
                  this.$emit("update:selections", [
                    ...this.selections,
                    d.data.name
                  ]);
                }
              });

            leaves
              .append("div")
              .attr("class", "leaf-title")
              .text(d => {
                if (d.y1 - d.y0 < 14) {
                  return;
                }
                var name = d.data.name.replace(" biome", "");
                if (d.x1 - d.x0 < name.length * 10) {
                  return;
                }
                return name;
              });

            leaves
              .append("div")
              .attr("class", "leaf-value")
              .text(d => d.data.value);
          },
          update => {
            var leaves = update
              .classed(
                "selected",
                d => this.selections.indexOf(d.data.name) !== -1
              )
              .transition()
              .duration(300)
              .style("left", d => `${d.x0}px`)
              .style("top", d => `${d.y0}px`)
              .style("width", d => `${d.x1 - d.x0}px`)
              .style("height", d => `${d.y1 - d.y0}px`)
              .style("background-color", d => mapColor("biome", d.data.name));

            leaves.select(".leaf-title").text(d => {
              if (d.y1 - d.y0 < 14) {
                return;
              }
              if (d.x1 - d.x0 < d.data.name.length * 10) {
                return;
              }
              return d.data.name;
            });
            leaves.select(".leaf-value").text(d => d.data.value);
          },
          remove => {
            remove
              .transition()
              .duration(300)
              .style("width", "0px")
              .style("height", "0px")
              .remove();
          }
        );
    }
  }
};
</script>

<template>
  <div class="biome-treemap"></div>
</template>

<style lang="scss" scoped>
.biome-treemap {
  height: 100%;
  position: relative;
}
</style>

<style lang="scss">
.biome-treemap {
  overflow: hidden;

  .leaf {
    position: absolute;
    overflow: hidden;
    transition: transform 0.4s;
    border: solid 2px transparent;

    &:hover {
      transition: transform 0.2s;
      transform: scale(0.97) !important;
    }

    &.selected {
      border: solid 2px black;
      transform: scale(0.99);
    }

    .leaf-title {
      margin: 10px 0 0 10px;
      color: white;
    }

    .leaf-value {
      margin: 0 0 0 10px;
      color: rgba(255, 255, 255, 0.589);
      font-size: 20px;
    }
  }
}
</style>
