<script>
import Sunburst from "@/components/Sunburst";
import NumericChart from "@/components/NumericChart";
import additionalFilterProperties from "@/components/additionalFilterProperties";

export default {
  name: "DataInsight",
  inject: ["girderRest"],
  components: {
    Sunburst,
    NumericChart
  },
  props: ["filter"],
  data: () => ({ selectedField: "table8" }),
  computed: {
    properties() {
      return [
        { value: "table8", text: "Sunburst" },
        ...additionalFilterProperties
      ];
    }
  },
  asyncComputed: {
    async records() {
      if (!this.selectedField || this.selectedField === "table8") {
        return null;
      }
      var { data: result } = await this.girderRest.get("record/filtered", {
        params: {
          fields: JSON.stringify([this.selectedField]),
          filter: this.filter
        }
      });
      return result.data.map(data => {
        var properties = this.selectedField.split(".");
        var value = data;
        for (let property of properties) {
          value = value[property];
        }
        return {
          _id: data._id,
          value: value ? value : 0
        };
      });
    }
  }
};
</script>

<template>
  <div class="data-insight">
    <v-select
      class="property-select"
      :items="properties"
      v-model="selectedField"
      hide-details
    ></v-select>
    <Sunburst :filter="filter" v-if="selectedField==='table8'" />
    <div class="chart-container" v-else>
    <NumericChart
      v-if="records"
      :records="records"
    />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.data-insight {
  height: 100%;

  .property-select {
    position: absolute;
    right: 20px;
    width: 200px;
    z-index: 1;
  }

  .chart-container {
    height: 100%;
    padding: 5px;
    padding-top:30px;
  }
}
</style>