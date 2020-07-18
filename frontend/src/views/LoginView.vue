<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <v-card class="elevation-6">
        <v-toolbar dark flat>
          <v-toolbar-title>Login no Radiólogo</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-form @submit.prevent>
          <v-card-text>
            <v-text-field
              label="Email"
              v-model="email"
              name="email"
              prepend-icon="mdi-account"
              type="text"
            ></v-text-field>

            <v-text-field
              id="password"
              label="Password"
              v-model="password"
              name="password"
              prepend-icon="mdi-lock"
              type="password"
            ></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn to="/password/recuperar"> Recuperar password </v-btn>
            <v-spacer></v-spacer>
            <v-btn @click="login" type="submit">Login</v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
      <div class="pt-3">
        <v-alert
          dismissible
          :value="alert"
          type="error"
          transition="scale-transition"
          >{{ errorMessage }}</v-alert
        >
      </div>
    </v-col>
  </v-row>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { AxiosError } from "axios";
@Component
export default class Login extends Vue {
  email = "";
  password = "";
  alert = false;
  errorMessage = "";
  login() {
    const email = this.email;
    const password = this.password;
    this.$store
      .dispatch("login", { email, password })
      .then(function(this: Login) {
        this.$router.push("/");
      })
      .catch(function(this: Login, error: AxiosError) {
        this.errorMessage = "";
        this.errorMessage = error.response!.data.detail;
        this.alert = true;
      });
  }
}
</script>
