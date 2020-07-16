<template>
  <v-row
    ><v-col
      ><v-row align="center" justify="center">
        <h1 class="text-h3">Oops! Página não encontrada</h1>
      </v-row>
      <v-row align="center" justify="center" class="pt-12"
        ><p>
          Isto pode dever-se ao uso de um link antigo, ou à página ter mudado de
          sítio.
        </p></v-row
      >
      <v-row class="pt-12" align="center" justify="center">
        <v-btn to="/"> Voltar à página inicial </v-btn>
      </v-row>
    </v-col>
  </v-row>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  components: {},
})
export default class NotFoundView extends Vue {}
</script>
