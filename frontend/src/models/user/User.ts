import Program from "@/models/program/program";

export default class User {
  id!: number;
  authorName!: string;
  fullName!: string;
  idType!: string;
  idNumber!: string;
  istStudentOptions!: string;
  istStudentNumber!: string;
  phone!: string;
  state!: string;
  entranceDate!: string;
  department!: string;
  role!: string;
  notes: string | undefined;
  dateJoined!: string;
  exitDate: string | undefined;
  isActive!: boolean;
  isRegistered!: boolean;
  programSet!: Program[];

  constructor(jsonObj: any) {
    if (jsonObj) {
      this.id = jsonObj.id;
      this.authorName = jsonObj.author_name;
      this.fullName = jsonObj.full_name;
      this.idType = jsonObj.id_type;
      this.idNumber = jsonObj.id_number;
      this.istStudentOptions = jsonObj.ist_student_options;
      this.istStudentNumber = jsonObj.ist_student_number;
      this.phone = jsonObj.phone;
      this.state = jsonObj.state;
      this.entranceDate = jsonObj.entrance_date;
      this.department = jsonObj.department;
      this.role = jsonObj.role;
      this.notes = jsonObj.notes;
      this.dateJoined = jsonObj.date_joined;
      this.exitDate = jsonObj.exit_date;
      this.isActive = jsonObj.is_active;
      this.isRegistered = jsonObj.is_registered;
      if (jsonObj.program_set) {
        if (jsonObj.program_set.lenght != 0)
          this.programSet = jsonObj.program_set;
      } else this.programSet = [];
    }
  }
}
