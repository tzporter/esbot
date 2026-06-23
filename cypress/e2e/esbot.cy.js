/**
 * ESBot End-to-End Test Suite
 * Covers 2 Happy Paths (Chat, Quiz) and 1 Negative Scenario.
 */

describe("ESBot E2E User Flows", () => {
  const baseUrl = "http://localhost:8501";

  beforeEach(() => {
    cy.visit(baseUrl);
    cy.contains("button", "Create Session", {
      matchCase: false,
      timeout: 15000,
    }).should("be.visible");
  });

  it("Happy Path 1: Should create a new session and successfully send/receive a chat message", () => {
    cy.get('input[placeholder="e.g., Python Basics"]')
      .clear()
      .type("My Cypress Session");
    cy.contains("button", "Create Session", { matchCase: false }).click();

    cy.contains("label", "My Cypress Session", { timeout: 10000 }).click();
    cy.contains("Workspace: My Cypress Session", { timeout: 10000 }).should(
      "be.visible",
    );

    const testMessage = "Hello, AI Tutor! Can you explain unit testing?";

    cy.get('[placeholder="Ask a technical question..."]')
      .last()
      .type(testMessage + "{enter}");

    cy.contains(testMessage).should("exist");

    cy.get(".stChatMessage", { timeout: 15000 })
      .last()
      .should("exist")
      .and("not.be.empty");
  });

  it("Happy Path 2: Should generate a quiz and submit an answer", () => {
    cy.get('input[placeholder="e.g., Python Basics"]')
      .clear()
      .type("Quiz Session");
    cy.contains("button", "Create Session", { matchCase: false }).click();

    cy.contains("label", "Quiz Session", { timeout: 10000 }).click();
    cy.contains("Workspace: Quiz Session", { timeout: 10000 }).should("exist");

    cy.contains("📝 AI Knowledge Quiz").click();

    const quizTopic = "Software Engineering Basics";
    // FIXED: Added { force: true } to handle dynamic overlay obstruction
    cy.get('input[placeholder="e.g., Context Managers"]').type(quizTopic, { force: true });
    cy.contains("button", "✨ Generate AI Quiz").click();

    cy.contains("Question 1:", { timeout: 15000 }).should("exist");

    cy.get('input[type="text"]')
      .last()
      .clear()
      .type("This is a test answer for Cypress.");

    cy.contains("button", "Submit Answer").click({ force: true });

    cy.contains(/Correct|Incorrect|Clarification/, {
      matchCase: false,
      timeout: 15000,
    }).should("exist");
  });

  it("Negative Scenario 1: Should show a warning when submitting an empty quiz answer", () => {
    cy.get('input[placeholder="e.g., Python Basics"]')
      .clear()
      .type("Empty Answer Session");
    cy.contains("button", "Create Session", { matchCase: false }).click();

    cy.contains("label", "Empty Answer Session", { timeout: 10000 }).click();
    cy.contains("Workspace: Empty Answer Session", { timeout: 10000 }).should(
      "exist",
    );

    cy.contains("📝 AI Knowledge Quiz").click();

    // FIXED: Added { force: true } here too as a safety precaution against Streamlit DOM updates
    cy.get('input[placeholder="e.g., Context Managers"]').type(
      "Testing negative path",
      { force: true }
    );
    cy.contains("button", "✨ Generate AI Quiz").click();

    cy.contains("Question 1:", { timeout: 15000 }).should("exist");

    cy.contains("button", "Submit Answer").click({ force: true });

    cy.contains("Please type an answer before submitting.").should("exist");
  });
});