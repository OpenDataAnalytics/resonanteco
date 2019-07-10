<script>
import _ from "lodash";
import numeral from "numeral";

var metagenomeSumProperties = [
  "GBp",
  "Number of features identified",
  "CDS",
  "rRNA"
];

export default {
  name: "MetagenomePropertiesTable",
  props: {
    filteredTables: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      headers: [
        {
          text: "Sample",
          align: "left",
          value: "name"
        },
        ...metagenomeSumProperties.map(property => ({
          text: property,
          value: property
        })),
        {
          text: "GC",
          value: "GC"
        }
      ]
    };
  },
  computed: {
    metagenomeSumProperties: () => metagenomeSumProperties,
    gcAggregated() {
      var gcNumbers = this.filteredTables.summary.map(summary =>
        parseFloat(summary.GC)
      );
      var min = Math.min(...gcNumbers);
      var max = Math.max(...gcNumbers);
      var mean = _.mean(gcNumbers);
      return `(${numeral(min).format("0.[00]")}% ~ ${numeral(max).format(
        "0.[00]"
      )}%) ${numeral(mean).format("0.[00]")}%`;
    },
    items() {
      var rows = Object.entries(this.filteredTables.table7).map(
        ([key, values]) => {
          var name = this.getPorjectName(
            this.filteredTables.meta.find(meta => meta["taxon_oid"] === key)
          );
          var gc = this.filteredTables.summary.find(
            summary => summary["taxon_oid"] === key
          )["GC"];
          gc = numeral(gc).format("0.[00]") + "%";
          var item = { name, GC: gc };
          for (let property of metagenomeSumProperties) {
            item[property] = numeral(values[property]).format("0,0.[000]");
          }
          return item;
        }
      );
      if (this.filteredTables.meta.length > 1) {
        var aggregated = {
          name: "Aggregated"
        };
        for (let property of metagenomeSumProperties) {
          aggregated[property] = numeral(this.table7Sum(property)).format(
            "0,0.[000]"
          );
        }
        aggregated["GC"] = this.gcAggregated;
        rows.unshift(aggregated);
      }
      return rows;
    }
  },
  methods: {
    getPorjectName(sample) {
      return sample["Genome Name / Sample Name"].split(" - ")[1];
    },
    table7Sum(property) {
      return _.sum(
        Object.values(this.filteredTables.table7).map(
          values => values[property]
        )
      );
    }
  }
};
</script>

<template>
  <v-data-table
    :headers="headers"
    :items="items"
    class="metagenome-properties-table"
    :rows-per-page-items="[3]"
  >
    <template v-slot:items="{ item }">
      <td>{{ item.name }}</td>
      <td v-for="property of metagenomeSumProperties" :key="property">
        {{ item[property] }}
      </td>
      <td>{{ item.GC }}</td>
    </template>
  </v-data-table>
</template>

<style lang="scss">
.metagenome-properties-table {
  // fix to prevent table height shifting
  min-height: 177px;
  position: relative;
  background: white;

  table.v-table thead tr {
    height: 40px;
  }

  table.v-table tbody td,
  table.v-table tbody th {
    height: 33px;
  }

  .v-datatable__actions {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
  }

  .v-datatable__actions__select .v-select {
    margin: 0px 0 0px 34px;
  }
  .v-datatable__actions__range-controls {
    min-height: 30px;

    button {
      margin-top: 0;
      margin-bottom: 0;
    }
  }
}
</style>
