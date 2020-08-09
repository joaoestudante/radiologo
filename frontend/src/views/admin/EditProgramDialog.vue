<template>
  <v-dialog
    :value="dialog"
    @input="closeDialog"
    @keydown.esc="closeDialog"
    scrollable
    persistent
  >
    <v-card>
      <v-toolbar flat>
        <v-toolbar-title v-if="program.id === 0">Novo programa</v-toolbar-title>
        <v-toolbar-title v-else>Editar {{ program.name }}</v-toolbar-title>
      </v-toolbar>
      <v-divider></v-divider>
      <v-card-text>
        <v-form
          ref="form"
          v-model="valid"
          lazy-validation
          v-if="!confirmDelete"
        >
          <v-row class="mt-3">
            <p class="title text-left" id="title">Informações básicas</p>
          </v-row>
          <v-row>
            <v-col>
              <v-row>
                <v-text-field
                  label="Nome"
                  outlined
                  v-model="editedProgram.name"
                  :rules="[v => !!v || 'O nome do programa é obrigatório']"
                  id="test-error"
                >
                </v-text-field>
              </v-row>
              <v-row>
                <v-textarea
                  label="Descrição"
                  outlined
                  rows="4"
                  v-model="editedProgram.description"
                  :rules="[v => !!v || 'A descrição é obrigatória']"
                ></v-textarea>
              </v-row>
              <v-row>
                <v-autocomplete
                  v-model="editedProgram.authors"
                  :items="allUsers"
                  chips
                  deletable-chips
                  item-text="authorName"
                  :item-value="buildAuthor"
                  label="Autores"
                  hint="Caso o programa não seja da autoria de um membro da Rádio Zero, escolhe o autor 'Externo'."
                  persistent-hint
                  multiple
                  outlined
                >
                </v-autocomplete>
              </v-row>
              <v-row class="mt-4">
                <v-menu
                  ref="menu"
                  v-model="menu"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  :return-value.sync="editedProgram.firstEmissionDate"
                  transition="scale-transition"
                  offset-y
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      v-model="editedProgram.firstEmissionDate"
                      label="Dia da primeira emissão"
                      append-icon="event"
                      outlined
                      readonly
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="editedProgram.firstEmissionDate"
                    scrollable
                    color="primary"
                    locale="pt-pt"
                  >
                    <v-spacer></v-spacer>
                    <v-btn text color="primary" @click="menu = false"
                      >Cancel</v-btn
                    >
                    <v-btn
                      text
                      color="primary"
                      @click="$refs.menu.save(editedProgram.firstEmissionDate)"
                      >OK</v-btn
                    >
                  </v-date-picker>
                </v-menu>
              </v-row>
              <v-row>
                <v-checkbox
                  v-model="editedProgram.comesNormalized"
                  label="Vem normalizado (não será efectuado ajuste automático de áudio)"
                ></v-checkbox>
              </v-row>
              <v-row>
                <v-checkbox
                  v-model="editedProgram.ignoreDurationAdjustment"
                  label="Não efectuar ajuste automático de duração"
                ></v-checkbox>
              </v-row>
              <v-divider></v-divider>
              <v-row class="mt-3">
                <p class="title text-left">Informações de grelha</p>
              </v-row>
              <v-row>
                <v-select
                  v-model="editedProgram.state"
                  :items="stateItems"
                  outlined
                  label="Estado"
                ></v-select>
              </v-row>
              <v-row>
                <v-select
                  v-model="editedProgram.maxDuration"
                  :items="durationItems"
                  outlined
                  label="Duração"
                  @change="updatePossibleSlots"
                  :disabled="editedProgram.state !== 'A'"
                ></v-select>
              </v-row>
              <v-row>
                <v-select
                  v-model="editedProgram.enabledDays"
                  :items="weekItems"
                  multiple
                  outlined
                  label="Dias de emissão"
                  @change="updatePossibleSlots"
                  :disabled="editedProgram.state !== 'A'"
                ></v-select>
              </v-row>
              <v-row>
                <v-select
                  v-model="newSlotTime"
                  :items="possibleSlots"
                  outlined
                  label="Hora de emissão"
                  :disabled="editedProgram.state !== 'A'"
                ></v-select>
              </v-row>
            </v-col>
          </v-row>
        </v-form>
        <div v-if="confirmDelete">
          <v-row>
            <v-col>
              <v-row>
                <p class="text-h4">
                  De certeza que queres apagar este programa?
                </p>
              </v-row>
              <v-row>
                <p class="text-body-1">
                  Escreve '{{ program.name }}' na caixa em baixo para confirmar.
                </p>
              </v-row>
              <v-row align="center" justify="center">
                <v-text-field filled v-model="confirmDeleteName">
                </v-text-field>
              </v-row>
              <v-row>
                <v-btn
                  color="error"
                  :disabled="confirmDeleteName !== editedProgram.name"
                  block
                  @click="deleteProgram"
                  >Eu aceito as consequências, apagar este programa</v-btn
                >
              </v-row>
            </v-col>
          </v-row>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="closeDialog">Fechar</v-btn>
        <v-btn
          v-if="editedProgram.id !== 0 && !confirmDelete"
          text
          @click="confirmDelete = true"
          color="error"
          >Apagar</v-btn
        >
        <v-btn text @click="saveProgram" color="success" v-if="!confirmDelete"
          >Guardar</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
