// Generated from: tests/features/control_dashboard_SRS-BENCH-005.feature
import { test } from "playwright-bdd";

test.describe('Control Dashboard', () => {

  test('Render historical metrics chart', async ({ Given, Then, page }) => { 
    await Given('the dashboard is loaded', null, { page }); 
    await Then('I should see the historical metrics chart rendered', null, { page }); 
  });

  test('Submit configuration form', async ({ Given, When, Then, And, page }) => { 
    await Given('the dashboard is loaded', null, { page }); 
    await When('I select the "ollama" runner', null, { page }); 
    await And('I enter the model name "llama3.2"', null, { page }); 
    await And('I enter the dataset ID "ag_news"', null, { page }); 
    await And('I click the Run Benchmark button', null, { page }); 
    await Then('I should see a status indicating the run has started', null, { page }); 
    await And('the terminal should become visible', null, { page }); 
  });

  test('Stream logs to the terminal', async ({ Given, When, Then, page }) => { 
    await Given('a benchmarking run has been started', null, { page }); 
    await When('the backend sends log messages via WebSocket', null, { page }); 
    await Then('the terminal should append the log messages to its output', null, { page }); 
  });

});

// == technical section ==

test.use({
  $test: [({}, use) => use(test), { scope: 'test', box: true }],
  $uri: [({}, use) => use('tests/features/control_dashboard_SRS-BENCH-005.feature'), { scope: 'test', box: true }],
  $bddFileData: [({}, use) => use(bddFileData), { scope: "test", box: true }],
});

const bddFileData = [ // bdd-data-start
  {"pwTestLine":6,"pickleLine":6,"tags":[],"steps":[{"pwStepLine":7,"gherkinStepLine":7,"keywordType":"Context","textWithKeyword":"Given the dashboard is loaded","stepMatchArguments":[]},{"pwStepLine":8,"gherkinStepLine":8,"keywordType":"Outcome","textWithKeyword":"Then I should see the historical metrics chart rendered","stepMatchArguments":[]}]},
  {"pwTestLine":11,"pickleLine":10,"tags":[],"steps":[{"pwStepLine":12,"gherkinStepLine":11,"keywordType":"Context","textWithKeyword":"Given the dashboard is loaded","stepMatchArguments":[]},{"pwStepLine":13,"gherkinStepLine":12,"keywordType":"Action","textWithKeyword":"When I select the \"ollama\" runner","stepMatchArguments":[{"group":{"start":13,"value":"\"ollama\"","children":[{"start":14,"value":"ollama","children":[{"children":[]}]},{"children":[{"children":[]}]}]},"parameterTypeName":"string"}]},{"pwStepLine":14,"gherkinStepLine":13,"keywordType":"Action","textWithKeyword":"And I enter the model name \"llama3.2\"","stepMatchArguments":[{"group":{"start":23,"value":"\"llama3.2\"","children":[{"start":24,"value":"llama3.2","children":[{"children":[]}]},{"children":[{"children":[]}]}]},"parameterTypeName":"string"}]},{"pwStepLine":15,"gherkinStepLine":14,"keywordType":"Action","textWithKeyword":"And I enter the dataset ID \"ag_news\"","stepMatchArguments":[{"group":{"start":23,"value":"\"ag_news\"","children":[{"start":24,"value":"ag_news","children":[{"children":[]}]},{"children":[{"children":[]}]}]},"parameterTypeName":"string"}]},{"pwStepLine":16,"gherkinStepLine":15,"keywordType":"Action","textWithKeyword":"And I click the Run Benchmark button","stepMatchArguments":[]},{"pwStepLine":17,"gherkinStepLine":16,"keywordType":"Outcome","textWithKeyword":"Then I should see a status indicating the run has started","stepMatchArguments":[]},{"pwStepLine":18,"gherkinStepLine":17,"keywordType":"Outcome","textWithKeyword":"And the terminal should become visible","stepMatchArguments":[]}]},
  {"pwTestLine":21,"pickleLine":19,"tags":[],"steps":[{"pwStepLine":22,"gherkinStepLine":20,"keywordType":"Context","textWithKeyword":"Given a benchmarking run has been started","stepMatchArguments":[]},{"pwStepLine":23,"gherkinStepLine":21,"keywordType":"Action","textWithKeyword":"When the backend sends log messages via WebSocket","stepMatchArguments":[]},{"pwStepLine":24,"gherkinStepLine":22,"keywordType":"Outcome","textWithKeyword":"Then the terminal should append the log messages to its output","stepMatchArguments":[]}]},
]; // bdd-data-end