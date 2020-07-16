<template>
  <v-row align="center" justify="center">
    <v-col cols="11">
      <v-row>
        <WeeklySchedule></WeeklySchedule>
      </v-row>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import WeeklySchedule from "@/components/WeeklySchedule.vue";
import { Component, Vue } from "vue-property-decorator";

@Component({
  components: { WeeklySchedule },
})
export default class HomeView extends Vue {}
</script>
