import User from "@/models/user/User";

export default class AuthDto {
  refresh!: string;
  access!: string;
  user!: User;

  constructor(jsonObj?: AuthDto) {
    if (jsonObj) {
      this.refresh = jsonObj.refresh;
      this.access = jsonObj.access;
      this.user = new User(jsonObj.user);
    }
  }
}
