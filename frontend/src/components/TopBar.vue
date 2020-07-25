<template>
  <nav>
    <v-app-bar app>
      <v-app-bar-nav-icon
        @click.stop="drawer = !drawer"
        class="hidden-md-and-up"
        aria-label="Menu"
      />

      <v-toolbar-title class="mr-5 hidden-sm-and-down">
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
        <v-menu
          offset-y
          transition="slide-y-transition"
          open-on-hover
          rounded="0"
        >
          <template v-slot:activator="{ on }">
            <v-btn text v-on="on">
              Gerir programas
            </v-btn>
          </template>
          <v-list
            v-for="(program, index) in $store.getters.getUser.programSet"
            :key="program.id"
          >
            <v-divider v-if="index !== 0"></v-divider>
            <v-subheader>{{ program.name }}</v-subheader>
            <v-list-item-content>
              <v-btn
                text
                block
                :to="{ name: 'programs-upload', params: { id: program.id } }"
                >Upload <v-spacer /> <v-icon>backup</v-icon>
              </v-btn>
            </v-list-item-content>
            <v-list-item-content>
              <v-btn text block
                >Arquivo <v-spacer /> <v-icon>archive</v-icon>
              </v-btn>
            </v-list-item-content>
          </v-list>
        </v-menu>
        <!-- End of own program menu -->
        <v-divider vertical inset></v-divider>
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

      <div class="hidden-sm-and-down">
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
      </div>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" app absolute temporary>
      <v-list-item>
        <v-list-item-content>
          <v-btn text class="align-center" to="/">
            <img src="@/assets/logo.png" width="20" style="margin-right:10pt" />
            <img />
            Radiólogo
          </v-btn>
        </v-list-item-content>
      </v-list-item>
      <div v-if="$store.getters.getUser != null">
        <v-divider></v-divider>

        <v-list-group v-if="$store.getters.getUser.programSet.length > 0">
          <template v-slot:activator>
            <v-list-item-title>Gerir programas</v-list-item-title>
          </template>
          <div
            v-for="(program, index) in $store.getters.getUser.programSet"
            :key="program.id"
            class="ml-4"
          >
            <v-divider class="mb-3 mt-2" v-if="index !== 0"></v-divider>
            <p class="text-caption ml-4">{{ program.name }}</p>
            <v-btn
              text
              block
              :to="{
                name: 'programs-upload',
                params: { id: program.id }
              }"
              >Upload <v-spacer /> <v-icon>backup</v-icon>
            </v-btn>
            <v-btn text block
              >Arquivo <v-spacer /> <v-icon>archive</v-icon>
            </v-btn>
          </div>
        </v-list-group>

        <v-list-item to="/administration/programs/">
          <v-list-item-content>
            Programas
          </v-list-item-content>
        </v-list-item>

        <v-list-item to="/administration/playlist/">
          <v-list-item-content>
            Playlist
          </v-list-item-content>
        </v-list-item>

        <v-list-item to="/administration/members/">
          <v-list-item-content>
            Membros
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item to="/profile/">
          <v-list-item-content>
            {{ $store.getters.getUser.authorName }}
          </v-list-item-content>
        </v-list-item>

        <v-list-item v-if="$store.getters.getUser != null" text @click="logout">
          <v-list-item-content>
            Sair
          </v-list-item-content>
        </v-list-item>
      </div>
      <v-list-item to="/login/" v-else>
        <v-list-item-content>
          Login
        </v-list-item-content>
      </v-list-item>
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
    this.$router.push({ name: "login" });
  }
}
</script>
