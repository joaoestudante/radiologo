<template>
  <v-app id="app">
    <top-bar />

    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer
      app
      absolute
      class="font-weight-medium"
      color="grey lighten-3"
      padless
    >
      <v-row justify="center" no-gutters>
        <v-btn text rounded class="my-2"> Contactos </v-btn>
      </v-row>
      <v-col class="grey lighten-4 py-2 text-center" cols="12">
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
