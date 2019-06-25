<script>
import { mapState, mapActions } from "vuex";

import NavigationBar from "@/components/NavigationBar";

export default {
  name: "ItemView",
  components: {
    NavigationBar
  },
  inject: ["girderRest"],
  data() {
    return {
      id: this.$route.params.id,
      pagination: {
        page: 1,
        rowsPerPage: 15
      }
    };
  },
  computed: {
    rows() {
      if (!this.item) {
        return [];
      }
      var { meta } = this.item;
      var rows = [];
      for (let key in meta) {
        if (typeof meta[key] !== "object") {
          rows.push({ key, value: meta[key] });
        }
      }
      return rows;
    },
    headers() {
      return [{ text: "Key", value: "key" }, { text: "Value", value: "value" }];
    }
  },
  asyncComputed: {
    async item() {
      if (!this.id) {
        return null;
      }
      var { data: item } = await this.girderRest.get(`item/${this.id}`);
      return item;
    }
  },
  activated() {
    this.id = this.$route.params.id;
  },
};
</script>

<template>
  <v-content class="item-view">
    <NavigationBar />
    <v-container grid-list-md>
      <v-layout align-center>
        <v-flex>
          <v-data-table
            :headers="headers"
            :items="rows"
            :pagination.sync="pagination"
            :rows-per-page-items="[5,10,15]">
            <template v-slot:items="{item}">
              <td>{{item.key}}</td>
              <td>{{item.value}}</td>
            </template>
          </v-data-table>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>
