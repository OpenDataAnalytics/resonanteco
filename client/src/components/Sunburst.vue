<script>
import Sunburst from "@arclamp/sunburst-chart";
import debounce from "lodash.debounce";

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
      this.debouncedUpdate(data);
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.chart = Sunburst()
        .width(this.$el.offsetWidth)
        .height(this.$el.offsetHeight)
        .tooltipShow(d => d.name !== "")
        .tooltipTitle(d => {
          const text = this.chart._tooltipTitle(d);
          return text
            .split(" > ")
            .slice(1)
            .join(" > ");
        })
        .tooltipContent(d => (d.value !== undefined ? `value: ${d.value}` : ""))
        .color(d => this.cmap(d.name))
        .data({
          name: "",
          children: []
        });

      this.debouncedUpdate = _.debounce(this.update.bind(this), 500);

      this.chart(this.$el);
    });
  },
  methods: {
    update(data) {
      this.chart.data(data);
    }
  }
};
</script>

<template>
  <div class="eco-sunburst" />
</template>

<style>
.eco-sunburst {
  flex: 1;
}

textPath.text-contour {
  stroke: none !important;
}

textPath.text-stroke {
  fill: white !important;
}
</style>