import axios from 'axios'

const api = axios.create({
    baseURL:
        import.meta.env.VITE_API_URL ||
        `${window.location.protocol}//${window.location.hostname}:8000/api`,
    timeout: 120000,
})

const errHandler = async (error) => {
    const response = error.response
    if (response) {
        switch (response.status) {
            case 401:
                // TODO: refresh token according to your backend
                // if (userStore.token) {
                //   return userStore.refreshToken().then((resp) => {
                //     return api(error.response!.config)
                //   })
                // }
                break
        }
        if (!response.headers['content-type']?.includes('text/html')) {
            throw response.data
        }
    }
    throw error
}

// Request interceptors
api.interceptors.request.use(
    async (config) => {
        // Add X-Access-Token header to every request, you can add other custom headers here
        const token = localStorage.getItem("token")
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    }
    // Add Error Handler Below
)

// Response interceptors
api.interceptors.response.use((response) => {
    return response
}, errHandler)

export default api
