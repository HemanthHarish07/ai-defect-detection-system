describe("Defect dashboard flow", () => {
  it("loads the dashboard and uploads an image", () => {
    cy.visit("/");
    cy.contains("Automated Defect Detection Dashboard").should("be.visible");
    cy.fixture("sample-base64.txt").then((fileContent) => {
      cy.get("input[type=file]").attachFile({
        fileContent,
        fileName: "sample.png",
        mimeType: "image/png",
        encoding: "base64",
      });
      cy.contains("Submit Image").click();
      cy.contains(/upload successful/i, { timeout: 10000 }).should("be.visible");
    });
  });
});
