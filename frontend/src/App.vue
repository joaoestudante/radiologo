<template>
  <v-app id="app">
    <top-bar />

    <v-main>
      <Loading />
      <v-container fill-height fluid>
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer app absolute class="font-weight-medium" padless>
      <v-row justify="center" align="center" no-gutters>
        <v-btn text> Contactos </v-btn>
        <v-spacer />
        <v-icon>flare</v-icon
        ><v-switch class="pl-2 pr-2" v-model="$vuetify.theme.dark"></v-switch>
        <v-icon>brightness_2</v-icon>
      </v-row>
    </v-footer>
  </v-app>
</template>

<script lang="ts">
import TopBar from "@/components/TopBar.vue";
import Loading from "@/components/Loading.vue";
import { Component, Vue } from "vue-property-decorator";

@Component({
  components: { TopBar, Loading }
})
export default class App extends Vue {
  created() {
    const setVuetifyTheme = (value: boolean) => {
      this.$vuetify.theme.dark = value;
    };
    window
      .matchMedia("(prefers-color-scheme: dark)")
      .addEventListener("change", function(e) {
        console.log(`changed to ${e.matches ? "dark" : "light"} mode`);
        setVuetifyTheme(e.matches);
      });
  }
}
</script>
