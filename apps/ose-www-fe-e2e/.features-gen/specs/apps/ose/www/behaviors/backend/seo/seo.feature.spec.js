// Generated from: ../../specs/apps/ose/www/behaviors/backend/seo/seo.feature
import { test } from "playwright-bdd";

test.describe('SEO', () => {

  test.beforeEach('Background', async ({ Given }, testInfo) => { if (testInfo.error) return;
    await Given('the API is running'); 
  });
  
  test('Sitemap contains all public pages', { tag: ['@unit', '@e2e'] }, async ({ Given, When, Then, And, request }) => { 
    await Given('the content repository contains public pages'); 
    await When('the sitemap is generated', null, { request }); 
    await Then('the sitemap contains a URL for the landing page'); 
    await And('the sitemap contains a URL for the about page'); 
    await And('the sitemap contains URLs for all update pages'); 
  });

  test('Robots.txt allows all crawlers', { tag: ['@unit', '@e2e'] }, async ({ When, Then, And, request }) => { 
    await When('the robots.txt is generated', null, { request }); 
    await Then('it allows all user agents'); 
    await And('it references the sitemap URL'); 
  });

});

// == technical section ==

test.use({
  $test: [({}, use) => use(test), { scope: 'test', box: true }],
  $uri: [({}, use) => use('../../specs/apps/ose/www/behaviors/backend/seo/seo.feature'), { scope: 'test', box: true }],
  $bddFileData: [({}, use) => use(bddFileData), { scope: "test", box: true }],
});

const bddFileData = [ // bdd-data-start
  {"pwTestLine":10,"pickleLine":10,"tags":["@unit","@e2e"],"steps":[{"pwStepLine":7,"gherkinStepLine":7,"keywordType":"Context","textWithKeyword":"Given the API is running","isBg":true,"stepMatchArguments":[]},{"pwStepLine":11,"gherkinStepLine":11,"keywordType":"Context","textWithKeyword":"Given the content repository contains public pages","stepMatchArguments":[]},{"pwStepLine":12,"gherkinStepLine":12,"keywordType":"Action","textWithKeyword":"When the sitemap is generated","stepMatchArguments":[]},{"pwStepLine":13,"gherkinStepLine":13,"keywordType":"Outcome","textWithKeyword":"Then the sitemap contains a URL for the landing page","stepMatchArguments":[]},{"pwStepLine":14,"gherkinStepLine":14,"keywordType":"Outcome","textWithKeyword":"And the sitemap contains a URL for the about page","stepMatchArguments":[]},{"pwStepLine":15,"gherkinStepLine":15,"keywordType":"Outcome","textWithKeyword":"And the sitemap contains URLs for all update pages","stepMatchArguments":[]}]},
  {"pwTestLine":18,"pickleLine":18,"tags":["@unit","@e2e"],"steps":[{"pwStepLine":7,"gherkinStepLine":7,"keywordType":"Context","textWithKeyword":"Given the API is running","isBg":true,"stepMatchArguments":[]},{"pwStepLine":19,"gherkinStepLine":19,"keywordType":"Action","textWithKeyword":"When the robots.txt is generated","stepMatchArguments":[]},{"pwStepLine":20,"gherkinStepLine":20,"keywordType":"Outcome","textWithKeyword":"Then it allows all user agents","stepMatchArguments":[]},{"pwStepLine":21,"gherkinStepLine":21,"keywordType":"Outcome","textWithKeyword":"And it references the sitemap URL","stepMatchArguments":[]}]},
]; // bdd-data-end