const env = process.env.NODE_ENV;

const apiConfig = {
    development: process.env.REACT_APP_API_URL_DEV,
    production: process.env.REACT_APP_API_URL_PROD,
};

export const apiUrl = apiConfig[env];
