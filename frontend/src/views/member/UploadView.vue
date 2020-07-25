<template>
  <v-row>
    <v-col>
      <v-row align="center" justify="center">
        <v-card class="mx-4" max-width="650px">
          <v-toolbar flat>
            <v-toolbar-title v-html="program.name"></v-toolbar-title>
          </v-toolbar>
          <v-divider />
          <v-card-text align="center">
            <div v-if="progress === '0'">
              <v-row align="start">
                <p class="text-body-1 ml-3">
                  Data da emissão:
                </p>
              </v-row>
              <v-date-picker
                v-model="date"
                locale="pt-pt"
                :allowed-dates="allowedDates"
                full-width
                elevation="3"
                color="secondary"
                ref="datePicker"
              ></v-date-picker>
              <br />
              <v-file-input
                label="Ficheiro de emissão"
                outlined
                dense
                show-size
                v-model="file"
              ></v-file-input>
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
              >O programa foi submetido com sucesso e encontra-se a ser
              processado. Se tudo correr bem, irás receber um e-mail com mais
              informações.</v-alert
            >
          </v-card-text>
          <v-card-actions>
            <v-btn v-if="progress === '0'" :loading="loading" @click="upload"
              >Upload</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-row>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Program from "@/models/program/program";
import BackendServices from "@/services/BackendServices";
import moment from "moment";

@Component
export default class UploadView extends Vue {
  program: Program | undefined;
  date: string | undefined = "";
  loading = false;
  alreadyUploadedDates: string[] = [];
  file: File | null = null;
  progress = "0";
  alert = false;
  success = false;
  errorMessage = "";

  beforeCreate() {
    const id = this.$route.params.id;
    BackendServices.updateUserData();
    for (const program of this.$store.getters.getUser.programSet)
      if (program.id == id) {
        this.program = program;
        BackendServices.getUploadedDates(id).then(dates => {
          this.alreadyUploadedDates = dates;
          this.date = program.nextUploadDate;
        });
      }
  }

  allowedDates(val: string) {
    const dt = moment(val);
    const weekday = dt.isoWeekday();
    return (
      this.program?.enabledDays.includes(weekday) &&
      !this.alreadyUploadedDates.includes(val)
    );
  }

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
      this.date != undefined
    )
      BackendServices.uploadProgram(
        this.program?.id,
        this.file,
        this.date.replaceAll("-", ""),
        this.updateProgress
      ).then(() => {
        this.success = true;
        this.loading = false;
      });
  }
}
</script>
