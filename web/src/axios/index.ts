import axios from "axios";

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api",
  timeout: 35000,
})

http.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    const detail = error.response?.data?.detail
    const message = typeof detail === "string" ? detail : "请求服务器失败"

    window.$message?.error(message)

    return Promise.reject(error)
  }
)

export default http;
