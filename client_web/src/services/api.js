import axios from "axios";

class ApiService {
  baseUrl = "http://localhost:8080/";

  get(url, headers, csrfToken, token) {
    if (headers === undefined)
      headers = {}
    headers['Content-Type'] = 'application/json'
    if (csrfToken)
      headers['X-CSRFToken'] = csrfToken
    if (token)
      headers['Authorization'] = 'Bearer ' + token
    return axios.get(this.baseUrl + url, { withCredentials:true, headers })
  }

  post(url, headers, data, csrfToken, token) {
    const jsonData = JSON.stringify(data)
    if (headers === undefined)
      headers = {}
    headers['Content-Type'] = 'application/json'
    if (csrfToken)
      headers['X-CSRFToken'] = csrfToken
    if (token)
      headers['Authorization'] = 'Bearer ' + token
    return axios.post(this.baseUrl + url, jsonData, {withCredentials: true, headers })
  }

  put(url, headers, data, csrfToken, token) {
    const jsonData = JSON.stringify(data)
    if (headers === undefined)
      headers = {}
    headers['Content-Type'] = 'application/json'
    if (csrfToken)
      headers['X-CSRFToken'] = csrfToken
    if (token)
      headers['Authorization'] = 'Bearer ' + token
    return axios.put(this.baseUrl + url, jsonData, {withCredentials: true, headers })
  }

  delete(url, headers, data, csrfToken, token) {
    const jsonData = JSON.stringify(data)
    if (headers === undefined)
      headers = {}
    headers['Content-Type'] = 'application/json'
    if (csrfToken)
      headers['X-CSRFToken'] = csrfToken
    if (token)
      headers['Authorization'] = 'Bearer ' + token
    return axios.delete(this.baseUrl + url, {headers: headers, data: jsonData, withCredentials: true})
  }
}
// eslint-disable-next-line
export default new ApiService();