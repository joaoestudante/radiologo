/* eslint-disable @typescript-eslint/camelcase */
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

  constructor(jsonObj?: any) {
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
      this.slotSet = jsonObj.slot_set.map((slotJson: Slot) => {
        return new Slot(slotJson);
      });
      this.authors = jsonObj.authors.map((authorJson: any) => {
        return new ShortUser(authorJson);
      });
      this.enabledDays = jsonObj.enabled_days;
    } else {
      this.id = 0;
      this.name = "";
      this.normalizedName = "";
      this.description = "";
      this.maxDuration = 0;
      this.firstEmissionDate = "";
      this.comesNormalized = false;
      this.ignoreDurationAdjustment = false;
      this.isExternal = false;
      this.state = "";
      this.slotSet = [];
      this.authors = [];
      this.enabledDays = [];
    }
  }

  static stateItems() {
    return [
      { text: "Activo", value: "A" },
      { text: "Em hiato", value: "H" },
      { text: "Terminado", value: "T" }
    ];
  }

  static durationItems() {
    return [
      { text: "28", value: 28 },
      { text: "57", value: 57 },
      { text: "117", value: 117 }
    ];
  }

  static weekItems() {
    return [
      { text: "Segunda", value: 1 },
      { text: "Terça", value: 2 },
      { text: "Quarta", value: 3 },
      { text: "Quinta", value: 4 },
      { text: "Sexta", value: 5 },
      { text: "Sábado", value: 6 },
      { text: "Domingo", value: 7 }
    ];
  }

  toJson() {
    return {
      id: this.id,
      name: this.name,
      normalized_name: this.normalizedName,
      description: this.description,
      max_duration: this.maxDuration,
      first_emission_date: this.firstEmissionDate,
      comes_normalized: this.comesNormalized,
      ignore_duration_adjustment: this.ignoreDurationAdjustment,
      is_external: this.isExternal,
      state: this.state,
      slot_set: this.slotSet.map(slot => {
        console.log(slot);
        return slot.toJson();
      }),
      authors: this.authors.map(author => {
        return author.toJson();
      })
    };
  }
}
