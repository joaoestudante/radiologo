import ShortUser from "@/models/user/ShortUser";
import Slot from "@/models/program/slot";

export default class Program {
  id!: number;
  name!: string;
  description!: string;
  max_duration!: number;
  first_emission_date!: string;
  comes_normalized!: boolean;
  ignore_duration_adjustment!: boolean;
  is_external!: boolean;
  state!: string;
  slot_set!: Slot[];
  authors!: ShortUser[];

  constructor(jsonObj?: Program) {
    if (jsonObj) {
      this.id = jsonObj.id;
      this.name = jsonObj.name;
      this.description = jsonObj.description;
      this.max_duration = jsonObj.max_duration;
      this.first_emission_date = jsonObj.first_emission_date;
      this.comes_normalized = jsonObj.comes_normalized;
      this.ignore_duration_adjustment = jsonObj.ignore_duration_adjustment;
      this.is_external = jsonObj.is_external;
      this.state = jsonObj.state;
      this.slot_set = jsonObj.slot_set;
      this.authors = jsonObj.authors;
    }
  }
}
