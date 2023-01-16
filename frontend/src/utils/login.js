const checkLogin = async () => {
    const token = localStorage.getItem('token')
    try {
        const res = await fetch('/api/check-token', {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        const {data} = await res
        return data.success
    } catch (e) {
        const refresh_token = localStorage.getItem('refreshToken')
        if (!refresh_token) {
            localStorage.removeItem('token')
            return false
        } else {
            await fetch('/api/refreshtoken', {
                method:'POST',
                headers: {
                    Authorization: `Bearer ${refresh_token}`
                }
            })
            .then((res) => localStorage.setItem('token', res.data.token))
            return true
        }
    }
}

const logout = async () => {
    if (localStorage.getItem('token')) {
        const token = localStorage.getItem('token')
        await fetch('/api/logout/access', {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        .then((res) => {
            if (res.data.error) {
                console.error(res.data.error)
            } else {
                localStorage.removeItem('token')
            }
        })
    }

    if (localStorage.getItem('refreshToken')) {
        const refreshToken = localStorage.getItem('refreshToken')
        await fetch('/api/logout/refresh', {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${refreshToken}`
            }
        })
        .then((res) => {
            if (res.data.error) {
                console.error(res.data.error)
            } else {
                localStorage.removeItem('refreshToken')
            }
        })
    }
    localStorage.clear()
    setTimeout(() => window.location = '/', 500)
}

export {checkLogin, logout}