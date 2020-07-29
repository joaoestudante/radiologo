<template>
  <v-row>
    <v-col>
      <v-row align="center" justify="center">
        <v-card class="mx-4" :max-width="maxWidthValue">
          <v-toolbar flat>
            <v-toolbar-title v-html="program.name"></v-toolbar-title>
          </v-toolbar>
          <v-divider />
          <v-card-text align="center" justify="center" class="px-8">
            <div v-if="progress === '0'">
              <v-row class="mt-5" align="start">
                <p class="text-body-1 ml-4">
                  Artista da Música:
                </p>
              </v-row>
              <v-text-field
                label="Artista"
                v-model="artist"
                name="artist"
                prepend-icon="mdi-account-music"
                type="text"
              ></v-text-field>
              <v-row class="mt-5" align="start">
                <p class="text-body-1 ml-4">
                  Título da Música:
                </p>
              </v-row>
              <v-text-field
                label="Título"
                v-model="title"
                name="title"
                prepend-icon="mdi-playlist-music"
                type="text"
              ></v-text-field>
              <v-row class="mt-5" align="start">
                <p class="text-body-1 ml-4">Ficheiro de emissão:</p>
              </v-row>
              <v-row align="center" justify="center" no-gutters>
                <v-col :cols="file != null ? 11 : 12">
                  <v-btn
                    color="secondary"
                    depressed
                    block
                    :loading="isSelecting"
                    @click="openFileChooser"
                    max-width="100%"
                    class="upload"
                  >
                    <v-icon left>
                      cloud_upload
                    </v-icon>
                    <span style="text-overflow:ellipsis; overflow: hidden">
                      {{ buttonText }}
                    </span>
                  </v-btn>
                  <input
                    ref="uploader"
                    class="d-none"
                    type="file"
                    accept="audio/*"
                    @change="onFileChanged"
                  />
                </v-col>
                <v-col v-if="file != null">
                  <v-btn icon @click="file = null">
                    <v-icon>mdi-close</v-icon>
                  </v-btn>
                </v-col>
              </v-row>
            </div>
            <v-expand-transition>
              <v-progress-circular
                v-if="progress > 0 && progress < 100"
                :rotate="360"
                :size="100"
                :width="15"
                :value="progress"
                color="primary"
                >{{ progress }}%</v-progress-circular
              >
            </v-expand-transition>
            <v-alert
              v-if="progress === '100'"
              :value="alert"
              type="error"
              transition="scale-transition"
              >{{ errorMessage }}</v-alert
            >
            <v-alert
              v-if="progress === '100'"
              :value="success"
              type="success"
              transition="scale-transition"
              >A música foi submetida com sucesso e encontra-se a ser
              processada. Se tudo correr bem, irás encontrá-la dentro de minutos
              na playlist.</v-alert
            >
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn
              v-if="progress === '0'"
              :loading="loading"
              @click="upload"
              :disabled="file == null"
              block
              raised
              >Enviar</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-row>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import BackendServices from "@/services/BackendServices";
import moment from "moment";

@Component
export default class PlaylistUploadView extends Vue {
  artist = "";
  title = "";
  file: File | null = null;
  loading = false;
  progress = "0";
  alert = false;
  success = false;
  errorMessage = "";
  isSelecting = false;
  defaultButtonText = "Escolher ficheiro";

  updateProgress(progressEvent: { loaded: number; total: number }) {
    this.progress = (
      (progressEvent.loaded * 100) /
      progressEvent.total
    ).toFixed(0);
  }

  upload() {
    this.loading = true;
    if (
      this.program != undefined &&
      this.file != null &&
      this.artist != undefined &&
      this.title != undefined
    )
      BackendServices.uploadPlaylist(
        this.artist,
        this.title,
        this.file,
        this.updateProgress
      ).then(() => {
        this.success = true;
        this.loading = false;
      });
  }

  onFileChanged(e: Event) {
    const input = e.target as HTMLInputElement;
    const files = input.files;
    if (files != null) this.file = files[0];
  }

  openFileChooser() {
    this.isSelecting = true;
    window.addEventListener(
      "focus",
      () => {
        this.isSelecting = false;
      },
      { once: true }
    );
    const element: HTMLElement = this.$refs.uploader as HTMLElement;
    element.click();
  }

  get buttonText() {
    return this.file != null
      ? this.file.name + " (" + (this.file.size / 1000000).toFixed(2) + " MB)"
      : this.defaultButtonText;
  }

  get maxWidthValue() {
    return this.$vuetify.breakpoint.smAndDown ? "90%" : "60%";
  }
}
</script>

<style>
.upload > span:nth-child(1) {
  /* to allow for upload button content overflow management */
  max-width: 100%;
}
</style>
