// import { env } from "process";
const env = "test";
export const API_BASE_URL =
  env?.REACT_APP_API_BASE_URL || "http://localhost:8000";
export const API_TIMEOUT = 10000; // 10 seconds

export const API_HEADERS = {
  "Content-Type": "application/json",
  Accept: "application/json",
};

export const API_AUTH_HEADERS = {
  ...API_HEADERS,
  Authorization: `Bearer ${localStorage.getItem("token")}`,
};
