// Generated from: ../../specs/apps/ose/www/behaviors/frontend/landing/landing-page.feature
import { test } from "playwright-bdd";

test.describe('Landing Page', () => {

  test.beforeEach('Background', async ({ Given }, testInfo) => { if (testInfo.error) return;
    await Given('the app is running'); 
  });
  
  test('Hero section displays platform information', { tag: ['@unit', '@e2e'] }, async ({ Given, Then, And, page }) => { 
    await Given('the landing page is rendered', null, { page }); 
    await Then('the hero section displays the title "Open Sharia Enterprise Platform"', null, { page }); 
    await And('the hero section displays a description of the platform mission', null, { page }); 
    await And('the hero section contains a "Learn More" link to "/about/"', null, { page }); 
    await And('the hero section contains a "GitHub" link', null, { page }); 
  });

  test('Social icons are displayed', { tag: ['@unit', '@e2e'] }, async ({ Given, Then, And, page }) => { 
    await Given('the landing page is rendered', null, { page }); 
    await Then('a GitHub icon link is visible', null, { page }); 
    await And('an RSS feed icon link is visible', null, { page }); 
  });

});

// == technical section ==

test.use({
  $test: [({}, use) => use(test), { scope: 'test', box: true }],
  $uri: [({}, use) => use('../../specs/apps/ose/www/behaviors/frontend/landing/landing-page.feature'), { scope: 'test', box: true }],
  $bddFileData: [({}, use) => use(bddFileData), { scope: "test", box: true }],
});

const bddFileData = [ // bdd-data-start
  {"pwTestLine":10,"pickleLine":10,"tags":["@unit","@e2e"],"steps":[{"pwStepLine":7,"gherkinStepLine":7,"keywordType":"Context","textWithKeyword":"Given the app is running","isBg":true,"stepMatchArguments":[]},{"pwStepLine":11,"gherkinStepLine":11,"keywordType":"Context","textWithKeyword":"Given the landing page is rendered","stepMatchArguments":[]},{"pwStepLine":12,"gherkinStepLine":12,"keywordType":"Outcome","textWithKeyword":"Then the hero section displays the title \"Open Sharia Enterprise Platform\"","stepMatchArguments":[{"group":{"start":36,"value":"\"Open Sharia Enterprise Platform\"","children":[{"start":37,"value":"Open Sharia Enterprise Platform","children":[{"children":[]}]},{"children":[{"children":[]}]}]},"parameterTypeName":"string"}]},{"pwStepLine":13,"gherkinStepLine":13,"keywordType":"Outcome","textWithKeyword":"And the hero section displays a description of the platform mission","stepMatchArguments":[]},{"pwStepLine":14,"gherkinStepLine":14,"keywordType":"Outcome","textWithKeyword":"And the hero section contains a \"Learn More\" link to \"/about/\"","stepMatchArguments":[{"group":{"start":28,"value":"\"Learn More\"","children":[{"start":29,"value":"Learn More","children":[{"children":[]}]},{"children":[{"children":[]}]}]},"parameterTypeName":"string"},{"group":{"start":49,"value":"\"/about/\"","children":[{"start":50,"value":"/about/","children":[{"children":[]}]},{"children":[{"children":[]}]}]},"parameterTypeName":"string"}]},{"pwStepLine":15,"gherkinStepLine":15,"keywordType":"Outcome","textWithKeyword":"And the hero section contains a \"GitHub\" link","stepMatchArguments":[{"group":{"start":28,"value":"\"GitHub\"","children":[{"start":29,"value":"GitHub","children":[{"children":[]}]},{"children":[{"children":[]}]}]},"parameterTypeName":"string"}]}]},
  {"pwTestLine":18,"pickleLine":18,"tags":["@unit","@e2e"],"steps":[{"pwStepLine":7,"gherkinStepLine":7,"keywordType":"Context","textWithKeyword":"Given the app is running","isBg":true,"stepMatchArguments":[]},{"pwStepLine":19,"gherkinStepLine":19,"keywordType":"Context","textWithKeyword":"Given the landing page is rendered","stepMatchArguments":[]},{"pwStepLine":20,"gherkinStepLine":20,"keywordType":"Outcome","textWithKeyword":"Then a GitHub icon link is visible","stepMatchArguments":[]},{"pwStepLine":21,"gherkinStepLine":21,"keywordType":"Outcome","textWithKeyword":"And an RSS feed icon link is visible","stepMatchArguments":[]}]},
]; // bdd-data-end