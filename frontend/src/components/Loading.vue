<template>
  <v-progress-linear
    :active="loading"
    indeterminate
    color="black"
    background-opacity="0"
  ></v-progress-linear>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class Loading extends Vue {
  loading: boolean = this.$store.getters.getLoading;

  created() {
    this.loading = this.$store.getters.getLoading;
    this.$store.watch(
      (state, getters) => getters.getLoading,
      () => {
        this.loading = this.$store.getters.getLoading;
      }
    );
  }
}
</script>
