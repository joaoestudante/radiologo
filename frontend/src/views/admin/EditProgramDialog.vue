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
        <v-toolbar-title v-if="program === undefined"
          >Novo programa</v-toolbar-title
        >
        <v-toolbar-title v-if="program !== undefined"
          >Editar {{ program.name }}</v-toolbar-title
        >
      </v-toolbar>
      <v-divider></v-divider>
      <v-card-text>
        <v-row class="mt-3">
          <p class="title text-left">Informações básicas</p>
        </v-row>
        <v-row>
          <v-col>
            <v-row>
              <v-text-field label="Nome" outlined v-model="editedProgram.name">
              </v-text-field>
            </v-row>
            <v-row>
              <v-textarea
                label="Descrição"
                outlined
                rows="4"
                v-model="editedProgram.description"
              ></v-textarea>
            </v-row>
            <v-row>
              <v-autocomplete
                v-model="editedProgram.authors"
                :items="allUsers"
                chips
                deletable-chips
                item-text="authorName"
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
              ></v-select>
            </v-row>
            <v-row>
              <v-select
                v-model="editedProgram.enabledDays"
                :items="weekItems"
                multiple
                outlined
                label="Dias de emissão"
              ></v-select>
            </v-row>
            <v-row>
              <v-select
                v-model="newSlotTime"
                :items="possibleSlots"
                outlined
                label="Hora de emissão"
              ></v-select>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="closeDialog">Fechar</v-btn>
        <v-btn text @click="saveProgram">Guardar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue, Model, Watch } from "vue-property-decorator";
import Program from "@/models/program/program";
import User from "@/models/user/User";
import BackendServices from "@/services/BackendServices";
import Slot from "@/models/program/slot";

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
  freeSlots = [];
  possibleSlots: { text: string; disabled: boolean }[] = [];
  newSlotTime: { text: string; disabled: boolean } = {
    text: "",
    disabled: true
  };

  mounted() {
    this.updateProgram();
    console.log("updated program");
    BackendServices.getAllUsers().then(usersList => {
      this.allUsers = usersList;
    });
    BackendServices.getAllFreeSlots(this.editedProgram.id).then(slots => {
      this.freeSlots = slots;
      for (const weekday of this.editedProgram.enabledDays) {
        for (const slot of Slot.getAllPossibleSlots()) {
          const weekdaySlots: string[] = this.freeSlots[weekday];
          if (!weekdaySlots.includes(slot)) {
            this.possibleSlots.push({ text: slot, disabled: true });
            console.log("Weekday " + weekday + " does not include " + slot);
          } else {
            this.possibleSlots.push({ text: slot, disabled: false });
          }
        }
      }
    });
  }

  @Watch("dialog", { immediate: true, deep: true }) // dialog opens/close
  updateProgram() {
    if (this.dialog) {
      console.log("in updating program");
      if (this.program == undefined) this.program = new Program();
      else {
        if (this.program.slotSet.length > 0)
          this.newSlotTime = {
            text: this.program.slotSet[0].time,
            disabled: false
          };
      }
      this.editedProgram = Object.assign(this.editedProgram, this.program); // copy
    }
  }

  saveProgram() {
    console.log(this.editedProgram?.name);
    this.closeDialog();
  }

  closeDialog() {
    this.editedProgram = new Program();
    this.$emit("dialog", false);
  }
}
</script>
