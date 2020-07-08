<template>
  <nav>
    <v-app-bar app>
      <v-app-bar-nav-icon
        @click.stop="drawer = !drawer"
        class="hidden-md-and-up"
        aria-label="Menu"
      />

      <v-toolbar-title>
        <v-btn text class="align-center" to="/">
          <img src="@/assets/logo.png" width="20" style="margin-right:10pt" />
          <img />
          Radiólogo
        </v-btn>
      </v-toolbar-title>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" app absolute temporary>
      <!-- -->
    </v-navigation-drawer>
  </nav>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
@Component
export default class TopBar extends Vue {
  drawer = false;
}
</script>
