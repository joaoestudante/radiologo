import axios from "axios";
import Store from "@/store";
import Schedule from "@/models/Schedule";

const httpClient = axios.create();
httpClient.defaults.timeout = 100000;
httpClient.defaults.baseURL =
  process.env.VUE_APP_ROOT_API || "http://localhost:8000";
httpClient.defaults.headers.post["Content-Type"] = "application/json";
httpClient.interceptors.request.use(
  (config) => {
    if (!config.headers.Authorization) {
      const token = Store.getters.getToken;

      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }

    return config;
  },
  (error) => Promise.reject(error)
);

export default class BackendServices {
  static async getWeeklySchedule(): Promise<Schedule> {
    return httpClient.get("/programs/schedule/").then((response) => {
      return response.data;
    });
  }
}
