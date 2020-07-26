import axios from "axios";
import Store from "@/store";
import Schedule from "@/models/Schedule";
import AuthDto from "@/models/user/AuthDto";
import router from "@/router";
import User from "@/models/user/User";
import FileSaver from "file-saver";

const httpClient = axios.create();
httpClient.defaults.timeout = 100000;
httpClient.defaults.baseURL =
  process.env.VUE_APP_ROOT_API || "http://localhost:8000";
httpClient.defaults.headers.post["Content-Type"] = "application/json";
httpClient.interceptors.request.use(
  config => {
    if (!config.headers.Authorization) {
      const token = Store.getters.getToken;

      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    Store.commit("startLoading");

    return config;
  },
  error => {
    Store.commit("startLoading");
    Promise.reject(error);
  }
);

httpClient.interceptors.response.use(
  config => {
    Store.commit("stopLoading");
    return config;
  },
  error => {
    if (error.response.status === 401) {
      Store.commit("logout");
      Store.commit("stopLoading");
      router.push({ name: "login" });
      return Promise.resolve();
    }
    Store.commit("stopLoading");
    return Promise.reject(error);
  }
);

export default class BackendServices {
  static async getWeeklySchedule(): Promise<Schedule> {
    return httpClient
      .get("/programs/schedule/")
      .then(response => {
        return response.data;
      })
      .catch(error => {
        console.log(error);
      });
  }

  static async login(email: string, password: string): Promise<AuthDto> {
    return httpClient
      .post("/token/", { email: email, password: password })
      .then(response => {
        return new AuthDto(response.data);
      })
      .catch(error => {
        return Promise.reject(error);
      });
  }

  static async getUploadedDates(programId: string): Promise<string[]> {
    return httpClient
      .get("/programs/" + programId + "/upload/uploaded-dates/")
      .then(response => {
        return Promise.resolve(response.data);
      });
  }

  static async updateUserData(): Promise<User> {
    return httpClient
      .get("/users/" + Store.getters.getUser.id + "/")
      .then(response => {
        const newUser = new User(response.data);
        Store.commit("updateUser", newUser);
        return Promise.resolve(newUser);
      });
  }

  static async uploadProgram(
    programId: number,
    file: File,
    date: string,
    progressUpdater: Function
  ): Promise<any> {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("date", date);
    return httpClient
      .put("/programs/" + programId + "/upload/", formData, {
        timeout: 60 * 10 * 1000,
        onUploadProgress: progressEvent => progressUpdater(progressEvent)
      })
      .then(() => {
        return Promise.resolve();
      });
  }

  static async getArchiveContents(programId: number): Promise<any> {
    return httpClient
      .get("/programs/" + programId + "/archive/")
      .then(response => {
        return response.data;
      });
  }

  static async getArchive(url: string, outputFilename: string): Promise<any> {
    httpClient
      .get(url, {
        responseType: "blob",
        timeout: 30000
      })
      .then(response => {
        FileSaver.saveAs(response.data, outputFilename);
        Promise.resolve();
      });
  }
}
