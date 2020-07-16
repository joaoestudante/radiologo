import ScheduleProgram from "./ScheduleProgram";

export default class Schedule {
  normal!: ScheduleProgram[];
  rerun!: ScheduleProgram[];

  constructor(jsonObj?: Schedule) {
    if (jsonObj) {
      this.normal = jsonObj.normal;
      this.rerun = jsonObj.rerun;
    }
  }
}
