// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This is will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })
import Config from '../../src/config.js'

Cypress.Commands.add('zxcvbnApi', () => {
  cy.server()
  let strengths = [0, 25, 50, 75, 100]
  strengths.forEach(strength => {
    cy.route('GET', `${Config.apiURL}/api/v1/zxcvbn?input=${strength}password`, {strength}).as(`zxcvbn${strength}`)
  })
})

Cypress.Commands.add('activateApi', () => {
  cy.server()
  cy.route({
    delay: 2000,
    method: 'POST',
    url: `${Config.apiURL}/api/v1/activate/valid_token`,
    response: {
      message: 'ok'
    },
    status: 200
  }).as('activateValid')
  cy.route({
    delay: 2000,
    method: 'POST',
    url: `${Config.apiURL}/api/v1/activate/invalid_token`,
    response: {
      message: 'Messaggio di errore'
    },
    status: 404
  }).as('activateInvalid')
})

Cypress.Commands.add('loggedInApi', () => {
  cy.server()
  cy.route('GET', `${Config.apiURL}/api/v1/user`, {
    name: 'User',
    surname: 'Test',
    id: 1,
    privileges: 2,
    gravatar_hash: 'gravatar-hash'
  }).as('userData')
})

Cypress.Commands.add('notLoggedInApi', () => {
  cy.server()
  cy.route({
    method: 'GET',
    url: `${Config.apiURL}/api/v1/user`,
    response: {
      message: 'Messaggio di errore'
    },
    status: 401
  }).as('userData')
})
