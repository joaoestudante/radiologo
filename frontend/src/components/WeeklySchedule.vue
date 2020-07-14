<template>
  <v-row>
    <v-col>
      <v-card>
        <v-toolbar flat>
          <v-toolbar-title>Grelha de emissão</v-toolbar-title>
        </v-toolbar>
        <v-calendar
          ref="calendar"
          :events="events"
          color="primary"
          :event-color="getEventColor"
          type="week"
          interval-height="28"
          locale="pt-PT"
          :weekdays="mondayToSundayWeekdays"
          :weekday-format="weekdayFormatter"
          @click:event="showEvent"
        ></v-calendar>
        <v-menu
          v-model="selectedOpen"
          :close-on-content-click="false"
          :activator="selectedElement"
          offset-x
        >
          <v-card
            color="grey lighten-4"
            min-width="150px"
            max-width="550px"
            flat
          >
            <v-toolbar :color="selectedEvent.color" dark>
              <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
              <v-spacer></v-spacer>
              <span
                >{{ selectedEventStartTime }} - {{ selectedEventEndTime }}</span
              >
            </v-toolbar>
            <v-card-text>
              <span v-html="selectedEvent.description"></span>
            </v-card-text>
            <v-card-actions>
              <v-btn text color="secondary" @click="selectedOpen = false">
                Fechar
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-menu>
      </v-card>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import BackendServices from "@/services/BackendServices";
import ScheduleProgram from "@/models/ScheduleProgram";

@Component
export default class WeeklySchedule extends Vue {
  events: ScheduleProgram[] = [];
  selectedEvent: ScheduleProgram | {} = {};
  selectedElement = null;
  selectedOpen = false;
  selectedEventStartTime = "";
  selectedEventEndTime = "";

  mondayToSundayWeekdays = [1, 2, 3, 4, 5, 6, 0];
  async created() {
    const res = await BackendServices.getWeeklySchedule();
    for (const event of res.rerun) {
      event.color = "indigo lighten-1";
    }
    for (const event of res.normal) {
      event.color = "red darken-4";
    }
    this.events.push(...res.normal);
    this.events.push(...res.rerun);
  }

  getEventColor(event: ScheduleProgram) {
    return event.color;
  }

  showEvent({
    nativeEvent,
    event,
  }: {
    nativeEvent: any;
    event: ScheduleProgram;
  }) {
    const open = () => {
      this.selectedEvent = event;
      this.selectedEventStartTime = event.start.split(" ")[1];
      this.selectedEventEndTime = event.end.split(" ")[1];
      this.selectedElement = nativeEvent.target;
      setTimeout(() => (this.selectedOpen = true), 10);
    };

    if (this.selectedOpen) {
      this.selectedOpen = false;
      setTimeout(open, 10);
    } else {
      open();
    }

    nativeEvent.stopPropagation();
  }

  weekdayFormatter(arg: any) {
    return ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"][arg.weekday];
  }
}
</script>
<style>
.v-btn--fab.v-size--default {
  /* Circle around the current day in the calendar, default is 56px which is 
  too big in smaller displays */
  height: 26px;
  width: 26px;
}
</style>
