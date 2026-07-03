import axios from "axios";

export const api = axios.create({
  baseURL: "http://192.168.1.202:8088/api/v1",
  timeout: 15000,
});
