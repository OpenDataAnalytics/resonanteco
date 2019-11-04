<script>
import { isEmpty } from "lodash";

import NumericChart from "@/components/NumericChart";
import additionalFilterProperties from "./additionalFilterProperties.js";

export default {
  name: "AddFilter",
  components: {
    NumericChart
  },
  inject: ["girderRest"],
  props: {
    filter: {
      type: Object,
      required: false
    },
    visible: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      selectedField: null,
      valueRange: [],
      includeFilter: !isEmpty(this.filter)
    };
  },
  computed: {
    fields: () => [{ value: null, text: "" }, ...additionalFilterProperties],
    cleanFilter() {
      var filter = { ...this.filter };
      delete filter[this.selectedField];
      return filter;
    },
    filter_() {
      var filter = {};
      if (
        this.valueRange[0] !== this.fieldMeta.min ||
        this.valueRange[1] !== this.fieldMeta.max
      ) {
        filter[this.selectedField] = {
          gt: parseFloat(this.valueRange[0].toFixed(4)),
          lt: parseFloat(this.valueRange[1].toFixed(4))
        };
      }
      if (this.includeFilter) {
        filter = { ...this.cleanFilter, ...filter };
      }
      return filter;
    }
  },
  asyncComputed: {
    async fieldMeta() {
      if (!this.selectedField) {
        return null;
      }
      var { data: result } = await this.girderRest.get("meta/field_meta", {
        params: {
          field: this.selectedField
        }
      });
      return result;
    },
    async records() {
      if (!this.selectedField || !this.fieldMeta) {
        return null;
      }
      var { data: result } = await this.girderRest.get("record/filtered", {
        params: {
          fields: JSON.stringify([this.selectedField]),
          filter: this.filter_
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
  },
  watch: {
    fieldMeta(fieldMeta) {
      if (!fieldMeta) {
        return;
      }
      this.valueRange = [fieldMeta.min, fieldMeta.max];
    },
    visible(value) {
      if (!value) {
        this.selectedField = null;
        this.valueRange = [];
        this.includeFilter = true;
      }
    }
  },
  methods: {
    isEmpty,
    updateValueRange(value) {
      this.valueRange = value;
    }
  }
};
</script>

<template>
  <v-card>
    <v-card-title>
      Add filter
    </v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="4">
          <v-select
            :items="fields"
            label="Field"
            v-model="selectedField"
            hide-details
          ></v-select>
        </v-col>
      </v-row>
      <transition name="fade">
        <div v-if="records" class="transition-container">
          <v-row no-gutters>
            <v-col class="flex-grow-0" style="min-width:60px;">
              <v-range-slider
                class="two-line mt-2"
                vertical
                :value="valueRange"
                @change="updateValueRange"
                :max="fieldMeta.max"
                :min="fieldMeta.min"
                hide-details
              />
              <v-btn
                text
                small
                @click="valueRange = [fieldMeta.min, fieldMeta.max]"
                >Reset</v-btn
              >
            </v-col>
            <v-col>
              <NumericChart
                style="height:400px"
                :records="records"
                range-selection
                @range-selected="updateValueRange"
              />
            </v-col>
          </v-row>
          <v-checkbox
            dense
            hide-details
            v-model="includeFilter"
            :disabled="isEmpty(filter)"
            label="Include other filters"
          ></v-checkbox>
        </div>
      </transition>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn
        text
        color="primary"
        :disabled="
          !selectedField ||
            !fieldMeta ||
            (valueRange[0] === fieldMeta.min && valueRange[1] === fieldMeta.max)
        "
        @click="$emit('add', { [selectedField]: filter_[selectedField] })"
        >Add</v-btn
      >
    </v-card-actions>
  </v-card>
</template>

<style lang="scss" scoped>
.transition-container {
  height: 440px;
}
</style>

<style lang="scss">
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease-in-out;
  overflow: hidden;
}
.fade-enter,
.fade-leave-to {
  height: 0px !important;
  opacity: 0;
}

.v-input__slider.two-line {
  .v-input__slot {
    height: 350px;
    .v-slider {
      height: 90%;
    }
  }
}
</style>
