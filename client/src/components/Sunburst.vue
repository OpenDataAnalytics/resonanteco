<script>
import Sunburst from "sunburst-chart";

export default {
  name: "Sunburst",
  props: {
    filteredTablesValues: {
      type: Object,
      required: true
    }
  },
  computed: {
    treeData() {
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
    treeData(data) {
      this.update(data);
    }
  },
  mounted() {
    this.chart = Sunburst()
      .width(400)
      .height(400)
      .data({
        name: "all",
        children: []
      });

    this.chart(this.$refs.container);

    this.update(this.treeData);
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
