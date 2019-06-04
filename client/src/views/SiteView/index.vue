<script>
import { mapState, mapActions } from "vuex";

import NavigationBar from "@/components/NavigationBar";
import ChildrenItems from "./ChildrenItems";

export default {
  name: "SiteView",
  components: {
    NavigationBar,
    ChildrenItems
  },
  inject: ["girderRest"],
  data() {
    return {
      name: this.$route.params.name,
      pagination: {
        page: 1,
        rowsPerPage: 15
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
      if (!this.name) {
        return null;
      }

      var { data: items } = await this.girderRest.get(
        `site/${this.name}/records`
      );
      return items;
    }
  },
  activated() {
    this.name = this.$route.params.name;
  }
};
</script>

<template>
  <v-content class="item-view">
    <NavigationBar />
    <v-container grid-list-md fluid>
      <v-layout align-center>
        <v-flex>
          <v-data-table
            v-if="items"
            :headers="headers"
            :items="records"
            item-key="_id"
            :pagination.sync="pagination"
            :rows-per-page-items="[5, 10, 15]"
          >
            <template #items="props">
              <tr @click="props.expanded = !props.expanded">
                <td v-for="header of headers" :key="header.value">
                  {{ props.item[header.value] }}
                </td>
              </tr>
            </template>
            <template #expand="{item}">
              <ChildrenItems
                class="ml-5"
                :key="item._id"
                :recordId="item._id"
              />
            </template>
          </v-data-table>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<style lang="scss" scoped>
.child {
  // margin-left:
}
</style>
