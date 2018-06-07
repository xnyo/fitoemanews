import Config from '../../src/config.js'

describe('Sign Up', () => {
  it('Accepts input', () => {
    cy.visit('/signup')

    let nthChildren = [1, 2, 3, 4, 6]
    let value = 'Test'
    nthChildren.forEach(element => {
      cy.get(`:nth-child(${element}) > .control > .input`).type(value).should('have.value', value)
    })
  })

  it('Accepts valid input', () => {
    cy.visit('/signup')

    let inputs = [
      {
        selector: ':nth-child(1) > .control > .input',
        value: 'Nome'
      }, {
        selector: ':nth-child(2) > .control > .input',
        value: 'Cognome'
      }, {
        selector: ':nth-child(3) > .control > .input',
        value: 'indirizzo@email.it'
      }, {
        selector: ':nth-child(4) > .control > .input',
        value: 'Password'
      }, {
        selector: ':nth-child(6) > .control > .input',
        value: 'Password'
      }
    ]
    inputs.forEach(element => {
      cy.get(element.selector).type(element.value).should('have.value', element.value).blur().should('have.class', 'is-success')
    })
  })

  it('Does not accept empty inputs', () => {
    cy.visit('/signup')

    let nthChildren = [1, 2, 3, 4, 6]
    nthChildren.forEach(idx => {
      cy.get(`:nth-child(${idx}) > .control > .input`).focus().blur().should('have.class', 'is-danger')
      cy.get(`:nth-child(${idx}) > .help`).should('have.class', 'is-danger').should('have.text', 'Questo campo è obbligatorio')
    })
  })

  it('Verifies email', () => {
    cy.visit('/signup')

    cy.get(':nth-child(3) > .control > .input').as('email')
    cy.get('@email').focus().blur().should('have.class', 'is-danger')
    cy.get('@email').type('valid@emailaddre.ss').blur({force: true}).should('have.class', 'is-success').clear()
    cy.get('@email').type('not an email address at all').blur({force: true}).should('have.class', 'is-danger').clear()
    cy.get('@email').type('another@valid.email').blur({force: true}).should('have.class', 'is-success').clear()
    cy.get('@email').type('partial@email').blur({force: true}).should('have.class', 'is-danger')
  })

  it('Handles password strengths', () => {
    cy.server()

    let strengths = [0, 25, 50, 75, 100]
    strengths.forEach(strength => {
      cy.route('GET', `${Config.apiURL}/api/v1/zxcvbn?input=${strength}password`, {strength}).as(`zxcvbn${strength}`)
    })

    cy.visit('/signup')

    cy.get(':nth-child(4) > .control > .input').as('passwordField')
    strengths.slice().reverse().forEach(strength => {
      cy.get('@passwordField').type(`${strength}password`)
      cy.wait(`@zxcvbn${strength}`)
      cy.get('.progress').should('have.attr', 'value', String(strength))
      cy.get('@passwordField').clear()
    })
  })

  it('Tests password and repeat password', () => {
    cy.server()
    cy.route('GET', `${Config.apiURL}/api/v1/zxcvbn?input=password`, {
      strength: 100
    }).as('zxcvbn')

    cy.visit('/signup')

    cy.get(':nth-child(4) > .control > .input').as('password')
    cy.get(':nth-child(6) > .control > .input').as('repeat')

    cy.get('@password').type('password').should('have.not.class', 'is-danger').blur().should('have.class', 'is-success')
    cy.wait('@zxcvbn')
    cy.get('@repeat').type('otherPassword').blur().should('have.class', 'is-danger')
    cy.get('@password').should('have.class', 'is-danger')
    cy.get('.help').should('have.text', 'Le due password non corrispondono')

    cy.get('@repeat').clear().type('password').blur({force: true})
    cy.get('@password').should('have.class', 'is-success')
    cy.get('@repeat').should('have.class', 'is-success')
  })
})
