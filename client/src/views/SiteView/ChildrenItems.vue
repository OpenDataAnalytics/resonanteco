<script>
export default {
  name: "ChildrenItems",
  inject: ["girderRest"],
  props: {
    recordId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      pagination: {
        page: 1,
        rowsPerPage: 5
      }
    };
  },
  computed: {
    records() {
      if (!this.items) {
        return [];
      }
      return this.items.map(({ meta }) => meta);
    },
    headers() {
      if (!this.items) {
        return null;
      }
      var record = this.records[0];
      var headers = [];
      for (let key in record) {
        if (typeof record[key] !== "object") {
          headers.push({
            text: key,
            value: key
          });
        }
      }
      return headers;
    }
  },
  asyncComputed: {
    async items() {
      if (!this.recordId) {
        return null;
      }
      var { data: items } = await this.girderRest.get(
        `record/${this.recordId}/children`
      );
      return items;
    }
  }
};
</script>

<template>
  <div>
    <v-data-table
      v-if="items && items.length"
      :headers="headers"
      :items="records"
      item-key="_id"
      hide-actions
    >
      <template #items="props">
        <tr @click="props.expanded = !props.expanded">
          <td v-for="header of headers" :key="header.value">
            {{ props.item[header.value] }}
          </td>
        </tr>
      </template>
    </v-data-table>
    <v-card flat v-if="items && !items.length"
      ><v-card-text>No children records</v-card-text></v-card
    >
  </div>
</template>
