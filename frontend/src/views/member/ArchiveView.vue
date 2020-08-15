<template>
  <v-row>
    <v-snackbar v-model="downloadStarted" top right timeout="4000"
      >Download iniciado...</v-snackbar
    >
    <v-col>
      <v-row align="center" justify="center">
        <v-card class="mx-4" max-width="650px" v-if="program !== null">
          <v-progress-linear
            v-if="downloadPercentage > 0 && downloadPercentage < 100"
            :value="downloadPercentage"
            stream
          ></v-progress-linear>
          <v-toolbar flat>
            <v-toolbar-title>Arquivo de "{{ program.name }}"</v-toolbar-title>
          </v-toolbar>
          <v-divider></v-divider>
          <v-card-text>
            <v-container fluid ma-0 pa-0 fill-height>
              <v-tabs v-model="tab" fixed-tabs class="mb-3" icons-and-text>
                <v-tab>Calendário <v-icon>mdi-calendar-today</v-icon></v-tab>
                <v-tab>Tabela <v-icon>mdi-table</v-icon></v-tab>
              </v-tabs>
              <v-tabs-items v-model="tab">
                <v-tab-item>
                  <v-date-picker
                    v-model="date"
                    :allowed-dates="allowedDates"
                    full-width
                    elevation="3"
                    locale="pt-pt"
                  ></v-date-picker>
                  <v-btn
                    class="mt-4"
                    @click="downloadFile('', '')"
                    block
                    :disabled="!archiveFileExists"
                    >Download da emissão de {{ date }}</v-btn
                  >
                </v-tab-item>
                <v-tab-item>
                  <v-data-table
                    style="flex: 1 1 auto"
                    :headers="headers"
                    :items="files"
                    full-width
                  >
                    <template v-slot:item.file_name="{ item }">
                      <v-btn
                        icon
                        :key="item.file_date"
                        @click="
                          downloadFile(
                            item.file_date,
                            item.file_name,
                            item.bytes
                          )
                        "
                      >
                        <v-icon>mdi-download</v-icon>
                      </v-btn>
                    </template>
                  </v-data-table>
                </v-tab-item>
              </v-tabs-items>
            </v-container>
          </v-card-text>
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
  program: Program | null = null;
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
  archiveFilesize = 0;
  tab = null;
  downloadPercentage = 0;
  downloadStarted: boolean | null = null;

  created() {
    const id = this.$route.params.id;
    for (const program of this.$store.getters.getUser.programSet)
      if (program.id == id) {
        this.program = program;
        this.getArchiveContents();
      }
    if (this.program == null) {
      const hasPermission = true; // check here for permission
      if (hasPermission) {
        BackendServices.getProgram(this.$route.params.id).then(program => {
          this.program = program;
          this.getArchiveContents();
        });
      } else {
        alert("no permission"); // redirect to 'no permission page' or load a 'no permission' component
      }
    }
  }

  getArchiveContents() {
    if (this.program != null) {
      BackendServices.getArchiveContents(this.program.id).then(response => {
        for (const file in response) {
          const date: string = response[file].display_date;
          this.uploadedDates.push(date);
        }
        this.files = response;
      });
    }
  }

  allowedDates(val: string) {
    return this.uploadedDates.includes(val);
  }

  downloadProgress(downloaded: number) {
    if (this.downloadStarted == null) this.downloadStarted = true;
    this.downloadPercentage = downloaded;
  }

  downloadFile(date: string, filename: string, filesize: number) {
    if (date != "" && this.program != null)
      // called by table
      BackendServices.getArchive(
        process.env.VUE_APP_ROOT_API +
          "/programs/" +
          this.program.id +
          "/archive/" +
          date +
          "/",
        filename,
        filesize,
        this.downloadProgress
      );
    else
      BackendServices.getArchive(
        this.archiveFileUrl,
        this.archiveFilename,
        this.archiveFilesize,
        this.downloadProgress
      );
  }

  @Watch("date")
  onPropertyChange(value: string) {
    this.archiveFileExists = this.uploadedDates.includes(value);
    if (this.archiveFileExists) {
      for (const file of this.files) {
        if (file["display_date"] == value) {
          if (this.program != null) {
            this.archiveFileUrl =
              process.env.VUE_APP_ROOT_API +
              "/programs/" +
              this.program.id +
              "/archive/" +
              file["file_date"] +
              "/";
            this.archiveFilename = file["file_name"];
            this.archiveFilesize = file["bytes"];
          }
        }
      }
    }
  }
}
</script>
