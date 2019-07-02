<script>
// import { schemePaired } from "d3-scale-chromatic";
// import { scaleOrdinal } from "d3-scale";
import Sunburst from "sunburst-chart";

function treeifyTable8(tab) {
  let tree = {};
  Object.keys(tab).forEach(key => {
    const val = tab[key];
    if (val === 0) {
      return;
    }

    const [kingdom, species] = key.split(":");
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
    filteredTablesValues: {
      type: Object,
      required: true
    },
    cmap: {
      required: true
    }
  },
  computed: {
    treeData() {
      return this.filteredTablesValues.table8.map(treeifyTable8);
    },
    treeDataSum() {
      return treeSum(this.treeData);
    },
    sunburstData() {
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
    testData() {
      return {
        name: "root",
        children: [
          {
            name: "A",
            value: 3
          },
          {
            name: "B",
            value: 4
          }
        ]
      };
    }
  },
  watch: {
    sunburstData(data) {
      this.update(data);
    }
  },
  mounted() {
    this.chart = Sunburst()
      .width(400)
      .height(400)
      .tooltipContent(d => `value: ${d.value}`)
      .color(d => this.cmap(d.name))
      .data({
        name: "",
        children: []
      });

    this.chart(this.$refs.container);

    this.update(this.sunburstData);
  },
  methods: {
    update(data) {
      this.chart.data(data);
    }
  }
};
</script>

<template>
  <div ref="container" />
</template>
