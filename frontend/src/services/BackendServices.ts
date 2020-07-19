import axios from "axios";
import Store from "@/store";
import Schedule from "@/models/Schedule";
import AuthDto from "@/models/user/AuthDto";

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
    Store.commit("stopLoading");
    return Promise.reject(error);
  }
);

export default class BackendServices {
  static async getWeeklySchedule(): Promise<Schedule> {
    return httpClient.get("/programs/schedule/").then(response => {
      return response.data;
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
}
