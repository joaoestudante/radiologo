import ShortUser from "@/models/user/ShortUser";
import Slot from "@/models/program/slot";

export default class Program {
  id!: number;
  name!: string;
  normalizedName!: string;
  description!: string;
  maxDuration!: number;
  firstEmissionDate!: string;
  comesNormalized!: boolean;
  ignoreDurationAdjustment!: boolean;
  isExternal!: boolean;
  state!: string;
  slotSet!: Slot[];
  authors!: ShortUser[];
  enabledDays!: number[];
  nextUploadDate!: string;

  constructor(jsonObj: any) {
    if (jsonObj) {
      this.id = jsonObj.id;
      this.name = jsonObj.name;
      this.normalizedName = jsonObj.normalized_name;
      this.description = jsonObj.description;
      this.maxDuration = jsonObj.max_duration;
      this.firstEmissionDate = jsonObj.first_emission_date;
      this.comesNormalized = jsonObj.comes_normalized;
      this.ignoreDurationAdjustment = jsonObj.ignore_duration_adjustment;
      this.isExternal = jsonObj.is_external;
      this.state = jsonObj.state;
      this.slotSet = jsonObj.slot_set;
      this.authors = jsonObj.authors;
      this.enabledDays = jsonObj.enabled_days;
      this.nextUploadDate = jsonObj.next_upload_date;
    }
  }
}
