<script>
import { dataset } from "@/util/dataLoader";

export default {
  name: "SampleList",
  props: {
    selectedSamples: {
      type: Array,
      required: true
    }
  },
  computed: {
    dataset: () => dataset
  },
  methods: {
    getPorjectName(sample) {
      return sample["Genome Name / Sample Name"].split(" - ")[1];
    },
    toggle(sample) {
      if (this.selectedSamples.indexOf(sample) !== -1) {
        this.$emit("update:selectedSamples", []);
      } else {
        this.$emit("update:selectedSamples", [sample]);
      }
    },
    check(checked, sample) {
      if (checked) {
        if (this.selectedSamples.indexOf(sample) === -1) {
          this.$emit("update:selectedSamples", [
            ...this.selectedSamples,
            sample
          ]);
        }
      } else {
        var index = this.selectedSamples.indexOf(sample);
        if (index !== -1) {
          this.selectedSamples.splice(index, 1);
          this.$emit("update:selectedSamples", this.selectedSamples);
        }
      }
    }
  }
};
</script>

<template>
  <v-list dense>
    <v-list-tile
      v-for="sample in dataset.meta"
      :key="sample['taxon_oid']"
      :class="{ selected: selectedSamples.indexOf(sample) !== -1 }"
      @click="123"
    >
      <v-list-tile-action>
        <v-checkbox
          :value="selectedSamples.indexOf(sample) !== -1"
          @change="check($event, sample)"
        ></v-checkbox>
      </v-list-tile-action>
      <v-list-tile-content @click="toggle(sample)">
        <v-list-tile-title>
          <v-tooltip right open-delay="500">
            <template #activator="data">
              <span v-on="data.on">{{ getPorjectName(sample) }}</span>
            </template>
            {{ getPorjectName(sample) }}
          </v-tooltip>
        </v-list-tile-title>
      </v-list-tile-content>
    </v-list-tile>
  </v-list>
</template>

<style lang="scss" scoped>
.v-list {
  .v-list__tile__action {
    min-width: unset;
  }
  .selected {
    background: #eee;
  }
}
</style>
