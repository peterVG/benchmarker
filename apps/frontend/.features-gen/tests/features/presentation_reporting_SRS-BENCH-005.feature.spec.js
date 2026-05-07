// Generated from: tests/features/presentation_reporting_SRS-BENCH-005.feature
import { test } from "playwright-bdd";

test.describe('Presentation Reporting', () => {

  test.beforeEach('Background', async ({ Given, And, page }, testInfo) => { if (testInfo.error) return;
    await Given('the SQLite database contains historical benchmark runs', null, { page }); 
    await And('the Vanilla JS frontend is running'); 
  });
  
  test('View historical benchmark runs', async ({ When, Then, And, page }) => { 
    await When('I navigate to the dashboard homepage', null, { page }); 
    await Then('I should see a list or table of all historical runs', null, { page }); 
    await And('each entry should display the run date, model used, and hardware profile', null, { page }); 
  });

  test('View detailed graphical metrics for a specific run', async ({ Given, When, Then, And, page }) => { 
    await Given('I am viewing the historical run list', null, { page }); 
    await When('I click on a specific benchmark run', null, { page }); 
    await Then('I should see graphical charts (e.g., bar charts) for latency and tokens/sec', null, { page }); 
    await And('I should see the overall accuracy percentage', null, { page }); 
  });

  test('Displaying the dashboard with an empty database', async ({ Given, When, Then, And, page }) => { 
    await Given('the SQLite database has no historical runs', null, { page }); 
    await When('I navigate to the dashboard homepage', null, { page }); 
    await Then('I should see an empty state message', null, { page }); 
    await And('a prompt explaining how to run a benchmark', null, { page }); 
  });

});

// == technical section ==

test.use({
  $test: [({}, use) => use(test), { scope: 'test', box: true }],
  $uri: [({}, use) => use('tests/features/presentation_reporting_SRS-BENCH-005.feature'), { scope: 'test', box: true }],
  $bddFileData: [({}, use) => use(bddFileData), { scope: "test", box: true }],
});

const bddFileData = [ // bdd-data-start
  {"pwTestLine":11,"pickleLine":12,"tags":[],"steps":[{"pwStepLine":7,"gherkinStepLine":8,"keywordType":"Context","textWithKeyword":"Given the SQLite database contains historical benchmark runs","isBg":true,"stepMatchArguments":[]},{"pwStepLine":8,"gherkinStepLine":9,"keywordType":"Context","textWithKeyword":"And the Vanilla JS frontend is running","isBg":true,"stepMatchArguments":[]},{"pwStepLine":12,"gherkinStepLine":13,"keywordType":"Action","textWithKeyword":"When I navigate to the dashboard homepage","stepMatchArguments":[]},{"pwStepLine":13,"gherkinStepLine":14,"keywordType":"Outcome","textWithKeyword":"Then I should see a list or table of all historical runs","stepMatchArguments":[]},{"pwStepLine":14,"gherkinStepLine":15,"keywordType":"Outcome","textWithKeyword":"And each entry should display the run date, model used, and hardware profile","stepMatchArguments":[]}]},
  {"pwTestLine":17,"pickleLine":18,"tags":[],"steps":[{"pwStepLine":7,"gherkinStepLine":8,"keywordType":"Context","textWithKeyword":"Given the SQLite database contains historical benchmark runs","isBg":true,"stepMatchArguments":[]},{"pwStepLine":8,"gherkinStepLine":9,"keywordType":"Context","textWithKeyword":"And the Vanilla JS frontend is running","isBg":true,"stepMatchArguments":[]},{"pwStepLine":18,"gherkinStepLine":19,"keywordType":"Context","textWithKeyword":"Given I am viewing the historical run list","stepMatchArguments":[]},{"pwStepLine":19,"gherkinStepLine":20,"keywordType":"Action","textWithKeyword":"When I click on a specific benchmark run","stepMatchArguments":[]},{"pwStepLine":20,"gherkinStepLine":21,"keywordType":"Outcome","textWithKeyword":"Then I should see graphical charts (e.g., bar charts) for latency and tokens/sec","stepMatchArguments":[]},{"pwStepLine":21,"gherkinStepLine":22,"keywordType":"Outcome","textWithKeyword":"And I should see the overall accuracy percentage","stepMatchArguments":[]}]},
  {"pwTestLine":24,"pickleLine":25,"tags":[],"steps":[{"pwStepLine":7,"gherkinStepLine":8,"keywordType":"Context","textWithKeyword":"Given the SQLite database contains historical benchmark runs","isBg":true,"stepMatchArguments":[]},{"pwStepLine":8,"gherkinStepLine":9,"keywordType":"Context","textWithKeyword":"And the Vanilla JS frontend is running","isBg":true,"stepMatchArguments":[]},{"pwStepLine":25,"gherkinStepLine":26,"keywordType":"Context","textWithKeyword":"Given the SQLite database has no historical runs","stepMatchArguments":[]},{"pwStepLine":26,"gherkinStepLine":27,"keywordType":"Action","textWithKeyword":"When I navigate to the dashboard homepage","stepMatchArguments":[]},{"pwStepLine":27,"gherkinStepLine":28,"keywordType":"Outcome","textWithKeyword":"Then I should see an empty state message","stepMatchArguments":[]},{"pwStepLine":28,"gherkinStepLine":29,"keywordType":"Outcome","textWithKeyword":"And a prompt explaining how to run a benchmark","stepMatchArguments":[]}]},
]; // bdd-data-end