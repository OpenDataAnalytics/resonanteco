<script>
import * as d3 from "d3";

import Sunburst from "sunburst-chart";
import debounce from "lodash.debounce";

function treeifyTable8(tab) {
  let tree = {};
  Object.keys(tab).forEach(key => {
    const val = tab[key];
    if (val === 0) {
      return;
    }

    const [kingdom, species] = key.split(":");
    if (!kingdom || !species) {
      return;
    }
    tree[kingdom] = tree[kingdom] || {};
    tree[kingdom][species] = tree[kingdom][species] || 0;

    tree[kingdom][species] += val;
  });

  return tree;
}

function speciesAdd(spec1, spec2) {
  const spec1Keys = Object.keys(spec1);
  const spec2Keys = Object.keys(spec2);
  const species = Array.from(new Set(spec1Keys.concat(spec2Keys)));

  let sum = {};
  species.forEach(spec => {
    sum[spec] = (spec1[spec] || 0) + (spec2[spec] || 0);
  });

  return sum;
}

function treeAdd(tree1, tree2) {
  const tree1Keys = Object.keys(tree1);
  const tree2Keys = Object.keys(tree2);
  const kingdoms = Array.from(new Set(tree1Keys.concat(tree2Keys)));

  let sum = {};
  kingdoms.forEach(kingdom => {
    const kingdom1 = tree1[kingdom] || {};
    const kingdom2 = tree2[kingdom] || {};

    sum[kingdom] = speciesAdd(kingdom1, kingdom2);
  });

  return sum;
}

function treeSum(arr) {
  return arr.reduce((acc, cur) => treeAdd(acc, cur), {});
}

export default {
  name: "Sunburst",
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
  inject: ["girderRest"],
  data: () => ({
    initialized: false
  }),
  computed: {
    treeDataSum() {
      if (!this.treeData) {
        return null;
      }
      return treeSum(this.treeData);
    },
    sunburstData() {
      if (!this.treeDataSum) {
        return null;
      }
      const data = this.treeDataSum;

      return {
        name: "",
        children: Object.keys(data).map(kingdom => ({
          name: kingdom,
          children: Object.keys(data[kingdom]).map(species => ({
            name: species,
            value: data[kingdom][species]
          }))
        }))
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
    async treeData() {
      var { data: records } = await this.girderRest.get("record/filtered", {
        params: {
          fields: JSON.stringify(["table8"]),
          filter: this.filter
        }
      });
      return records.data
        .map(record => record.table8)
        .filter(d => d)
        .map(treeifyTable8);
    }
  },
  watch: {
    sunburstData(data) {
      if (data) {
        if (!this.initialized) {
          this.initialize();
        } else {
          this.debouncedUpdate(data);
        }
      }
    }
  },
  // mounted() {
  //   this.$nextTick(() => {});
  // },
  methods: {
    initialize() {
      this.chart = Sunburst()
        .width(this.$el.offsetWidth)
        .height(this.$el.offsetHeight)
        .showTooltip(d => d.name !== "")
        .tooltipTitle((data, d) => {
          let stack = [];
          let curNode = d;
          while (curNode) {
            stack.unshift(curNode);
            curNode = curNode.parent;
          }
          stack = stack.slice(1);

          return stack.map(d => d.data.name).join(" > ");
        })
        .tooltipContent(d => (d.value !== undefined ? `value: ${d.value}` : ""))
        .color(d => this.cmap(d.name))
        .data({
          name: "",
          children: []
        });

      this.debouncedUpdate = debounce(this.update.bind(this), 500);
      this.update(this.sunburstData);

      this.chart(this.$el);
      this.initialized = true;
    },
    update(data) {
      this.chart.data(data);
    }
  }
};
</script>

<template>
  <div class="eco-sunburst" />
</template>

<style lang="scss">
.eco-sunburst {
  height: calc(100% - 10px);
  padding: 5px;

  > div:first-child svg {
    display: block;
  }
}

textPath.text-contour {
  stroke: none !important;
}

textPath.text-stroke {
  fill: white !important;
}
</style>
