<template>
  <v-app id="app">
    <top-bar />

    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer app absolute class="font-weight-medium">
      <v-col class="text-center" cols="12">
        {{ new Date().getFullYear() }} — <strong>Rádio Zero</strong>
      </v-col>
    </v-footer>
  </v-app>
</template>

<script lang="ts">
import TopBar from "@/components/TopBar.vue";
import { Component, Vue } from "vue-property-decorator";

@Component({
  components: { TopBar },
})
export default class App extends Vue {}
</script>
