export default class Slot {
  isoWeekday!: string;
  time!: string;
  isRerun!: boolean;

  constructor(jsonObj: any) {
    if (jsonObj) {
      this.isoWeekday = jsonObj.iso_weekday;
      this.time = jsonObj.time;
      this.isRerun = jsonObj.is_rerun;
    }
  }

  static getAllPossibleSlots() {
    return [
      "00:03",
      "00:32",
      "01:03",
      "01:32",
      "02:03",
      "02:32",
      "03:03",
      "03:32",
      "04:03",
      "04:32",
      "05:03",
      "05:32",
      "06:03",
      "06:32",
      "07:03",
      "07:32",
      "08:03",
      "08:32",
      "09:03",
      "09:32",
      "10:03",
      "10:32",
      "11:03",
      "11:32",
      "12:03",
      "12:32",
      "13:03",
      "13:32",
      "14:03",
      "14:32",
      "15:03",
      "15:32",
      "16:03",
      "16:32",
      "17:03",
      "17:32",
      "18:03",
      "18:32",
      "19:03",
      "19:32",
      "20:03",
      "20:32",
      "21:03",
      "21:32",
      "22:03",
      "22:32",
      "23:03",
      "23:32"
    ];
  }
}
