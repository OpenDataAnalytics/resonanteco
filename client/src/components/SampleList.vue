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
    },
    checkAll(checked) {
      if (checked) {
        this.$emit("update:selectedSamples", dataset.meta.slice());
      } else {
        this.$emit("update:selectedSamples", []);
      }
    }
  }
};
</script>

<template>
  <div class="sample-list">
    <v-list dense>
      <v-list-tile class="hover-show-parent">
        <v-list-tile-content>
          <v-list-tile-title>
            <v-subheader style="height:unset;padding:0;"
              >Projects and samples
            </v-subheader>
          </v-list-tile-title>
        </v-list-tile-content>
        <v-list-tile-action
          class="hover-show-child"
          :style="{
            display: selectedSamples.length > 1 ? 'inherit' : ''
          }"
        >
          <v-checkbox
            :value="!!selectedSamples.length"
            :indeterminate="
              !!selectedSamples.length &&
                selectedSamples.length !== dataset.meta.length
            "
            @change="checkAll($event)"
          />
        </v-list-tile-action>
      </v-list-tile>
    </v-list>
    <vue-nice-scrollbar classes="my-scrollbar">
      <v-list dense>
        <v-list-tile
          class="hover-show-parent"
          v-for="sample in dataset.meta"
          :key="sample['taxon_oid']"
          :class="{ selected: selectedSamples.indexOf(sample) !== -1 }"
          @click="123"
        >
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
          <v-list-tile-action
            class="hover-show-child"
            :style="{
              display:
                selectedSamples.indexOf(sample) !== -1 &&
                selectedSamples.length > 1
                  ? 'inherit'
                  : ''
            }"
          >
            <v-checkbox
              :value="selectedSamples.indexOf(sample) !== -1"
              @change="check($event, sample)"
            ></v-checkbox>
          </v-list-tile-action>
        </v-list-tile>
      </v-list>
    </vue-nice-scrollbar>
  </div>
</template>

<style lang="scss" scoped>
.sample-list {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.nice-bar {
  margin: unset;
  flex: 1;
}

.v-list {
  .v-list__tile__action {
    min-width: unset;
  }
  .selected {
    background: #eee;
  }
}

.hover-show-parent {
  .hover-show-child {
    display: none;
    &.show {
      display: flex;
    }
  }
  &:hover {
    .hover-show-child {
      display: inherit;
    }
  }
}
</style>

<style lang="scss">
.hover-show-child {
  .v-icon.theme--light {
    color: rgb(206, 206, 206);
  }
}

.my-scrollbar {
  .v-list .v-list__tile {
    font-weight: 500;
  }

  &.theme-light .nice-bar-slider-y {
    background: #ccc;
  }

  .nice-bar-slider-x {
    display: none;
  }
}
</style>
