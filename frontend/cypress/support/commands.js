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
