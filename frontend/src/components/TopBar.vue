<template>
  <nav>
    <v-app-bar app>
      <v-app-bar-nav-icon
        @click.stop="drawer = !drawer"
        class="hidden-md-and-up"
        aria-label="Menu"
      />

      <v-toolbar-title class="mr-5">
        <v-btn text class="align-center" to="/">
          <img src="@/assets/logo.png" width="20" style="margin-right:10pt" />
          <img />
          Radiólogo
        </v-btn>
      </v-toolbar-title>

      <v-toolbar-items
        class="hidden-sm-and-down"
        hide-details
        v-if="$store.getters.getUser != null"
      >
        <v-menu offset-y transition="slide-y-transition" open-on-hover>
          <template v-slot:activator="{ on }">
            <v-btn text v-on="on">
              Programa
            </v-btn>
          </template>
          <v-list
            v-for="program of $store.getters.getUser.programSet"
            :key="program.id"
          >
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>Upload</v-list-item-title>
              </v-list-item-content>
              <v-list-item-icon>
                <v-icon>backup</v-icon>
              </v-list-item-icon>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>Arquivo</v-list-item-title>
              </v-list-item-content>
              <v-list-item-icon>
                <v-icon>archive</v-icon>
              </v-list-item-icon>
            </v-list-item>
          </v-list>
        </v-menu>
        <!-- End of own program menu -->

        <v-menu offset-y transition="slide-y-transition" open-on-hover>
          <template v-slot:activator="{ on }">
            <v-btn text v-on="on">
              Programas
            </v-btn>
          </template>
        </v-menu>

        <v-menu offset-y transition="slide-y-transition" open-on-hover>
          <template v-slot:activator="{ on }">
            <v-btn text v-on="on">
              Playlist
            </v-btn>
          </template>
        </v-menu>

        <v-menu offset-y transition="slide-y-transition" open-on-hover>
          <template v-slot:activator="{ on }">
            <v-btn text v-on="on">
              Membros
            </v-btn>
          </template>
        </v-menu>
      </v-toolbar-items>

      <v-spacer />

      <v-btn
        v-if="$store.getters.getUser != null"
        text
        class="align-center"
        to="/profile/"
      >
        {{ $store.getters.getUser.authorName }}
      </v-btn>
      <v-btn v-if="$store.getters.getUser != null" text @click="logout">
        Sair
      </v-btn>
      <v-btn v-else text class="align-center" to="/login/">
        Login
      </v-btn>
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
  logout() {
    this.$store.commit("logout");
    this.$router.push({ name: "Login" });
  }
}
</script>
