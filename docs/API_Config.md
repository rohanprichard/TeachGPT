---
layout: default
title: "API Configuration"
---

# API Configuration (Frontend)

This document describes how the API configuration is set up in the frontend.

## Overview
The file `frontend/client/src/components/apiConfig.js` selects the backend API URL based on the environment:

- **Development:** Uses the URL from `REACT_APP_API_URL_DEV`
- **Production:** Uses the URL from `REACT_APP_API_URL_PROD`

## Example Content 

```javascript
const env = process.env.NODE_ENV;
const apiConfig = {
development: process.env.REACT_APP_API_URL_DEV,
production: process.env.REACT_APP_API_URL_PROD,
};
export const apiUrl = apiConfig[env];
```

## Setup Recommendations
- Ensure that you have a `.env` file in your project root for both the client and admin frontends.
- The environment variables must be set so that the proper API URL is used according to the deployment stage.