export default class Slot {
  iso_weekday!: string;
  time!: string;
  is_rerun!: boolean;

  constructor(jsonObj?: Slot) {
    if (jsonObj) {
      this.iso_weekday = jsonObj.iso_weekday;
      this.time = jsonObj.time;
      this.is_rerun = jsonObj.is_rerun;
    }
  }
}
