/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: dev-hpls-y2y.us.auth0.com,
    audience: drinks, // the audience set for the auth0 app
    clientId: NwwNUsx1e3vy1MQ8LIzfTi6UlHGb6hon, // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
