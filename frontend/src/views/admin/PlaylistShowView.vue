<template>
  <v-row>
    <v-snackbar v-model="downloadStarted" top right timeout="4000">
        Download iniciado...
    </v-snackbar>
    <v-col>
      <v-row align="center" justify="center">
        <v-card class="mx-4" max-width="650px">
          <v-progress-linear
            v-if="downloadPercentage > 0 && downloadPercentage < 100"
            :value="downloadPercentage"
            stream>
          </v-progress-linear>
          <v-toolbar flat>
            <v-toolbar-title>Faixas na Playlist</v-toolbar-title>
          </v-toolbar>
          <v-divider></v-divider>
          <v-card-text>
              <v-row align="center" justify="center">
               <v-col>
                <v-text-field
                  v-model="search"
                  prepend-icon="search"
                  label="Pesquisar"
                  single-line
                  hide-details
                  clearable
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-data-table
                style="flex: 1 1 auto"
                :headers="headers"
                :items="files"
		:search="search"
                full-width
              >
                <template v-slot:item.actions="{ item }">
                
                
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <v-icon class="mr-2" v-on="on"
                     @click="
                      downloadFile(
                        item.file_name,
                        item.bytes
                      )"
                      >mdi-download</v-icon>
                  </template>
                  <span>Descarregar faixa</span>
                </v-tooltip>
                
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <v-icon class="mr-2" v-on="on"
                     @click="
                      deleteFile(
                        item.file_name,
                      )"
                      >mdi-delete-forever</v-icon>
                  </template>
                  <span>Apagar faixa</span>
                </v-tooltip>
                
                </template>
              </v-data-table>
            </v-row>
          </v-card-text>
        </v-card>
      </v-row>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import BackendServices from "@/services/BackendServices";
@Component
export default class PlaylistShowView extends Vue {
  headers = [
    { text: "Nome", value: "file_name", align: "left" },
    { text: "Ações", value: "actions", align: "right" }
  ];
  files = [];
  search = "";

  downloadPercentage = 0;
  downloadStarted: boolean | null = null;
  
  created() {
      this.getPlaylistContents();
  }

  getPlaylistContents() {
      BackendServices.getPlaylistContents().then(response => {
        this.files = response;
      });
  }

  downloadProgress(downloaded: number) {
    if (this.downloadStarted == null) this.downloadStarted = true;
    this.downloadPercentage = downloaded;
  }

  downloadFile(filename: string, filesize: number) {
      BackendServices.downloadPlaylistTrack(
        process.env.VUE_APP_ROOT_API +
          "/playlist/track/" +
          filename +
          "/",
        filename,
        filesize,
        this.downloadProgress
      );
  }
  
  deleteFile(filename: string) {
    if(confirm("Vai remover permanentemente o ficheiro. Prima Ok para confirmar a remoção, Cancelar se não tiver a certeza.")){
      BackendServices.deletePlaylistTrack(filename);
    }
  }
}
</script>
