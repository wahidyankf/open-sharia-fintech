// Generated from: ../../specs/apps/ose/www/behaviors/frontend/app-shell/responsive.feature
import { test } from "playwright-bdd";

test.describe('Responsive Design', () => {

  test.beforeEach('Background', async ({ Given }, testInfo) => { if (testInfo.error) return;
    await Given('the app is running'); 
  });
  
  test('Mobile viewport shows hamburger navigation', { tag: ['@unit', '@e2e'] }, async ({ Given, When, Then, And, page }) => { 
    await Given('the viewport width is less than 640 pixels', null, { page }); 
    await When('the header is rendered', null, { page }); 
    await Then('the hamburger menu button is visible', null, { page }); 
    await And('the desktop navigation links are hidden', null, { page }); 
  });

  test('Desktop viewport shows full navigation', { tag: ['@unit', '@e2e'] }, async ({ Given, When, Then, And, page }) => { 
    await Given('the viewport width is greater than 1024 pixels', null, { page }); 
    await When('the header is rendered', null, { page }); 
    await Then('the desktop navigation links are visible', null, { page }); 
    await And('the hamburger menu button is hidden', null, { page }); 
  });

});

// == technical section ==

test.use({
  $test: [({}, use) => use(test), { scope: 'test', box: true }],
  $uri: [({}, use) => use('../../specs/apps/ose/www/behaviors/frontend/app-shell/responsive.feature'), { scope: 'test', box: true }],
  $bddFileData: [({}, use) => use(bddFileData), { scope: "test", box: true }],
});

const bddFileData = [ // bdd-data-start
  {"pwTestLine":10,"pickleLine":10,"tags":["@unit","@e2e"],"steps":[{"pwStepLine":7,"gherkinStepLine":7,"keywordType":"Context","textWithKeyword":"Given the app is running","isBg":true,"stepMatchArguments":[]},{"pwStepLine":11,"gherkinStepLine":11,"keywordType":"Context","textWithKeyword":"Given the viewport width is less than 640 pixels","stepMatchArguments":[]},{"pwStepLine":12,"gherkinStepLine":12,"keywordType":"Action","textWithKeyword":"When the header is rendered","stepMatchArguments":[]},{"pwStepLine":13,"gherkinStepLine":13,"keywordType":"Outcome","textWithKeyword":"Then the hamburger menu button is visible","stepMatchArguments":[]},{"pwStepLine":14,"gherkinStepLine":14,"keywordType":"Outcome","textWithKeyword":"And the desktop navigation links are hidden","stepMatchArguments":[]}]},
  {"pwTestLine":17,"pickleLine":17,"tags":["@unit","@e2e"],"steps":[{"pwStepLine":7,"gherkinStepLine":7,"keywordType":"Context","textWithKeyword":"Given the app is running","isBg":true,"stepMatchArguments":[]},{"pwStepLine":18,"gherkinStepLine":18,"keywordType":"Context","textWithKeyword":"Given the viewport width is greater than 1024 pixels","stepMatchArguments":[]},{"pwStepLine":19,"gherkinStepLine":19,"keywordType":"Action","textWithKeyword":"When the header is rendered","stepMatchArguments":[]},{"pwStepLine":20,"gherkinStepLine":20,"keywordType":"Outcome","textWithKeyword":"Then the desktop navigation links are visible","stepMatchArguments":[]},{"pwStepLine":21,"gherkinStepLine":21,"keywordType":"Outcome","textWithKeyword":"And the hamburger menu button is hidden","stepMatchArguments":[]}]},
]; // bdd-data-end