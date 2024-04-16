import { configureStore } from "@reduxjs/toolkit";
import userReducer from 'features/user/user-slice'

export const store = configureStore({
    reducer: {
        auth: userReducer,
    },
});

export default store;