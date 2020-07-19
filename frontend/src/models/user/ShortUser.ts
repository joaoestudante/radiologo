export default class ShortUser {
  id!: number;
  authorName!: string;

  constructor(jsonObj?: any) {
    if (jsonObj) {
      this.id = jsonObj.id;
      this.authorName = jsonObj.author_name;
    }
  }
}
