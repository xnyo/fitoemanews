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
    cy.zxcvbnApi()

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
        value: '100password'
      }, {
        selector: ':nth-child(6) > .control > .input',
        value: '100password'
      }
    ]
    inputs.forEach((element, idx) => {
      cy.get(element.selector).type(element.value).should('have.value', element.value).blur()
      if (idx === 3) {
        cy.wait('@zxcvbn100')
      }
      cy.get(element.selector).should('have.class', 'is-success')
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
    cy.zxcvbnApi()

    cy.visit('/signup')

    cy.get(':nth-child(4) > .control > .input').as('passwordField')
    let strengths = [100, 75, 50, 25]
    strengths.forEach(strength => {
      cy.get('@passwordField').type(`${strength}password`)
      cy.wait(`@zxcvbn${strength}`)
      cy.get('.progress').should('have.attr', 'value', String(strength))
      cy.get('@passwordField').clear()
    })
  })

  it('Tests password and repeat password', () => {
    cy.zxcvbnApi()

    cy.visit('/signup')

    cy.get(':nth-child(4) > .control > .input').as('password')
    cy.get(':nth-child(6) > .control > .input').as('repeat')

    cy.get('@password').type('100password').should('have.not.class', 'is-danger').blur().should('have.class', 'is-success')
    cy.wait('@zxcvbn100')
    cy.get('@repeat').type('otherPassword').blur().should('have.class', 'is-danger')
    cy.get('@password').should('have.class', 'is-danger')
    cy.get('.help').should('have.text', 'Le due password non corrispondono')

    cy.get('@repeat').clear().type('100password').blur({force: true})
    cy.get('@password').should('have.class', 'is-success')
    cy.get('@repeat').should('have.class', 'is-success')
  })

  it('Does not accept weak passwords', () => {
    cy.zxcvbnApi()
    cy.visit('/signup')

    cy.get(':nth-child(4) > .control > .input').as('password')
    cy.get(':nth-child(6) > .control > .input').as('repeat')

    let strengths = [0, 25, 50, 75, 100]
    strengths.forEach(strength => {
      cy.get('@password').clear().type(`${strength}password`)
      cy.get('@repeat').clear().type(`${strength}password`).blur()
      cy.wait(`@zxcvbn${strength}`)
      cy.get('@password').should('have.class', (strength >= 50) ? 'is-success' : 'is-danger')
    })
  })
})
