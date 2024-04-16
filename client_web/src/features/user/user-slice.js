import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    csrfToken: "",
    user: undefined
};

const userSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setToken(state, action) {
            state.csrfToken = action.payload
            console.log(state.csrfToken)
        },
        setUser(state, action) {
            state.user = action.payload
        },
        mergeUser(state, action) {
            state.user = { ...state.user, ...action.payload };
        }
    }
})

export const { setToken, setUser, mergeUser } = userSlice.actions;
export default userSlice.reducer