/* eslint-disable @typescript-eslint/camelcase */
import { Component, Model, Prop, Vue, Watch } from "vue-property-decorator";
import Program from "@/models/program/program";
import User from "@/models/user/User";
import BackendServices from "@/services/BackendServices";
import Slot from "@/models/program/slot";
import ShortUser from "@/models/user/ShortUser";

@Component
export default class EditProgramDialog extends Vue {
  @Prop(Program) program: Program | undefined;
  @Model("dialog", Boolean) dialog!: boolean;

  editedProgram: Program = new Program();
  allUsers: User[] = [];
  menu = false;
  stateItems = Program.stateItems();
  durationItems = Program.durationItems();
  weekItems = Program.weekItems();
  possibleSlots: { text: string; disabled: boolean }[] = [];
  newSlotTime: { text: string; disabled: boolean } = {
    text: "",
    disabled: true
  };
  valid = true;
  confirmDelete = false;
  confirmDeleteName = "";

  created() {
    this.updateProgram();
    console.log("updated program");
    BackendServices.getAllUsers().then(usersList => {
      this.allUsers = usersList;
    });
    this.updatePossibleSlots();
  }

  updatePossibleSlots() {
    BackendServices.getAllFreeSlots(
      this.editedProgram.id,
      this.editedProgram.enabledDays,
      this.editedProgram.maxDuration
    ).then(slots => {
      this.possibleSlots = [];
      for (const slot of Slot.getAllPossibleSlots()) {
        if (slots.includes(slot))
          this.possibleSlots.push({ text: slot, disabled: false });
        else this.possibleSlots.push({ text: slot, disabled: true });
      }
    });
  }

  @Watch("dialog", { immediate: true, deep: true }) // dialog opens/close
  updateProgram() {
    if (this.dialog) {
      if (this.program != undefined) {
        if (this.program.slotSet.length > 0)
          this.newSlotTime = {
            text: this.program.slotSet[0].time,
            disabled: false
          };
      }

      this.editedProgram = Object.assign(this.editedProgram, this.program); // copy
    }
  }

  buildAuthor(value: User) {
    return new ShortUser({ id: value.id, author_name: value.authorName });
  }

  saveProgram() {
    const form = this.$refs.form as HTMLFormElement;
    if (form.validate()) {
      this.editedProgram.slotSet = this.editedProgram.enabledDays.map(day => {
        return new Slot({
          iso_weekday: day,
          time: this.newSlotTime,
          is_rerun: false
        }); //TODO change here when implementing rerun
      });
      if (this.program != undefined) {
        if (this.program.id != 0) {
          BackendServices.updateProgram(this.editedProgram)
            .then(() => {
              this.$emit("program-saved", true);
              this.closeDialog();
            })
            .catch(error => {
              console.log("ERROR occured");
              console.log(error);
            });
        } else {
          BackendServices.createProgram(this.editedProgram)
            .then(() => {
              this.$emit("program-saved", true);
              this.closeDialog();
            })
            .catch(error => {
              console.log("ERROR occured");
              console.log(error);
            });
        }
      }
    } else {
      /* Not ideal, I'd prefer to go to the first element with an error */
      //this.$vuetify.goTo("#title");
      const el = document.querySelector("#title") as HTMLElement;
      el.scrollIntoView();
    }
  }

  deleteProgram() {
    BackendServices.deleteProgram(this.editedProgram.id).then(() => {
      this.closeDialog();
    });
  }

  closeDialog() {
    this.editedProgram = new Program();
    this.valid = true;
    this.confirmDelete = false;
    this.confirmDeleteName = "";
    this.$emit("program-saved", true);
    this.$emit("dialog", false);
  }
}
</script>
