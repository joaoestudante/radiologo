<template>
  <v-row>
    <v-col>
      <v-row align="center" justify="center">
        <v-card class="mx-4" max-width="650px">
          <v-toolbar flat>
            <v-toolbar-title>Arquivo de "{{ program.name }}"</v-toolbar-title>
          </v-toolbar>
          <v-divider></v-divider>
          <v-card-text>
            <v-date-picker
              v-model="date"
              :allowed-dates="allowedDates"
              full-width
              elevation="3"
            ></v-date-picker>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="downloadFile" block :disabled="!archiveFileExists"
              >Download da emissão para o dia {{ date }}</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-row>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import Program from "@/models/program/program";
import BackendServices from "@/services/BackendServices";
@Component
export default class ArchiveView extends Vue {
  program: Program | undefined;
  headers = [
    { text: "Data de emissão", value: "display_date", align: "left" },
    { text: "Download", value: "file_name", align: "right" }
  ];
  files = [];
  uploadedDates: string[] = [];
  search = "";
  date: string = new Date().toISOString().substr(0, 10);
  archiveFileExists = false;
  archiveFileUrl = "";
  archiveFilename = "";

  beforeCreate() {
    const id = this.$route.params.id;
    for (const program of this.$store.getters.getUser.programSet)
      if (program.id == id) {
        this.program = program;
      }
  }

  created() {
    if (this.program != undefined)
      BackendServices.getArchiveContents(this.program.id).then(response => {
        for (const file in response) {
          const date: string = response[file].display_date;
          this.uploadedDates.push(date);
        }
        this.files = response;
      });
  }

  allowedDates(val: string) {
    return this.uploadedDates.includes(val);
  }

  downloadFile() {
    BackendServices.getArchive(this.archiveFileUrl, this.archiveFilename);
  }

  @Watch("date")
  onPropertyChange(value: string) {
    this.archiveFileExists = this.uploadedDates.includes(value);
    if (this.archiveFileExists) {
      for (const file of this.files) {
        if (file["display_date"] == value) {
          if (this.program != undefined) {
            this.archiveFileUrl =
              process.env.VUE_APP_ROOT_API +
              "programs/" +
              this.program.id +
              "/archive/" +
              file["file_date"] +
              "/";
            this.archiveFilename =
              this.program.normalizedName + file["file_date"] + ".mp3";
          }
        }
      }
    }
  }
}
</script>
