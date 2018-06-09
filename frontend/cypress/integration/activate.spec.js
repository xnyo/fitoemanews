describe('Activate', () => {
  it('Displays loading', () => {
    cy.activateApi()
    let routes = ['/activate/valid_token', '/activate/invalid_token']
    routes.forEach(element => {
      cy.visit(element)
      cy.get('#msg').should('have.class', 'is-loading')
      cy.wait(element.indexOf('invalid') >= 0 ? '@activateInvalid' : '@activateValid')
      cy.get('#msg').should('not.have.class', 'is-loading')
    })
  })

  it('Activates a valid token', () => {
    cy.activateApi()
    cy.visit('/activate/valid_token')
    cy.wait('@activateValid')
    cy.get('.icon > .title').should('have.text', 'Account attivato!')
  })

  it('Does not activate an invalid token', () => {
    cy.activateApi()
    cy.visit('/activate/invalid_token')
    cy.wait('@activateInvalid')
    cy.get('.icon > .title').should('have.text', 'Si è verificato un errore')
    cy.get('p').should('have.text', 'Messaggio di errore')
  })
})
