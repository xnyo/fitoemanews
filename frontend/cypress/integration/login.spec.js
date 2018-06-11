import Config from '../../src/config.js'

describe('Login', () => {
  it('Accepts valid input', () => {
    cy.visit('/login')
    cy.get(':nth-child(1) > .control > .input').type('email@addr.es').should('have.value', 'email@addr.es')
    cy.get(':nth-child(2) > .control > .input').type('password').should('have.value', 'password')
  })

  it('Does not accept empty fields', () => {
    cy.visit('/login')
    cy.get(':nth-child(3) > .button').click()
    cy.get(':nth-child(1) > .control > .input').should('have.class', 'is-danger')
    cy.get(':nth-child(1) > .help').should('have.text', 'Per favore, inserisci la tua email')
    cy.get(':nth-child(2) > .control > .input').should('have.class', 'is-danger')
    cy.get(':nth-child(2) > .help').should('have.text', 'Per favore, inserisci la tua password')
  })

  it('Does not accept invalid emails', () => {
    cy.visit('/login')
    cy.get(':nth-child(1) > .control > .input').type('...').blur({force: true}).should('have.class', 'is-danger')
  })

  it('Logs in with valid credentials', () => {
    cy.notLoggedInApi()
    cy.route('POST', `${Config.apiURL}/api/v1/login`, {message: 'ok'}).as(`login`)

    cy.visit('/login')
    cy.wait('@userData')
    cy.route('GET', `${Config.apiURL}/api/v1/user`, {})
    cy.get(':nth-child(1) > .control > .input').type('email@addr.es')
    cy.get(':nth-child(2) > .control > .input').type('password')
    cy.get(':nth-child(3) > .button').click()
    cy.wait('@login')
    cy.location('pathname').should('eq', '/')
  })

  it('Displays message with wrong credentials', () => {
    cy.server()
    cy.route({
      method: 'POST',
      url: `${Config.apiURL}/api/v1/login`,
      response: {
        message: 'Messaggio di errore'
      },
      status: 404
    }).as('login')

    cy.visit('/login')
    cy.get(':nth-child(1) > .control > .input').type('email@addr.es')
    cy.get(':nth-child(2) > .control > .input').type('password')
    cy.get(':nth-child(3) > .button').click()
    cy.wait('@login')
    cy.get('.toast').should('have.text', 'Messaggio di errore')
    cy.location('pathname').should('eq', '/login')
  })

  it('Displays user info in navbar when logged in', () => {
    cy.loggedInApi()
    cy.visit('/')
    cy.wait('@userData')
    cy.get('.navbar-link').should('contain', 'User Test')
    cy.get('.avatar').should('have.attr', 'src', 'https://gravatar.com/avatar/gravatar-hash')
  })

  it('Display login button in navbar when logged in', () => {
    cy.notLoggedInApi()
    cy.visit('/login')
    cy.wait('@userData')
    cy.get('.navbar-end > .navbar-item').should('contain', 'Login')
  })
})
