<script>
import SamplesLocation from "@/components/SamplesLocation";

export default {
  name: "ViewFilterDialog",
  components: { SamplesLocation },
  props: {
    value: {
      type: Boolean,
      required: true
    },
    filter: {
      type: Object,
      required: true
    }
  },
  data: () => ({ ready:false }),
  watch: {
    value(value) {
      if (value) {
        this.readyHandle = setTimeout(() => {
          this.ready = true;
        }, 200);
      } else {
        this.ready = false;
        clearTimeout(this.readyHandle);
      }
    }
  },
  methods: {
    getConditionDisplay(value) {
      if (Array.isArray(value)) {
        return value.join(", ");
      } else {
        var parts = [];
        if (value.gt) {
          parts.push(`>${value.gt}`);
        }
        if (value.lt) {
          parts.push(`<${value.lt}`);
        }
        return parts.join(", ");
      }
    }
  }
};
</script>

<template>
  <v-dialog :value="value" @input="$emit('input', $event)" max-width="900">
    <v-card>
      <v-card-title>
        Filter histroy
      </v-card-title>
      <v-card-text>
        <v-row v-for="(obj, key, index) in filter" :key="index">
          <v-col cols='4'>{{key}}</v-col>
          <v-col>
            <div v-if="key!=='selectedRegion'">
              {{getConditionDisplay(obj)}}
            </div>
            <div v-else style="height: 250px;position:relative;">
              <SamplesLocation
                v-if="ready"
                :selectedRegion="obj"
              />
            </div>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
