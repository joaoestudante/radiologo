export default class ScheduleProgram {
  name!: string;
  description!: string;
  start!: string;
  end!: string;
  color: string = "";

  constructor(jsonObj?: ScheduleProgram) {
    if (jsonObj) {
      this.name = jsonObj.name;
      this.description = jsonObj.description;
      this.start = jsonObj.start;
      this.end = jsonObj.end;
    }
  }
}
