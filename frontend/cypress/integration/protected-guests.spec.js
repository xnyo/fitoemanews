describe('Protected and guests-only routes', () => {
  it('Does not redirect when on protected page and logged in', () => {
    cy.loggedInApi()
    cy.visit('/')
    cy.wait('@userData')
    cy.location('pathname').should('eq', '/')
  })

  it('Does redirect to login when on protected page and not logged in', () => {
    cy.notLoggedInApi()
    cy.visit('/')
    cy.wait('@userData')
    cy.location('pathname').should('eq', '/login')
  })

  it('Does not redirect when on guests-only page and not logged in', () => {
    cy.notLoggedInApi()
    cy.visit('/login')
    cy.wait('@userData')
    cy.location('pathname').should('eq', '/login')
  })

  it('Does redirect when on guests-only page and logged in', () => {
    cy.loggedInApi()
    cy.visit('/login')
    cy.wait('@userData')
    cy.location('pathname').should('eq', '/')
  })
})
